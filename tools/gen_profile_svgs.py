"""Generate the org-profile SVGs (dark + light) into profile/assets/."""
import base64
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "profile", "assets")
MARK = base64.b64encode(open(os.path.join(os.path.dirname(__file__), "mark.png"), "rb").read()).decode()

SANS = "ui-sans-serif, -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace"

THEMES = {
    "dark": dict(bg="#101112", card="#171a1c", line="#262a2d", grid="rgba(232,230,225,0.045)",
                 ink="#e8e6e1", ink2="#c4c2bc", mute="#918f8a", acc="#6063ea", acc2="#9ba0ff",
                 glow="#6063ea", live="#ef4444", ok="#3fb950"),
    "light": dict(bg="#f7f4ee", card="#fbf9f5", line="#e2ddd2", grid="rgba(27,28,29,0.05)",
                  ink="#1b1c1d", ink2="#3d3e40", mute="#6b6a66", acc="#4348c8", acc2="#5457e0",
                  glow="#9ba0ff", live="#dc2626", ok="#1a7f37"),
}

STYLE = """<style>
  .sans{font-family:%(sans)s}
  .mono{font-family:%(mono)s}
  @media (prefers-reduced-motion: reduce){ *{animation:none!important} }
</style>""" % dict(sans=SANS, mono=MONO)


def grid(w, h, t, step=40):
    lines = [f'<path d="M{x} 0V{h}" />' for x in range(step, w, step)]
    lines += [f'<path d="M0 {y}H{w}" />' for y in range(step, h, step)]
    return f'<g stroke="{t["grid"]}" stroke-width="1">{"".join(lines)}</g>'


def digit_column(x, y, cycle_s, n, t, size=26, step_s=1):
    """A clipped column of digits 0..n-1 that ticks one step per `step_s` seconds."""
    lh = size * 1.25
    digits = "".join(f'<tspan x="{x}" dy="{lh if i else 0}">{i}</tspan>' for i in range(n))
    values = ";".join(f"0 {-i * lh:.2f}" for i in range(n))
    return f'''<g clip-path="url(#dclip{x})">
      <g><text x="{x}" y="{y}" class="mono" font-size="{size}" font-weight="600" fill="{t["ink"]}">{digits}</text>
      <animateTransform attributeName="transform" type="translate" values="{values}" dur="{cycle_s}s" calcMode="discrete" repeatCount="indefinite"/></g>
    </g>'''


def banner(t):
    W, H = 1280, 420
    lem = "M1000 235 C 1060 165, 1140 165, 1140 235 C 1140 305, 1060 305, 1000 235 C 940 165, 860 165, 860 235 C 860 305, 940 305, 1000 235 Z"
    chips = ""
    for i, name in enumerate(["YouTube", "Twitch", "Kick"]):
        cx = 860 + i * 104
        bars = ""
        for j in range(3):
            bx = cx + 76 + j * 5
            bh = 5 + j * 3
            bars += (f'<rect x="{bx}" y="{356 - bh}" width="3" height="{bh}" rx="1" fill="{t["ok"]}">'
                     f'<animate attributeName="opacity" values="1;0.35;1" dur="1.6s" begin="{(i * 3 + j) * 0.17:.2f}s" repeatCount="indefinite"/></rect>')
        chips += (f'<rect x="{cx}" y="336" width="96" height="28" rx="14" fill="none" stroke="{t["line"]}"/>'
                  f'<text x="{cx + 14}" y="355" class="sans" font-size="13" fill="{t["ink2"]}">{name}</text>{bars}')

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="TheLoops: pre-recorded video, live around the clock">
{STYLE}
<defs>
  <radialGradient id="glow" cx="78%" cy="45%" r="45%"><stop offset="0" stop-color="{t["glow"]}" stop-opacity="0.28"/><stop offset="1" stop-color="{t["glow"]}" stop-opacity="0"/></radialGradient>
  <linearGradient id="hl" x1="0" x2="1"><stop offset="0" stop-color="{t["acc"]}"/><stop offset="1" stop-color="{t["acc2"]}"/></linearGradient>
  <clipPath id="dclip1092"><rect x="1091" y="98" width="17" height="32"/></clipPath>
  <clipPath id="dclip1108"><rect x="1107" y="98" width="17" height="32"/></clipPath>
  <filter id="soft" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="6"/></filter>
