"""Phone remote: use NeonClipping from a phone, or from any browser when it is hosted (for example on Railway).

The heavy work (recording, speech, rendering) always happens on the server. The browser is a remote control and viewer.

Safety rules:
  * Requests from the machine itself (127.0.0.1) are never asked for a PIN.
  * Anything else is refused unless phone access is switched on:
        NEONCLIPPING_LAN=1   (home Wi-Fi use, the "Start-NeonClipping-Phone" shortcut), or
        PHONE_PIN=<secret>   (hosted use; this also switches phone access on)
  * Outside requests need the PIN. After 5 wrong tries an address is locked for 10 minutes. A correct PIN gives an HttpOnly cookie.
  * Home Wi-Fi mode (NEONCLIPPING_LAN=1 only): a logged-in phone can use only the routes listed in ALLOW.
  * Hosted mode (PHONE_PIN set, or NEONCLIPPING_PHONE_FULL=1): a logged-in browser can use the whole app, except the routes in BLOCK
    (cloud AI key, self-update, YouTube cookie settings, PIN management).

Settings (environment variables):
  PHONE_PIN                 Any secret string (use 20+ random characters when the app is on the internet). Overrides data/phone.json.
  PHONE_SALT                Optional. Changing it signs every browser out.
  NEONCLIPPING_PHONE_FULL   1 = full access after login, 0 = phone routes only. Default: 1 when PHONE_PIN is set, otherwise 0.
"""
import hmac
import hashlib
import json
import os
import secrets
import socket
import threading
import time
from pathlib import Path

from fastapi import HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse, Response

LOCAL = ('127.0.0.1', '::1', 'localhost')
ALLOW = ('/m', '/manifest.webmanifest', '/phone-icon.svg', '/live', '/live-active', '/library', '/media', '/text', '/make', '/status',
         '/clips', '/feedback', '/creators', '/donate', '/healthz', '/assets')
PUBLIC = ('/m', '/m/login', '/manifest.webmanifest', '/phone-icon.svg', '/healthz')   # carry no data, no PIN needed
BLOCK = ('/phone', '/update', '/llm', '/ytdl')                                          # never reachable from outside, even after login
MAX_TRIES, LOCK_SECONDS = 5, 600
MAX_TRACKED = 2000
COOKIE = 'nc_phone'
FORWARD_HEADERS = ('x-forwarded-for', 'x-real-ip', 'forwarded', 'cf-connecting-ip')


def is_local(host):
    return host in LOCAL or str(host).startswith('127.')


def under(path, prefixes):
    return any(path == p or path.startswith(p + '/') for p in prefixes)


def allowed(path):
    return under(path, ALLOW)


def env_pin():
    return (os.environ.get('PHONE_PIN') or '').strip()


def lan_enabled():
    return os.environ.get('NEONCLIPPING_LAN') == '1' or bool(env_pin())


def full_access():
    flag = os.environ.get('NEONCLIPPING_PHONE_FULL')
    if flag in ('0', '1'):
        return flag == '1'
    return bool(env_pin())


def lan_ips():
    """Private IPv4 addresses of this PC (what a phone on the same Wi-Fi would type)."""
    found = []
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('10.255.255.255', 1))                 # no packet is sent; it only picks the outgoing interface
        found.append(s.getsockname()[0])
        s.close()
    except OSError:
        pass
    try:
        for info in socket.getaddrinfo(socket.gethostname(), None, socket.AF_INET):
            found.append(info[4][0])
    except OSError:
        pass
    out = []
    for ip in found:
        parts = ip.split('.')
        try:
            private = ip.startswith(('10.', '192.168.')) or (ip.startswith('172.') and len(parts) > 1 and 16 <= int(parts[1]) <= 31)
        except ValueError:
            private = False
        if private and ip not in out:
            out.append(ip)
    return out


def _same(a, b):
    """Constant-time string comparison that never raises (non-ASCII input is fine)."""
    return hmac.compare_digest(str(a).encode('utf-8', 'replace'), str(b).encode('utf-8', 'replace'))


