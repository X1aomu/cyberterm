# ᴄʏʙᴇʀᴛᴇʀᴍ

**cyberterm** is a fully fleshed-out 16-color terminal palette, inspired by the excellent [cyberdream.nvim](https://github.com/scottmckendry/cyberdream.nvim) Neovim theme.

While the upstream `cyberdream.nvim` theme is beautiful, its provided terminal configurations typically only define 8 basic colors, which falls short of a complete 16-color ANSI environment.

**cyberterm** bridges this gap by focusing on the color palette itself. It expands the original colors into a complete, harmonious 16-color ANSI palette (both normal and bright variants). For convenience, ready-to-use configurations for several popular terminal emulators are also included out-of-the-box.

## 📸 Screenshots

| Dark Mode | Light Mode |
| :---: | :---: |
| ![cyberterm dark mode](./assets/palette-cyberterm-dark.png) | ![cyberterm light mode](./assets/palette-cyberterm-light.png) |

## ✨ Features

- **Full 16-Color Palette**: Expands the original 8-color terminal config into a complete 16-color ansi palette.
- **Color Philosophy**: The design principle strictly maximizes the use of the original upstream colors to maintain authentic aesthetic harmony. New colors are dynamically generated (e.g., via HSV transformations like hue shifting and maximizing saturation) only to fill the missing or unsuitable slots in the 16-color palette.
- **Cyber-Flavored Cursors**: The cursor colors have been meticulously tweaked to give your terminal a more authentic "cyber" feel.
  - *Dark Mode*: Striking Yellow cursor with Pink text.
  - *Light Mode*: Vibrant Orange cursor with Red text.
- **Dark & Light Variants**: Full support for both dark and light modes.
- **Multi-Terminal Support**: Out-of-the-box configurations for popular terminal emulators.

## 💻 Terminal Configurations

You can find the ready-to-use configuration files for your favorite terminal emulator in the root of this repository:

- **Alacritty**: [Dark](./cyberterm-dark-alacritty.toml) / [Light](./cyberterm-light-alacritty.toml)
- **Kitty**: [Dark](./cyberterm-dark-kitty.conf) / [Light](./cyberterm-light-kitty.conf)
- **Konsole**: [Dark](./cyberterm-dark-konsole.colorscheme) / [Light](./cyberterm-light-konsole.colorscheme)
- **Windows Terminal**: [Dark](./cyberterm-dark-wt.json) / [Light](./cyberterm-light-wt.json)

*(Missing your favorite terminal? PRs to add new configurations are always welcome!)*

## 🎨 Palette

### 🌙 Dark Mode

#### ANSI Colors

| Color | Normal | Bright |
| :--- | :--- | :--- |
| **Black** | ![](https://placehold.co/20x20/1e2124/1e2124.png) `#1e2124` | ![](https://placehold.co/20x20/7b8496/7b8496.png) `#7b8496` |
| **Red** | ![](https://placehold.co/20x20/ff6e5e/ff6e5e.png) `#ff6e5e` | ![](https://placehold.co/20x20/ff5ea0/ff5ea0.png) `#ff5ea0` |
| **Green** | ![](https://placehold.co/20x20/5eff6c/5eff6c.png) `#5eff6c` | ![](https://placehold.co/20x20/14ff00/14ff00.png) `#14ff00` |
| **Yellow** | ![](https://placehold.co/20x20/ffbd5e/ffbd5e.png) `#ffbd5e` | ![](https://placehold.co/20x20/f1ff5e/f1ff5e.png) `#f1ff5e` |
| **Blue** | ![](https://placehold.co/20x20/5ea1ff/5ea1ff.png) `#5ea1ff` | ![](https://placehold.co/20x20/0095ff/0095ff.png) `#0095ff` |
| **Magenta** | ![](https://placehold.co/20x20/bd5eff/bd5eff.png) `#bd5eff` | ![](https://placehold.co/20x20/ff5ef1/ff5ef1.png) `#ff5ef1` |
| **Cyan** | ![](https://placehold.co/20x20/5ef1ff/5ef1ff.png) `#5ef1ff` | ![](https://placehold.co/20x20/00ffeb/00ffeb.png) `#00ffeb` |
| **White** | ![](https://placehold.co/20x20/acacac/acacac.png) `#acacac` | ![](https://placehold.co/20x20/ffffff/ffffff.png) `#ffffff` |

#### Terminal Colors

| Element | Color |
| :--- | :--- |
| **Background** | ![](https://placehold.co/20x20/16181a/16181a.png) `#16181a` |
| **Foreground** | ![](https://placehold.co/20x20/eaeaea/eaeaea.png) `#eaeaea` |
| **Bright Background** | ![](https://placehold.co/20x20/3c4048/3c4048.png) `#3c4048` |
| **Bright Foreground** | ![](https://placehold.co/20x20/ffffff/ffffff.png) `#ffffff` |
| **Selection Background** | ![](https://placehold.co/20x20/3c4048/3c4048.png) `#3c4048` |
| **Cursor Background** | ![](https://placehold.co/20x20/f1ff5e/f1ff5e.png) `#f1ff5e` |
| **Cursor Text** | ![](https://placehold.co/20x20/ff5ea0/ff5ea0.png) `#ff5ea0` |

### ☀️ Light Mode

#### ANSI Colors

| Color | Normal | Bright |
| :--- | :--- | :--- |
| **Black** | ![](https://placehold.co/20x20/eaeaea/eaeaea.png) `#eaeaea` | ![](https://placehold.co/20x20/7b8496/7b8496.png) `#7b8496` |
| **Red** | ![](https://placehold.co/20x20/d11500/d11500.png) `#d11500` | ![](https://placehold.co/20x20/f40064/f40064.png) `#f40064` |
| **Green** | ![](https://placehold.co/20x20/008b0c/008b0c.png) `#008b0c` | ![](https://placehold.co/20x20/008b23/008b23.png) `#008b23` |
| **Yellow** | ![](https://placehold.co/20x20/d17c00/d17c00.png) `#d17c00` | ![](https://placehold.co/20x20/997b00/997b00.png) `#997b00` |
| **Blue** | ![](https://placehold.co/20x20/0057d1/0057d1.png) `#0057d1` | ![](https://placehold.co/20x20/0034d1/0034d1.png) `#0034d1` |
| **Magenta** | ![](https://placehold.co/20x20/a018ff/a018ff.png) `#a018ff` | ![](https://placehold.co/20x20/d100bf/d100bf.png) `#d100bf` |
| **Cyan** | ![](https://placehold.co/20x20/008c99/008c99.png) `#008c99` | ![](https://placehold.co/20x20/007399/007399.png) `#007399` |
| **White** | ![](https://placehold.co/20x20/3c4048/3c4048.png) `#3c4048` | ![](https://placehold.co/20x20/16181a/16181a.png) `#16181a` |

#### Terminal Colors

| Element | Color |
| :--- | :--- |
| **Background** | ![](https://placehold.co/20x20/ffffff/ffffff.png) `#ffffff` |
| **Foreground** | ![](https://placehold.co/20x20/1e2124/1e2124.png) `#1e2124` |
| **Bright Background** | ![](https://placehold.co/20x20/acacac/acacac.png) `#acacac` |
| **Bright Foreground** | ![](https://placehold.co/20x20/16181a/16181a.png) `#16181a` |
| **Selection Background** | ![](https://placehold.co/20x20/acacac/acacac.png) `#acacac` |
| **Cursor Background** | ![](https://placehold.co/20x20/d17c00/d17c00.png) `#d17c00` |
| **Cursor Text** | ![](https://placehold.co/20x20/d11500/d11500.png) `#d11500` |

## 🪄 How It Works

The magic behind the color palette generation is defined in [`spec.yml`](./spec.yml). You can inspect this file to see exactly how the base colors from `cyberdream` are mapped and how the missing colors are generated via color space transformations (`rgb-to-hsv` -> `hue shift` -> `sat-set-max` -> `hsv-to-rgb`).

The repository also includes a `show_colors.py` script, which is used to preview and process these colors.

## 📜 License

This project is open-source and free to use. See the [LICENSE](LICENSE) file for details. Enjoy your new cyberpunk terminal experience!