</defs>
<rect width="{W}" height="{H}" rx="20" fill="{t["bg"]}"/>
{grid(W, H, t)}
<rect width="{W}" height="{H}" rx="20" fill="url(#glow)"/>

<image x="72" y="62" width="54" height="35" href="data:image/png;base64,{MARK}"/>
<text x="140" y="86" class="mono" font-size="14" letter-spacing="3" fill="{t["acc2"]}">THELOOPS · 24/7 LIVE STREAMING</text>
<text x="72" y="170" class="sans" font-size="54" font-weight="700" fill="{t["ink"]}">Pre-recorded video,</text>
<text x="72" y="232" class="sans" font-size="54" font-weight="700" fill="url(#hl)">live around the clock.</text>
<text x="72" y="284" class="sans" font-size="19" fill="{t["ink2"]}">Upload a video or a playlist. It streams to YouTube, Twitch, Kick</text>
<text x="72" y="312" class="sans" font-size="19" fill="{t["ink2"]}">and any RTMP server, with no PC left running.</text>
<rect x="72" y="340" width="176" height="36" rx="18" fill="{t["acc"]}"/>
<text x="92" y="364" class="mono" font-size="15" font-weight="600" fill="#ffffff">theloops.live →</text>

<rect x="824" y="62" width="384" height="320" rx="16" fill="{t["card"]}" stroke="{t["line"]}"/>
<rect x="848" y="88" width="70" height="26" rx="13" fill="{t["live"]}" fill-opacity="0.14"/>
<circle cx="864" cy="101" r="5" fill="{t["live"]}"><animate attributeName="opacity" values="1;0.25;1" dur="1.4s" repeatCount="indefinite"/></circle>
<text x="876" y="106" class="mono" font-size="13" font-weight="700" fill="{t["live"]}">LIVE</text>
<text x="848" y="140" class="mono" font-size="12" letter-spacing="2" fill="{t["mute"]}">ON AIR</text>
<text x="934" y="122" class="mono" font-size="26" font-weight="600" fill="{t["ink"]}">44d 18:32:</text>
{digit_column(1092, 122, 60, 6, t)}
{digit_column(1108, 122, 10, 10, t)}

<path d="{lem}" fill="none" stroke="{t["line"]}" stroke-width="10" stroke-linecap="round"/>
<path d="{lem}" fill="none" stroke="{t["acc"]}" stroke-width="3" stroke-opacity="0.55" stroke-dasharray="4 10">
  <animate attributeName="stroke-dashoffset" values="0;-140" dur="4s" repeatCount="indefinite"/></path>
<g><circle r="12" fill="{t["acc2"]}" filter="url(#soft)" opacity="0.9"/><circle r="6" fill="{t["acc2"]}"/>
  <animateMotion dur="6s" repeatCount="indefinite" path="{lem}"/></g>
