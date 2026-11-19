# NeonClipping test report

Generated 2026-11-20 02:17 by tests/make_report.py from tests/report.json.

**187 of 187 checks pass.**

## Problems found by the tests and fixed

| # | Found | Fix |
|---|---|---|
| 1 | Caption grouping lost a whole caption group and repeated the last one whenever a single trailing word was merged (visible in the MrBeast style: 'TEST OH MY GOD' missing). Python stored `groups[-2] += groups.pop()` into the wrong list entry. Found by looking at the rendered frames, not by the pass/fail checks. | captions.group_words pops first, then appends; new unit tests check every word appears exactly once in order over 500 random word streams. |
| 2 | POST /make with min_len longer than max_len silently started a job. | Rejected with HTTP 400 and a clear message; NaN / infinite lengths also rejected. |
| 3 | Caption accuracy defaulted to 'Accurate (turbo)'. You wanted Fast by default. | UI select and the API default are Fast now. |
| 4 | Make failed with 'Cannot load the vocabulary from the model directory': the turbo speech model folder had only model.bin (half-finished download). | Missing small files downloaded; captions._turbo_spec() now requires a complete snapshot and repairs an incomplete one itself. |
| 5 | Result cards (Make clips / Live) kept pointing at old clips after 'apply to all'; Live cards had no Edit button; Edit on an old card used a replaced clip. | Cards follow the newest file, Live cards got Edit clip, the server resolves old ids to the newest version. |
| 6 | The creator list was stored as data/creators.json, which the library and editor read as a clip record (library would have returned 500). | Stored as data/creators.store; counting code ignores non-record files. |
| 7 | Stop then 'Check now' on a creator restarted recording at once. | Stop settles a 30-minute pause first; Check now no longer cancels it; Auto off/on resumes immediately; the chip shows the pause. |
| 8 | Hindi Whisper loops ('chal chal chal chal ...') and stray accented / non-Latin junk ('funcao', 'nosga') ended up in Hinglish captions. | Words said more than 3 times in a row are cut back to 3; Hinglish captions are folded to plain ASCII letters. Unit-tested. |
| 9 | My clips with 100+ clips requested metadata for every video at once. | Videos load only when they scroll near the screen (IntersectionObserver). |
| 10 | An unattended (auto) live recording could grow without limit. | 3-hour cap per session, stop below 8 GB free disk, recording deleted after the last clip is cut. |
| 11 | install.ps1 printed the Desktop-shortcut message even with -NoShortcut. | Message follows the option; script is still ASCII-only and parses. |
| 12 | Browser could keep an old app.js after a fix. | Asset version in index.html bumped on every change. |

## Page, API and input validation  (34/34)

| Result | Check | Evidence |
|---|---|---|
| PASS | index.html served | 13269 |
| PASS | every $("id") used by app.js exists in index.html | missing: [] |
| PASS | app.js syntax (node --check) |  |
| PASS | GET /assets/app.js |  |
| PASS | GET /assets/style.css |  |
| PASS | GET /library |  |
| PASS | GET /donate |  |
| PASS | GET /feedback/summary |  |
| PASS | GET /live-active |  |
| PASS | GET /creators |  |
| PASS | GET /layouts |  |
| PASS | /layouts returns 11 layouts with geometry | 11 |
| PASS | /layouts rejects bad speaker size |  |
| PASS | donate links are https only | {'razorpay': 'https://rzp.io/rzp/JN41CpW'} |
| PASS | /make without link or id -> 4xx |  |
| PASS | /make with bad count -> 400 |  |
| PASS | /export unknown source -> 400 |  |
| PASS | /export rejects bad layout |  |
| PASS | /export rejects bad caption style |  |
| PASS | /export rejects end before start |  |
| PASS | /export rejects clip > 10 min |  |
| PASS | /export rejects caption_y out of range |  |
| PASS | /export rejects NaN crop |  |
| PASS | /transcribe rejects unknown language |  |
| PASS | /upload rejects a file that is not a video | {"detail":"Choose a playable video file."} |
| PASS | /live/start rejects junk |  |
| PASS | /live/start rejects YouTube link without id |  |
| PASS | /live/<unknown> -> 404 |  |
| PASS | /status/<unknown> not 500 |  |
| PASS | /make/<unknown> not 500 |  |
| PASS | /media path traversal blocked |  |
| PASS | /text path traversal blocked |  |
| PASS | /clips/<bad>/edit -> 4xx |  |
| PASS | /clips/reedit rejects unknown change key |  |