def attach(app, data, root):
    store = Path(data) / 'phone.json'
    fails = {}                 # client address -> [count, first_time]
    lock = threading.Lock()
    cache = {}                 # keeps the PIN stable even if the disk cannot be written

    def new_pin():
        j = {'pin': f'{secrets.randbelow(10**6):06d}', 'salt': secrets.token_hex(16)}
        try:
            store.parent.mkdir(parents=True, exist_ok=True)
            tmp = store.with_suffix('.tmp')
            tmp.write_text(json.dumps(j), encoding='utf-8')
            tmp.replace(store)
        except OSError:
            pass               # read-only disk: the PIN lives in memory for this run
        return j

    def load():
        pin = env_pin()
        if pin:
            return {'pin': pin, 'salt': os.environ.get('PHONE_SALT') or 'neonclipping-phone'}
        with lock:
            if cache.get('j'):
                return cache['j']
            try:
                j = json.loads(store.read_text(encoding='utf-8'))
                if isinstance(j, dict) and j.get('pin') and j.get('salt'):
                    cache['j'] = {'pin': str(j['pin']), 'salt': str(j['salt'])}
                    return cache['j']
            except (OSError, ValueError):
                pass
            cache['j'] = new_pin()
            return cache['j']

    def token(j):
        return hmac.new(str(j['salt']).encode(), str(j['pin']).encode(), hashlib.sha256).hexdigest()

    def authed(request):
        got = request.cookies.get(COOKIE, '')
        return bool(got) and _same(got, token(load()))

    def proxied(request):
        return any(h in request.headers for h in FORWARD_HEADERS)

    def on_pc(request):
        """True only for a direct request from this machine. A request that came through a proxy is never 'the PC'."""
        host = request.client.host if request.client else ''
        return is_local(host) and not proxied(request)

    def client_id(request):
        fwd = request.headers.get('x-real-ip') or (request.headers.get('x-forwarded-for') or '').split(',')[0].strip()
        return fwd or (request.client.host if request.client else '?')

    def secure_cookie(request):
        return request.headers.get('x-forwarded-proto', request.url.scheme) == 'https'

    def port_of(request):
        return os.environ.get('NEONCLIPPING_PORT') or str(request.url.port or 8770)

    @app.middleware('http')
    async def gate(request: Request, call_next):
        try:
            if on_pc(request):
                return await call_next(request)
            path = request.url.path
            if not lan_enabled():
                return JSONResponse({'detail': 'Phone access is off on this computer.'}, status_code=403)
            if under(path, PUBLIC):
                return await call_next(request)                 # the page itself and the PIN form carry no data
            if under(path, BLOCK):
                return JSONResponse({'detail': 'This is only available on the PC.'}, status_code=403)
            if not full_access() and not allowed(path):
                return JSONResponse({'detail': 'This is only available on the PC.'}, status_code=403)
            if not authed(request):
                if request.method in ('GET', 'HEAD') and path == '/':
                    return RedirectResponse('/m', status_code=302)
                return JSONResponse({'detail': 'Enter the PIN shown on the PC.'}, status_code=401)
        except Exception:
            return JSONResponse({'detail': 'Access check failed. Try again.'}, status_code=500)
        return await call_next(request)

    @app.get('/healthz')
    def healthz():
        return {'ok': True}

    @app.get('/m')
    def mobile_page():
        page = Path(root) / 'mobile.html'
        try:
            return HTMLResponse(page.read_text(encoding='utf-8'))
        except OSError:
            return JSONResponse({'detail': 'mobile.html is missing from this install.'}, status_code=404)

    @app.post('/m/login')
    def login(b: dict, request: Request):
        ip = client_id(request)
        now = time.time()
        with lock:
            count, first = fails.get(ip, [0, now])
            if now - first >= LOCK_SECONDS:
                count, first = 0, now
            if count >= MAX_TRIES:
                raise HTTPException(429, 'Too many wrong PINs. Try again in a few minutes.')
        j = load()
        if not _same(str(b.get('pin', '')).strip(), j['pin']):
            with lock:
                if len(fails) > MAX_TRACKED:
                    fails.clear()
                fails[ip] = [count + 1, first]
            time.sleep(0.4)                                     # slows down guessing
            raise HTTPException(401, 'Wrong PIN.')
        with lock:
            fails.pop(ip, None)
        resp = JSONResponse({'ok': True})
        resp.set_cookie(COOKIE, token(j), httponly=True, samesite='lax', secure=secure_cookie(request), max_age=30 * 24 * 3600)
        return resp

    @app.get('/phone/status')
    def status(request: Request):
        if not on_pc(request):
            raise HTTPException(403, 'This is only available on the PC.')
        port = port_of(request)
        on = lan_enabled()
        return {'enabled': on, 'port': port, 'urls': [f'http://{ip}:{port}/m' for ip in lan_ips()] if on else [],
                'pin': load()['pin'] if on else None}

    @app.post('/phone/newpin')
    def newpin(request: Request):
        if not on_pc(request):
            raise HTTPException(403, 'This is only available on the PC.')
        if env_pin():
            raise HTTPException(400, 'The PIN is set by the PHONE_PIN variable. Change it there.')
        with lock:
            cache['j'] = new_pin()
            return {'pin': cache['j']['pin']}

    @app.get('/manifest.webmanifest')
    def manifest():
        return JSONResponse({'name': 'NeonClipping', 'short_name': 'NeonClip', 'start_url': '/m', 'scope': '/', 'display': 'standalone',
                             'background_color': '#0b0912', 'theme_color': '#0b0912',
                             'icons': [{'src': '/phone-icon.svg', 'sizes': 'any', 'type': 'image/svg+xml', 'purpose': 'any'}]},
                            media_type='application/manifest+json')

    @app.get('/phone-icon.svg')
    def icon():
        svg = ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'><rect width='64' height='64' rx='14' fill='#0b0912'/>"
               "<text x='8' y='46' font-family='Impact,Arial Black' font-size='38' fill='#ff4ba5'>N</text>"
               "<path d='M34 40 L52 22 M40 22 H52 V34' stroke='#58e8f7' stroke-width='5' fill='none' stroke-linecap='round'/></svg>")
        return Response(svg, media_type='image/svg+xml')
