# dots4qtile

Minimal, opinionated dotfiles centered around Qtile on Arch Linux.

## Contents

- `config/qtile/config.py` Qtile config (keys, groups, layouts, bar/widgets).
- `config/qtile/scripts/calculator.py` Qtile calculator script.
- `config/nvim/init.lua` Neovim entrypoint (loads modular Lua config).
- `config/alacritty/alacritty.toml` Alacritty font setup.
- `config/fastfetch/config.jsonc` Fastfetch theme/layout.
- `config/cava/config` CAVA defaults (mostly commented).
- `config/.zshrc` Zsh configuration.

## Key features

- Qtile keybindings for apps: `firefox`, `Telegram`, `discord`, `steam-nvidia`, `flameshot`.
- Groups labeled I–IX, Columns layout, and a custom top bar.
- Nerd Font usage in Qtile bar and Alacritty (`FiraCode Nerd Font`, `MesloLGS Nerd Font`).
- Fastfetch layout with custom blocks and colors.

## Requirements

- Qtile, Picom, Alacritty, Neovim.
- Fonts: Nerd Font variants (FiraCode Nerd Font, MesloLGS Nerd Font).
- Optional: fastfetch, cava, flameshot, Telegram, Discord, Steam.

## Install (manual)

This repo is structured like `~/.config` with Zsh config stored under `config/`.
Copy what you need:

```bash
cp -r "$PWD/config/qtile" ~/.config/qtile
cp -r "$PWD/config/nvim" ~/.config/nvim
cp -r "$PWD/config/alacritty" ~/.config/alacritty
cp -r "$PWD/config/fastfetch" ~/.config/fastfetch
cp -r "$PWD/config/cava" ~/.config/cava
cp "$PWD/config/.zshrc" ~/.zshrc
```

## Notes

- Qtile autostart runs `xset -b` and `picom --daemon` in `config/qtile/config.py`.
- Network widget expects `wlan0`; adjust in `config/qtile/config.py` if needed.
- Update widget assumes Arch (`pacman -Syu`).