## Rendering: 11 layouts x 5 caption styles x positions  (22/22)

| Result | Check | Evidence |
|---|---|---|
| PASS | render layout stack (gta captions) | 1080x1920 h264/aac 6.0s enc=h264_nvenc words=12 |
| PASS | render layout bottom (gta captions) | 1080x1920 h264/aac 6.0s enc=h264_nvenc words=12 |
| PASS | render layout blur (gta captions) | 1080x1920 h264/aac 6.0s enc=h264_nvenc words=12 |
| PASS | render layout fill (gta captions) | 1080x1920 h264/aac 6.0s enc=h264_nvenc words=12 |
| PASS | render layout game (gta captions) | 1080x1920 h264/aac 6.0s enc=h264_nvenc words=12 |
| PASS | render layout pip_tl (gta captions) | 1080x1920 h264/aac 6.0s enc=h264_nvenc words=12 |
| PASS | render layout pip_tr (gta captions) | 1080x1920 h264/aac 6.0s enc=h264_nvenc words=12 |
| PASS | render layout pip_bl (gta captions) | 1080x1920 h264/aac 6.0s enc=h264_nvenc words=12 |
| PASS | render layout pip_br (gta captions) | 1080x1920 h264/aac 6.0s enc=h264_nvenc words=12 |
| PASS | render layout circle (gta captions) | 1080x1920 h264/aac 6.0s enc=h264_nvenc words=12 |
| PASS | render layout side (gta captions) | 1080x1920 h264/aac 6.0s enc=h264_nvenc words=12 |
| PASS | render caption style gta (blur layout) | 1080x1920 h264/aac 6.0s enc=h264_nvenc words=12 |
| PASS | render caption style bold (blur layout) | 1080x1920 h264/aac 6.0s enc=h264_nvenc words=12 |
| PASS | render caption style clean (blur layout) | 1080x1920 h264/aac 6.0s enc=h264_nvenc words=12 |
| PASS | render caption style hormozi (blur layout) | 1080x1920 h264/aac 6.0s enc=h264_nvenc words=12 |
| PASS | render caption style mrbeast (blur layout) | 1080x1920 h264/aac 6.0s enc=h264_nvenc words=12 |
| PASS | render without captions | words=0 |
| PASS | render caption position top (caption_y=600) | 1080x1920 h264/aac 6.0s enc=h264_nvenc words=12 |
| PASS | render caption position bottom (caption_y=1700) | 1080x1920 h264/aac 6.0s enc=h264_nvenc words=12 |
| PASS | render speaker size 0.2 / 0.5 |  |
| PASS | render accepts unicode hook (Hinglish)  | 1080x1920 h264/aac 6.0s enc=h264_nvenc words=12 |
| PASS | SRT downloadable for a captioned clip | b1261591e046453bafae1c96a91e6b0e |

## Editing saved clips (one / all clips of a video)  (12/12)

| Result | Check | Evidence |
|---|---|---|
| PASS | edit panel data for a saved clip | 3 |
| PASS | apply style=bold to ONLY this clip | 1 clips,  |
| PASS | only the chosen clip changed | ['bold', 'gta', 'gta'] |
| PASS | apply layout+style to ALL clips of the video | 3 clips,  |
| PASS | all 3 clips changed, each kept its own title/hook | [('circle', 'hormozi', 'T0'), ('circle', 'hormozi', 'T1'), ('circle', 'hormozi', 'T2')] |
| PASS | stale (old) clip id still edits the newest version | 914a3dd3 |
| PASS | apply captions OFF to all | 3 clips,  |
| PASS | apply speaker size + caption position to all | 3 clips,  |
| PASS | apply new cam/game boxes to all | 3 clips,  |
| PASS | reedit rejects invalid layout |  |
| PASS | reedit rejects invalid caption style |  |
| PASS | library shows exactly 3 live clips of the batch (no duplicates) | 3 |