<text x="1016" y="320" class="mono" font-size="12" letter-spacing="2" fill="{t["mute"]}" text-anchor="middle">PLAYLIST · ON LOOP</text>
{chips}
</svg>'''


def flow(t):
    W, H = 1280, 300
    dests = ["YouTube", "Twitch", "Kick", "Facebook", "any RTMP"]
    hub = (640, 150)
    out = []
    for i, d in enumerate(dests):
        y = 62 + i * 50
        p = f"M{hub[0] + 92} {hub[1]} C 880 {hub[1]}, 900 {y}, 1010 {y}"
        out.append(f'<path id="d{i}" d="{p}" fill="none" stroke="{t["line"]}" stroke-width="2"/>')
        out.append(f'<path d="{p}" fill="none" stroke="{t["acc"]}" stroke-width="2" stroke-dasharray="6 8">'
                   f'<animate attributeName="stroke-dashoffset" values="0;-28" dur="1.2s" repeatCount="indefinite"/></path>')
        out.append(f'<circle r="4" fill="{t["acc2"]}"><animateMotion dur="2.4s" begin="-{i * 0.45 + 0.1:.2f}s" repeatCount="indefinite" path="{p}"/></circle>')
        out.append(f'<rect x="1010" y="{y - 17}" width="200" height="34" rx="17" fill="{t["card"]}" stroke="{t["line"]}"/>')
        out.append(f'<circle cx="1032" cy="{y}" r="4.5" fill="{t["ok"]}"><animate attributeName="opacity" values="1;0.3;1" dur="1.8s" begin="{i * 0.3:.1f}s" repeatCount="indefinite"/></circle>')
        out.append(f'<text x="1048" y="{y + 5}" class="sans" font-size="15" fill="{t["ink"]}">{d}</text>')
    src = "M330 150 C 420 150, 460 150, 548 150"
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="How TheLoops works: upload, loop 24/7, stream to every platform at once">
{STYLE}
<rect width="{W}" height="{H}" rx="20" fill="{t["bg"]}"/>
{grid(W, H, t)}
<text x="72" y="44" class="mono" font-size="12" letter-spacing="2.5" fill="{t["acc2"]}">01 · UPLOAD</text>
<g transform="translate(96 82)">
  <rect x="24" y="-6" width="150" height="104" rx="12" fill="{t["card"]}" stroke="{t["line"]}" opacity="0.6"/>
  <rect x="12" y="6" width="150" height="104" rx="12" fill="{t["card"]}" stroke="{t["line"]}" opacity="0.8"/>
  <rect x="0" y="18" width="150" height="104" rx="12" fill="{t["card"]}" stroke="{t["line"]}"/>
  <path d="M62 52 L62 88 L92 70 Z" fill="{t["acc"]}"/>
  <text x="0" y="150" class="mono" font-size="14" fill="{t["ink2"]}">video.mp4 · playlist</text>
</g>
<path d="{src}" fill="none" stroke="{t["line"]}" stroke-width="2"/>
<path d="{src}" fill="none" stroke="{t["acc"]}" stroke-width="2" stroke-dasharray="6 8"><animate attributeName="stroke-dashoffset" values="0;-28" dur="1.2s" repeatCount="indefinite"/></path>
<circle r="4" fill="{t["acc2"]}"><animateMotion dur="1.6s" repeatCount="indefinite" path="{src}"/></circle>
<text x="560" y="44" class="mono" font-size="12" letter-spacing="2.5" fill="{t["acc2"]}">02 · LOOPED 24/7</text>
<circle cx="{hub[0]}" cy="{hub[1]}" r="92" fill="{t["card"]}" stroke="{t["line"]}"/>
<circle cx="{hub[0]}" cy="{hub[1]}" r="92" fill="none" stroke="{t["acc"]}" stroke-width="3" stroke-dasharray="40 538" stroke-linecap="round">
  <animateTransform attributeName="transform" type="rotate" values="0 {hub[0]} {hub[1]};360 {hub[0]} {hub[1]}" dur="5s" repeatCount="indefinite"/></circle>
<image x="{hub[0] - 46}" y="{hub[1] - 44}" width="92" height="60" href="data:image/png;base64,{MARK}"/>
<text x="{hub[0]}" y="{hub[1] + 46}" class="mono" font-size="13" fill="{t["ink2"]}" text-anchor="middle">cloud, no PC on</text>
<text x="1010" y="30" class="mono" font-size="12" letter-spacing="2.5" fill="{t["acc2"]}">03 · EVERY PLATFORM</text>
{"".join(out)}
</svg>'''


