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

def fg(r: int, g: int, b: int) -> str:
    return f"\033[38;2;{r};{g};{b}m"

def block(r: int, g: int, b: int) -> str:
    """Pure colored block, no text overlay."""
    return f"{bg(r, g, b)}{' ' * BLOCK_W}{RESET}"

def colored_hex(hex_str: str, fg_rgb: tuple, bg_rgb: tuple) -> str:
    """Hex value in fg color on bg color. Exactly 9 visible chars."""
    return f"{bg(*bg_rgb)}{fg(*fg_rgb)} {hex_str} {RESET}"

def text_on_bg(text: str, fg_rgb: tuple, bg_rgb: tuple, width: int) -> str:
    """Render text in fg color on bg background, padded to width visible chars."""
    inner = f" {text} "
    pad = width - len(inner)
    left, right = pad // 2, pad - pad // 2
    return f"{bg(*bg_rgb)}{fg(*fg_rgb)}{' ' * left}{inner}{' ' * right}{RESET}"

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

def ansi_pair(left_name: str, left_hex: str, left_rgb: tuple,
              right_name: str, right_hex: str, right_rgb: tuple,
              term_bg_rgb: tuple) -> None:
    """ANSI row with hex colored on terminal background."""
    lh = colored_hex(left_hex, left_rgb, term_bg_rgb)
    rh = colored_hex(right_hex, right_rgb, term_bg_rgb)
    lb = block(*left_rgb)
    rb = block(*right_rgb)
    print(f"  {left_name:<{NAME_W}} {lh} {lb}"
          f"{GAP}"
          f"{right_name:<{NAME_W}} {rh} {rb}")

def single(name: str, hex_str: str, rgb: tuple) -> None:
    print(f"  {name:<{NAME_W}} {hex_str:<{HEX_W}} {block(*rgb)}")

def term_pair(label: str, bg_rgb: tuple, fg_rgb: tuple,
              bg_hex: str, fg_hex: str, label_w: int) -> None:
    """Terminal fg/bg pair — demo text on colored background."""
    demo = text_on_bg("Sample", fg_rgb, bg_rgb, BLOCK_W + 6)
    print(f"  {label:<{label_w}} {demo}  {fg_hex} on {bg_hex}")

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
        elif step == "hue-add-10-degree":
            h = (h + 10) % 360
        elif step == "sat-set-max":
            s = 1.0
        elif step == "hsv-to-rgb":
            r, g, b = hsv_to_rgb(h, s, v)
    return r, g, b

# ---------- palette display ----------

NORMAL_NAMES = ["black", "red", "green", "yellow", "blue", "magenta", "cyan", "white"]
TERM_PAIRS = [
    ("background", "foreground"),
    ("bright-background", "bright-foreground"),
    ("cursor-background", "cursor-text"),
]

def display_palette(palette_data: dict) -> None:
    name = palette_data["name"]
    ansi = palette_data["ansi"]
    term = palette_data["terminal"]

    section(f"palette: {name}")

    # 16-color bar: 2 rows × 8 columns (normal / bright aligned)
    print()
    for label, prefix in [("normal", ""), ("bright", "bright-")]:
        print(f"  {label + ':':<9}", end="")
        for cn in NORMAL_NAMES:
            rgb = resolve(ansi[f"{prefix}{cn}"]["color"])
            print(f"{bg(*rgb)}  {RESET}", end="")
        print()

    # table with colored hex on terminal background
    term_bg_rgb = resolve(term["background"]["color"])
    print(f"  {'normal':<{NAME_W}} {'hex':<{HEX_W}} {'color':<{BLOCK_W}}"
          f"{GAP}"
          f"{'bright-*':<{NAME_W}} {'hex':<{HEX_W}} {'color':<{BLOCK_W}}")
    print(f"  {'─' * NAME_W} {'─' * HEX_W} {'─' * BLOCK_W}"
          f"{GAP}"
          f"{'─' * NAME_W} {'─' * HEX_W} {'─' * BLOCK_W}")
    for cn in NORMAL_NAMES:
        bright_name = f"bright-{cn}"
        nrgb = resolve(ansi[cn]["color"])
        nhex = rgb_to_hex(*nrgb)
        brgb = resolve(ansi[bright_name]["color"])
        bhex = rgb_to_hex(*brgb)
        ansi_pair(cn, nhex, nrgb, bright_name, bhex, brgb, term_bg_rgb)

    # terminal pairs + singles
    pair_labels = [f"{bg} + {fg}" for bg, fg in TERM_PAIRS]
    label_w = max(len(l) for l in pair_labels)
    paired_keys = {k for a, b in TERM_PAIRS for k in (a, b)}
    for (bg_key, fg_key), label in zip(TERM_PAIRS, pair_labels):
        bg_rgb = resolve(term[bg_key]["color"])
        fg_rgb = resolve(term[fg_key]["color"])
        bg_hex = rgb_to_hex(*bg_rgb)
        fg_hex = rgb_to_hex(*fg_rgb)
        term_pair(label, bg_rgb, fg_rgb, bg_hex, fg_hex, label_w)
    term_fg_rgb = resolve(term["foreground"]["color"])
    for key in term:
        if key not in paired_keys:
            trgb = resolve(term[key]["color"])
            thex = rgb_to_hex(*trgb)
            demo = text_on_bg("Sample", term_fg_rgb, trgb, BLOCK_W + 6)
            print(f"  {key:<{label_w}} {demo}  {thex}")

# ---------- main ----------

def main() -> None:
    data = yaml.safe_load(open(SPEC))

    upstream = data["upstream-cyberdream"]
    dark = upstream["dark"]
    light = upstream["light"]

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

    # ── palettes ──
    display_palette(data["palette"])
    display_palette(data["palette-light"])

    print()

if __name__ == "__main__":
    main()