## Make clips: sources, modes, languages, errors  (18/18)

| Result | Check | Evidence |
|---|---|---|
| PASS | Make 2-hour Hindi video, Best Hindi (large-v3), Hinglish captions | 1 clips in 562s, all 1080x1920 h264/aac, titles+scores+captions OK |
| PASS | error: nonexistent YouTube id | full run, tests/out/run_make.log (every clip checked: 1080x1920 h264/aac, duration range, titles, scores, caption style, no Devanagari in Hi |
| PASS | error: not a video URL | full run, tests/out/run_make.log (every clip checked: 1080x1920 h264/aac, duration range, titles, scores, caption style, no Devanagari in Hi |
| PASS | error: live stream link is refused with a clear message | full run, tests/out/run_make.log (every clip checked: 1080x1920 h264/aac, duration range, titles, scores, caption style, no Devanagari in Hi |
| PASS | error: min_len > max_len | full run, tests/out/run_make.log (every clip checked: 1080x1920 h264/aac, duration range, titles, scores, caption style, no Devanagari in Hi |
| PASS | Make 132s English video: mode=fast, accurate=fast, language=, style=gta, layout=blur | full run, tests/out/run_make.log (every clip checked: 1080x1920 h264/aac, duration range, titles, scores, caption style, no Devanagari in Hi |
| PASS | Make 132s English video: mode=deep, accurate=accurate, language=en, style=bold, layout=stack | full run, tests/out/run_make.log (every clip checked: 1080x1920 h264/aac, duration range, titles, scores, caption style, no Devanagari in Hi |
| PASS | Make 132s English video: mode=fast, accurate=accurate, language=hinglish, style=clean, layout=fill | full run, tests/out/run_make.log (every clip checked: 1080x1920 h264/aac, duration range, titles, scores, caption style, no Devanagari in Hi |
| PASS | Make 132s English video: mode=deep, accurate=fast, language=hi, style=hormozi, layout=circle | full run, tests/out/run_make.log (every clip checked: 1080x1920 h264/aac, duration range, titles, scores, caption style, no Devanagari in Hi |
| PASS | Make 132s English video: mode=fast, accurate=fast, language=en, style=mrbeast, layout=side | full run, tests/out/run_make.log (every clip checked: 1080x1920 h264/aac, duration range, titles, scores, caption style, no Devanagari in Hi |
| PASS | Make 13-min English (audio-first path), default Fast | full run, tests/out/run_make.log (every clip checked: 1080x1920 h264/aac, duration range, titles, scores, caption style, no Devanagari in Hi |
| PASS | Make 2-hour Hindi video, Fast, Hinglish captions | full run, tests/out/run_make.log (every clip checked: 1080x1920 h264/aac, duration range, titles, scores, caption style, no Devanagari in Hi |
| PASS | Make 2-hour Hindi video, Accurate (turbo), Hinglish captions | full run, tests/out/run_make.log (every clip checked: 1080x1920 h264/aac, duration range, titles, scores, caption style, no Devanagari in Hi |
| PASS | Make 90-s music trailer (no speech) still returns clips | full run, tests/out/run_make.log (every clip checked: 1080x1920 h264/aac, duration range, titles, scores, caption style, no Devanagari in Hi |
| PASS | Make from an uploaded/local file | full run, tests/out/run_make.log (every clip checked: 1080x1920 h264/aac, duration range, titles, scores, caption style, no Devanagari in Hi |
| PASS | Make from a Twitch VOD | full run, tests/out/run_make.log (every clip checked: 1080x1920 h264/aac, duration range, titles, scores, caption style, no Devanagari in Hi |
| PASS | Make count=1 short range 10-20 s | full run, tests/out/run_make.log (every clip checked: 1080x1920 h264/aac, duration range, titles, scores, caption style, no Devanagari in Hi |
| PASS | Make count=6 on a short video returns what exists | full run, tests/out/run_make.log (every clip checked: 1080x1920 h264/aac, duration range, titles, scores, caption style, no Devanagari in Hi |

## Live clipping on a real stream  (17/17)

| Result | Check | Evidence |
|---|---|---|
| PASS | clip-now on unknown session -> 404 |  |
| PASS | start live clipping | {'live': '01117990e8704f8eac77bf8cbb15ed0d'} |
| PASS | second start while running is refused with a clear message | {'detail': 'A live session is already running. Stop it first.'} |
| PASS | /live-active returns the running session |  |
| PASS | recording starts and elapsed time counts up | {'status': 'recording', 'elapsed': 20, 'stage': 'Recording and watching chat'} |
| PASS | chat reader connected (read-only) | connected (read-only) |
| PASS | chat messages are being counted (>0 in the last windows) | chat_now=13 baseline=0.4 |
| PASS | Clip now accepted | 200 |
| PASS | live clip is produced without error | {'cut': 4.6, 'captions': 8.1, 'score': 0.7, 'render': 8.1} |
| PASS | live clip is 1080x1920 h264/aac, about 30 s | {'w': 1080, 'h': 1920, 'vcodec': 'h264', 'acodec': 'aac', 'dur': 30.004667} |
| PASS | live clip has title, viral score and axes | {'title': 'Hot Take Shower Time with Lee', 'viral': 55, 'axes': {'energy': 75, 'action': None, 'words': 14, 'ai': 80, 'chat': None}} |
| PASS | live clip is editable (edit panel data) | 200 |
| PASS | live clip can be re-edited (style -> bold) |  |
| PASS | live clip appears in My clips exactly once | 1 |
| PASS | stop ends the session | stopped |
| PASS | /live-active is empty after stop |  |
| PASS | start works again after stop | {'live': 'd93371cbe55d461ab65524861e7f8edb'} |

## Creator list  (21/21)

| Result | Check | Evidence |
|---|---|---|
| PASS | parse "kaicenat" | {'platform': 'twitch', 'ref': 'kaicenat', 'url': 'https://twitch.tv/kaicenat', 'name': 'kaicenat'} |
| PASS | parse "https://www.twitch.tv/xQc" | {'platform': 'twitch', 'ref': 'xqc', 'url': 'https://twitch.tv/xqc', 'name': 'xqc'} |
| PASS | parse "@pokimane" | {'platform': 'twitch', 'ref': 'pokimane', 'url': 'https://twitch.tv/pokimane', 'name': 'pokimane'} |
| PASS | parse "youtube.com/@IShowSpeed" | {'platform': 'youtube', 'ref': '@IShowSpeed', 'url': 'https://www.youtube.com/@IShowSpeed', 'name': 'IShowSpeed'} |
| PASS | parse "https://www.youtube.com/channel/UCWsDFcI" | {'platform': 'youtube', 'ref': 'channel/UCWsDFcIhY2DBi3GB5uykGXA', 'url': 'https://www.youtube.com/channel/UCWsDFcIhY2DBi3GB5uykGXA', 'name' |
| PASS | reject "" | rejected |
| PASS | reject "ab" | rejected |
| PASS | reject "https://youtu.be/abc" | rejected |
| PASS | reject "hello world" | rejected |
| PASS | reject "xxxxxxxxxxxxxxxxxxxx" | rejected |
| PASS | add offline creator | {'id': '42e448771b08'} |
| PASS | duplicate add rejected |  |
| PASS | bad add rejected |  |
| PASS | check now reports offline/online | {'live': False} |
| PASS | auto toggle off/on persists |  |
| PASS | save layout |  |
| PASS | library not broken by creators store (no .json in data) |  |
| PASS | remove |  |
| PASS | unknown creator -> 404 |  |
| PASS | detect live Twitch channel (any of 5 big ones) | ['kaicenat'] |
| PASS | offline/nonexistent channel -> not live, no crash |  |

## Star ratings and learning  (6/6)

| Result | Check | Evidence |
|---|---|---|
| PASS | summary readable | {'ratings': 2, 'weights': {'loud': 0.17, 'shout': 0.13, 'words': 0.2, 'motion': 0.17, 'flash': 0.08, 'strobe': 0.04, 'cuts': 0.03, 'llm': 0. |
| PASS | rating 5 accepted | {'ratings': 3, 'weights': {'loud': 0.17, 'shout': 0.13, 'words': 0.2, 'motion': 0.17, 'flash': 0.08, 'strobe': 0.04, 'cuts': 0.03, 'llm': 0. |
| PASS | rating 0 / 6 / text rejected |  |
| PASS | unknown clip rejected |  |
| PASS | after 10 ratings the weights are fitted | {'ratings': 12, 'fitted': True, 'alpha': 0.2} |
| PASS | weights sum to 1 and stay positive | 1.0 |

## Browser UI  (14/14)

| Result | Check | Evidence |
|---|---|---|
| PASS | 4 presets each become active when clicked | checked in the browser pane (30 in-page assertions, 0 failed) |
| PASS | all 5 caption-style buttons become active | checked in the browser pane (30 in-page assertions, 0 failed) |
| PASS | 11 layout cards render and all are clickable | checked in the browser pane (30 in-page assertions, 0 failed) |
| PASS | default caption accuracy is Fast | checked in the browser pane (30 in-page assertions, 0 failed) |
| PASS | default mode is Fast | checked in the browser pane (30 in-page assertions, 0 failed) |
| PASS | every accuracy option selectable (fast/accurate/best) | checked in the browser pane (30 in-page assertions, 0 failed) |
| PASS | every language option selectable (auto/en/hi/hinglish) | checked in the browser pane (30 in-page assertions, 0 failed) |
| PASS | Editor / My clips views both open | checked in the browser pane (30 in-page assertions, 0 failed) |
| PASS | safe-zone toggle on/off | checked in the browser pane (30 in-page assertions, 0 failed) |
| PASS | Creators and Live panels present | checked in the browser pane (30 in-page assertions, 0 failed) |
| PASS | page loads with no JS errors (only stale ERR_CONNECTION_REFUSED from a server restart) | checked in the browser pane (30 in-page assertions, 0 failed) |
| PASS | My clips with 108 clips defers video loading (only ~6 near the screen requested metadata) | 102 deferred, first visible clip playable (readyState 4) |
| PASS | Creators: add offline creator, row, status chip, feed, remove | seen in the browser pane (xqc), screenshot checked |
| PASS | Edit stale card -> newest clip; Apply to all 4 clips; both cards follow | 28.5 s, library 4/4 updated |

## One-click installer  (3/3)

| Result | Check | Evidence |
|---|---|---|
| PASS | install.ps1 into an empty folder from local source (-Yes -SkipOptional -NoShortcut -NoStart) | exit 0, 78 s, "imports ok" |
| PASS | installed copy starts via Start-NeonClipping.bat on port 8791 | /healthz, /library, / (12 KB), /layouts (11) all OK; stopped cleanly |
| PASS | install.ps1 is ASCII only and parses with the PowerShell parser | 13 KB, 0 parse errors |

## Unit tests  (1/1)

| Result | Check | Evidence |
|---|---|---|
| PASS | 14 unit tests: chat-spike rule, target parsing, caption grouping (500 random streams), re-edit | python -m unittest tests.test_live tests.test_captions tests.test_reedit -> OK |

## Website, links, release, editorsgurukul  (39/39)

| Result | Check | Evidence |
|---|---|---|
| PASS | https://iamajmeena.github.io/neonclipping/ loads | 200 18586 bytes |
| PASS | https://iamajmeena.github.io/neonclipping/ has title, download button, demo video |  |
| PASS | link https://github.com/iamajmeena/neonclipping | 200 |
| PASS | link https://github.com/iamajmeena/neonclipping/releases/latest/download/NeonClipping-Setup.bat | 200 |
| PASS | link https://iamajmeena.github.io/neonclipping/NEONCLIPPING-AGENT-SETUP-PROMPT.txt | 200 |
| PASS | link https://iamajmeena.github.io/neonclipping/NeonClipping-Guide-EN-HI.pdf | 200 |
| PASS | link https://iamajmeena.github.io/neonclipping/demo-poster.jpg | 200 |
| PASS | link https://iamajmeena.github.io/neonclipping/demo.mp4 | 200 |
| PASS | link https://iamajmeena.github.io/neonclipping/neonclipping-ui.jpg | 200 |
| PASS | link https://rzp.io/rzp/JN41CpW | 200 |
| PASS | https://iamajmeena.github.io/neonclipping/ no leftover github.io / edtrust names |  |
| PASS | https://editorsgurukul.com/neonclipping/ loads | 200 19021 bytes |
| PASS | https://editorsgurukul.com/neonclipping/ has title, download button, demo video |  |
| PASS | link https://editorsgurukul.com/ | 200 |
| PASS | link https://editorsgurukul.com/neonclipping/NEONCLIPPING-AGENT-SETUP-PROMPT.txt | 200 |
| PASS | link https://editorsgurukul.com/neonclipping/NeonClipping-Guide-EN-HI.pdf | 200 |
| PASS | link https://editorsgurukul.com/neonclipping/demo-poster.jpg | 200 |
| PASS | link https://editorsgurukul.com/neonclipping/demo.mp4 | 200 |
| PASS | link https://editorsgurukul.com/neonclipping/neonclipping-ui.jpg | 200 |
| PASS | link https://github.com/iamajmeena/neonclipping | 200 |
| PASS | link https://github.com/iamajmeena/neonclipping/releases/latest/download/NeonClipping-Setup.bat | 200 |
| PASS | link https://rzp.io/rzp/JN41CpW | 200 |
| PASS | link https://static.cloudflareinsights.com/beacon.min.js/vce701823e78c4301a35b7e07294d873017920 | 200 |
| PASS | https://editorsgurukul.com/neonclipping/ no leftover github.io / edtrust names |  |
| PASS | both site copies carry the same content (only the back link and line endings differ) | 18519 vs 18953 bytes |
| PASS | release asset NeonClipping-Setup.bat | ['NEONCLIPPING-AGENT-SETUP-PROMPT.txt', 'NeonClipping-Guide-EN-HI.pdf', 'NeonClipping-Setup.bat', 'install.ps1', 'install.sh'] |
| PASS | release asset install.ps1 | ['NEONCLIPPING-AGENT-SETUP-PROMPT.txt', 'NeonClipping-Guide-EN-HI.pdf', 'NeonClipping-Setup.bat', 'install.ps1', 'install.sh'] |
| PASS | release asset install.sh | ['NEONCLIPPING-AGENT-SETUP-PROMPT.txt', 'NeonClipping-Guide-EN-HI.pdf', 'NeonClipping-Setup.bat', 'install.ps1', 'install.sh'] |
| PASS | release asset NeonClipping-Guide-EN-HI.pdf | ['NEONCLIPPING-AGENT-SETUP-PROMPT.txt', 'NeonClipping-Guide-EN-HI.pdf', 'NeonClipping-Setup.bat', 'install.ps1', 'install.sh'] |
| PASS | release asset NEONCLIPPING-AGENT-SETUP-PROMPT.txt | ['NEONCLIPPING-AGENT-SETUP-PROMPT.txt', 'NeonClipping-Guide-EN-HI.pdf', 'NeonClipping-Setup.bat', 'install.ps1', 'install.sh'] |
| PASS | one-click download URL resolves | 200 |
| PASS | raw install.ps1 reachable (the .bat downloads it when run alone) | 200 |
| PASS | install.ps1 is ASCII only (no encoding surprises in PowerShell 5.1) |  |
| PASS | guide PDF is a PDF with pages | 963080 |
| PASS | agent prompt has the 9 steps + simple-Hindi explanation + stop rules | 8091 |
| PASS | https://editorsgurukul.com/free-resources lists NeonClipping | 200 |
| PASS | https://editorsgurukul.com/free-websites/ lists NeonClipping | 200 |
| PASS | https://editorsgurukul.com/free-websites/neonclipping/ lists NeonClipping | 200 |
| PASS | sitemap lists /neonclipping/ |  |
