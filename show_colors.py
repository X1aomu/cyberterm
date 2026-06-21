"""Display all colors from spec.yml using true-color (RGB) terminal escape codes."""

from pathlib import Path

import yaml

SPEC = Path(__file__).resolve().parent / "spec.yml"

RESET = "\033[0m"
NAME_W = 22
HEX_W = 9
BLOCK_W = 8
GAP = "  │  "

def hex_to_rgb(h: str) -> tuple[int, int, int]:
    h = h.lstrip("#")
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)

def rgb_to_hex(r: int, g: int, b: int) -> str:
    return f"#{r:02x}{g:02x}{b:02x}"

def bg(r: int, g: int, b: int) -> str:
    return f"\033[48;2;{r};{g};{b}m"

def block(r: int, g: int, b: int) -> str:
    """Pure colored block, no text overlay."""
    return f"{bg(r, g, b)}{' ' * BLOCK_W}{RESET}"

def section(title: str) -> None:
    bar = "─" * (len(title) + 4)
    print(f"\n  {bar}")
    print(f"  {title}")
    print(f"  {bar}")

def pair(left_name: str, left_hex: str, left_rgb: tuple,
         right_name: str, right_hex: str, right_rgb: tuple) -> None:
    print(f"  {left_name:<{NAME_W}} {left_hex:<{HEX_W}} {block(*left_rgb)}"
          f"{GAP}"
          f"{right_name:<{NAME_W}} {right_hex:<{HEX_W}} {block(*right_rgb)}")

def single(name: str, hex_str: str, rgb: tuple) -> None:
    print(f"  {name:<{NAME_W}} {hex_str:<{HEX_W}} {block(*rgb)}")

# ---------- HSV hexagon-model transforms ----------
# Despite the spec naming them "hsi", the hexagon (piecewise-linear)
# HSV model matches the Kitty reference targets exactly.

def rgb_to_hsv(r: int, g: int, b: int) -> tuple[float, float, float]:
    """Hexagon-model HSV: H(deg), S(0-1), V(0-1)."""
    rn, gn, bn = r / 255.0, g / 255.0, b / 255.0
    mx = max(rn, gn, bn)
    mn = min(rn, gn, bn)
    v = mx
    delta = mx - mn
    s = delta / mx if mx > 0 else 0.0
    if delta == 0:
        return 0.0, 0.0, v
    if mx == rn:
        h = 60.0 * (((gn - bn) / delta) % 6)
    elif mx == gn:
        h = 60.0 * (((bn - rn) / delta) + 2)
    else:
        h = 60.0 * (((rn - gn) / delta) + 4)
    return h % 360.0, s, v

def hsv_to_rgb(h: float, s: float, v: float) -> tuple[int, int, int]:
    """Hexagon-model HSV -> RGB (0-255)."""
    h = h % 360.0
    c = v * s
    x = c * (1.0 - abs((h / 60.0) % 2 - 1.0))
    m = v - c
    if h < 60:
        rp, gp, bp = c, x, 0.0
    elif h < 120:
        rp, gp, bp = x, c, 0.0
    elif h < 180:
        rp, gp, bp = 0.0, c, x
    elif h < 240:
        rp, gp, bp = 0.0, x, c
    elif h < 300:
        rp, gp, bp = x, 0.0, c
    else:
        rp, gp, bp = c, 0.0, x
    return (
        round((rp + m) * 255),
        round((gp + m) * 255),
        round((bp + m) * 255),
    )

def resolve(value) -> tuple[int, int, int]:
    if isinstance(value, str):
        return hex_to_rgb(value)
    t = value["transform"]
    r, g, b = hex_to_rgb(t["input"])
    for step in t["steps"]:
        if step == "rgb-to-hsv":
            h, s, v = rgb_to_hsv(r, g, b)
        elif step == "hue-sub-10-degree":
            h = (h - 10) % 360
        elif step == "sat-set-max":
            s = 1.0
        elif step == "hsv-to-rgb":
            r, g, b = hsv_to_rgb(h, s, v)
    return r, g, b

# ---------- main ----------

def main() -> None:
    data = yaml.safe_load(open(SPEC))

    upstream = data["upstream-cyberdream"]
    dark = upstream["dark"]
    light = upstream["light"]
    palette = data["palette"]
    ansi = palette["ansi"]
    term = palette["terminal"]

    dark_colors = [(k, v) for k, v in dark.items()]
    light_colors = [(k, v) for k, v in light.items()]

    # ── banner ──
    edge = "═" * 85
    title = "C Y B E R T E R M   C O L O R   S P E C"
    pad = (85 - len(title)) // 2
    print(f"{RESET}")
    print(f"  ╔{edge}╗")
    print(f"  ║{' ' * pad}{title}{' ' * (85 - pad - len(title))}║")
    print(f"  ╚{edge}╝")

    # ── upstream ──
    section("upstream-cyberdream")
    print(f"  {'dark':<{NAME_W}} {'hex':<{HEX_W}} {'color':<{BLOCK_W}}"
          f"{GAP}"
          f"{'light':<{NAME_W}} {'hex':<{HEX_W}} {'color':<{BLOCK_W}}")
    print(f"  {'─' * NAME_W} {'─' * HEX_W} {'─' * BLOCK_W}"
          f"{GAP}"
          f"{'─' * NAME_W} {'─' * HEX_W} {'─' * BLOCK_W}")
    for (dk, dhex), (lk, lhex) in zip(dark_colors, light_colors):
        drgb, lrgb = hex_to_rgb(dhex), hex_to_rgb(lhex)
        pair(dk, dhex, drgb, lk, lhex, lrgb)

    # ── ansi palette ──
    section("palette / ansi")
    normal_names = ["black", "red", "green", "yellow", "blue", "magenta", "cyan", "white"]
    print(f"  {'normal':<{NAME_W}} {'hex':<{HEX_W}} {'color':<{BLOCK_W}}"
          f"{GAP}"
          f"{'bright-*':<{NAME_W}} {'hex':<{HEX_W}} {'color':<{BLOCK_W}}")
    print(f"  {'─' * NAME_W} {'─' * HEX_W} {'─' * BLOCK_W}"
          f"{GAP}"
          f"{'─' * NAME_W} {'─' * HEX_W} {'─' * BLOCK_W}")
    for name in normal_names:
        bright_name = f"bright-{name}"
        nrgb = resolve(ansi[name]["color"])
        nhex = rgb_to_hex(*nrgb)
        brgb = resolve(ansi[bright_name]["color"])
        bhex = rgb_to_hex(*brgb)
        pair(name, nhex, nrgb, bright_name, bhex, brgb)

    # ── terminal palette ──
    section("palette / terminal")
    for key in term:
        trgb = resolve(term[key]["color"])
        thex = rgb_to_hex(*trgb)
        single(key, thex, trgb)

    print()

if __name__ == "__main__":
    main()
