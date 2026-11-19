"""Import captions from an .srt or .ass file: cue times are spread over the words of each cue (by letter count)
and shifted so they are relative to the clip start, ready for the caption editor / export."""
import math
import re


def _seconds(value):
    value = value.strip().replace(',', '.')
    parts = value.split(':')
    if len(parts) == 3:
        h, m, s = parts
    elif len(parts) == 2:
        h, m, s = '0', parts[0], parts[1]
    else:
        raise ValueError('Bad time: ' + value)
    return int(h) * 3600 + int(m) * 60 + float(s)


def _clean(text):
    text = re.sub(r'\{[^}]*\}', '', text)                 # ASS override tags
    text = re.sub(r'<[^>]+>', '', text)                   # <i> <b> <font ...>
    text = text.replace('\\N', ' ').replace('\\n', ' ').replace('\\h', ' ')
    return ' '.join(text.split())


def cues(text):
    """-> [(start, end, text)] from SRT or ASS content."""
    text = text.lstrip('﻿').replace('\r\n', '\n').replace('\r', '\n')
    out = []
    if re.search(r'^\s*\[Events\]', text, re.M) or re.search(r'^\s*Dialogue:', text, re.M):
        fmt = None
        for line in text.split('\n'):
            if line.lower().startswith('format:') and 'start' in line.lower() and 'text' in line.lower():
                fmt = [x.strip().lower() for x in line.split(':', 1)[1].split(',')]
            elif line.startswith('Dialogue:'):
                cols = fmt or ['layer', 'start', 'end', 'style', 'name', 'marginl', 'marginr', 'marginv', 'effect', 'text']
                parts = line.split(':', 1)[1].lstrip().split(',', len(cols) - 1)
                if len(parts) < len(cols):
                    continue
                row = dict(zip(cols, parts))
                try:
                    out.append((_seconds(row['start']), _seconds(row['end']), _clean(row['text'])))
                except (ValueError, KeyError):
                    continue
    else:
        for block in re.split(r'\n\s*\n', text.strip()):
            lines = [l for l in block.split('\n') if l.strip()]
            for i, l in enumerate(lines):
                if '-->' in l:
                    try:
                        a, b = l.split('-->')
                        out.append((_seconds(a), _seconds(b.split()[0] if b.split() else b), _clean(' '.join(lines[i + 1:]))))
                    except (ValueError, IndexError):
                        pass
                    break
    out = [(a, b, t) for a, b, t in out if t and b > a and math.isfinite(a) and math.isfinite(b)]
    if not out:
        raise ValueError('No captions found. Use an .srt or .ass file.')
    return sorted(out)


def words_from(text, clip_start=0.0, clip_end=None):
    """Words with start/end relative to the clip (clip_start..clip_end in source time). Cues outside the clip are dropped."""
    result = []
    for a, b, t in cues(text):
        if b <= clip_start or (clip_end is not None and a >= clip_end):
            continue
        tokens = t.split()
        total = sum(len(x) + 1 for x in tokens)
        pos = a
        for tok in tokens:
            span = (b - a) * (len(tok) + 1) / total
            ws, we = pos, pos + span
            pos = we
            ws, we = ws - clip_start, we - clip_start
            if clip_end is not None:
                we = min(we, clip_end - clip_start)
            if we <= 0 or ws >= (clip_end - clip_start if clip_end is not None else 1e9):
                continue
            ws = max(0.0, ws)
            if we - ws < 0.03:
                continue
            result.append({'start': round(ws, 3), 'end': round(we, 3), 'text': tok[:100]})
    return result


def attach(app):
    from fastapi import HTTPException

    @app.post('/captions/parse')
    def parse_captions(b: dict):
        try:
            text = str(b.get('text', ''))
            if len(text) > 4_000_000:
                raise ValueError('That caption file is too large.')
            start = float(b.get('start', 0) or 0)
            end = b.get('end')
            end = float(end) if end not in (None, '') else None
            if not math.isfinite(start) or (end is not None and (not math.isfinite(end) or end <= start)):
                raise ValueError('Check the clip start and end.')
            words = words_from(text, start, end)
            if not words:
                raise ValueError('No caption lines fall inside this clip. Check the clip start and end.')
            return {'words': words, 'cues': len(cues(text))}
        except (ValueError, TypeError) as e:
            raise HTTPException(400, str(e))