def stats(t):
    W, H = 1280, 190
    cells = [
        ("44,000 h", "of 24/7 streams in our", "open dataset (CC BY)"),
        ("68%", "of airtime is a single", "video on loop"),
        ("44.8 days", "longest single session", "on air without a stop"),
        ("99.95%", "measured uptime, with", "every gap counted"),
    ]
    cw = (W - 144) / 4
    body = ""
    for i, (big, a, b) in enumerate(cells):
        x = 72 + i * cw
        if i:
            body += f'<path d="M{x - 18:.0f} 52V150" stroke="{t["line"]}"/>'
        body += (f'<text x="{x:.0f}" y="96" class="sans" font-size="40" font-weight="700" fill="{t["ink"]}">{big}</text>'
                 f'<text x="{x:.0f}" y="128" class="sans" font-size="15" fill="{t["ink2"]}">{a}</text>'
                 f'<text x="{x:.0f}" y="149" class="sans" font-size="15" fill="{t["ink2"]}">{b}</text>'
                 f'<rect x="{x:.0f}" y="44" width="28" height="3" rx="1.5" fill="{t["acc"]}"/>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="From our open dataset: 44,000 hours of 24/7 streams; 68% of airtime is one video on loop; longest session 44.8 days; 99.95% measured uptime">
{STYLE}
<rect width="{W}" height="{H}" rx="20" fill="{t["bg"]}"/>
{grid(W, H, t)}
<text x="72" y="30" class="mono" font-size="12" letter-spacing="2.5" fill="{t["acc2"]}">FROM OUR OPEN DATA · SEP–OCT 2026</text>
{body}
</svg>'''


def card(t, name, line1, line2, cmd, tag):
    W, H = 620, 230
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{name}: {line1} {line2}">
{STYLE}
<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="16" fill="{t["card"]}" stroke="{t["line"]}"/>
<text x="28" y="44" class="mono" font-size="12" letter-spacing="2" fill="{t["acc2"]}">{tag}</text>
<text x="28" y="82" class="sans" font-size="26" font-weight="700" fill="{t["ink"]}">{name}</text>
<text x="28" y="114" class="sans" font-size="15" fill="{t["ink2"]}">{line1}</text>
<text x="28" y="136" class="sans" font-size="15" fill="{t["ink2"]}">{line2}</text>
<rect x="28" y="160" width="{W - 56}" height="44" rx="10" fill="{t["bg"]}" stroke="{t["line"]}"/>
<text x="46" y="188" class="mono" font-size="14" fill="{t["ink"]}"><tspan fill="{t["acc2"]}">$</tspan> {cmd}</text>
<rect x="{48 + 8.7 * (len(cmd) + 2):.0f}" y="174" width="9" height="18" fill="{t["acc2"]}"><animate attributeName="opacity" values="1;1;0;0" dur="1.1s" repeatCount="indefinite"/></rect>
</svg>'''


os.makedirs(OUT, exist_ok=True)
for mode, t in THEMES.items():
    files = {
        f"banner-{mode}.svg": banner(t),
        f"flow-{mode}.svg": flow(t),
        f"stats-{mode}.svg": stats(t),
        f"card-jwt-{mode}.svg": card(t, "channels-jwt-subprotocol", "JWT auth for Django Channels WebSockets,",
                                    "without the token in the URL or access logs.", "pip install channels-jwt-subprotocol",
                                    "PYTHON · DJANGO · PYPI"),
        f"card-tee-{mode}.svg": card(t, "ffmpeg-tee-builder", "FFmpeg -f tee for many RTMP servers at once:",
                                    "one dead destination can't stop the others.", "ffmpeg-tee-builder rtmp://a/KEY rtmp://b/KEY",
                                    "PYTHON · FFMPEG · CLI"),
    }
    for name, svg in files.items():
        open(os.path.join(OUT, name), "w").write(svg)
        print(name, len(svg) // 1024, "KB")
