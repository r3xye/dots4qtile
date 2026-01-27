# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import subprocess
import libqtile.resources
from libqtile import bar, layout, qtile, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

mod = "mod4"
terminal = "alacritty"
browser = "firefox"
INTERNAL_OUTPUT = "eDP-1"
EXTERNAL_OUTPUT = "HDMI-1"

home = os.path.expanduser('~')

def external_monitor_connected():
    try:
        out = subprocess.check_output(["xrandr", "--query"], text=True)
    except Exception:
        return False
    for line in out.splitlines():
        if line.startswith(EXTERNAL_OUTPUT) and " connected" in line:
            return True
    return False

def configure_outputs():
    if qtile.core.name != "x11":
        return
    if external_monitor_connected():
        subprocess.run(
            [
                "xrandr",
                "--output",
                INTERNAL_OUTPUT,
                "--auto",
                "--primary",
                "--output",
                EXTERNAL_OUTPUT,
                "--auto",
                "--right-of",
                INTERNAL_OUTPUT,
            ]
        )
    else:
        subprocess.run(
            [
                "xrandr",
                "--output",
                EXTERNAL_OUTPUT,
                "--off",
                "--output",
                INTERNAL_OUTPUT,
                "--auto",
                "--primary",
            ]
        )

# Autostart
@hook.subscribe.startup_once
def autostart():
    subprocess.run(['xset', '-b'])
    subprocess.Popen(["picom", "--daemon"])
    # Keep default groups on their intended screens when a second monitor exists.
    if len(qtile.screens) > 1:
        qtile.groups_map["1"].toscreen(0)
        qtile.groups_map["e1"].toscreen(1)
    configure_outputs()

@hook.subscribe.screen_change
def _reconfigure_outputs(event=None):
    configure_outputs()

@hook.subscribe.setgroup
def _warp_pointer_to_group():
    if qtile.core.name != "x11":
        return
    screen = qtile.current_screen
    if screen is None:
        return
    x = screen.x + (screen.width // 2)
    y = screen.y + (screen.height // 2)
    qtile.core.warp_pointer(x, y)

# ---------------------- KEYS ----------------------
keys = [
    Key([mod], "b", lazy.spawn(browser), desc="Okey Google"),
    Key([mod], "t", lazy.spawn("Telegram"), desc="Start Telegram"),
    Key([mod, "shift"], "t", lazy.spawn("discord"), desc="Start Discord"),
    Key([mod], "s", lazy.spawn("steam-nvidia"), desc="lets play"),
    Key([mod, "shift"], "s", lazy.spawn("flameshot gui"), desc="Интерактивный скриншот"),
    
    # Window navigation
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    Key([mod, "shift"], "Return", lazy.layout.toggle_split(), desc="Toggle split/unsplit sides"),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "c", lazy.window.kill(), desc="Kill focused window"),
    Key([mod], "f", lazy.window.toggle_fullscreen(), desc="Toggle fullscreen"),
    Key([mod], "v", lazy.window.toggle_floating(), desc="Toggle floating"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
    Key([mod], "e", lazy.spawn("rofi -show drun"), desc="spawn rofi"),
]

# VTs for Wayland
for vt in range(1, 8):
    keys.append(
        Key(
            ["control", "mod1"],
            f"f{vt}",
            lazy.core.change_vt(vt).when(func=lambda: qtile.core.name == "wayland"),
            desc=f"Switch to VT{vt}",
        )
    )

# ---------------------- GROUPS ----------------------
groups = [
    # Laptop groups (I - IX)
    Group("1", label="I", screen_affinity=0),
    Group("2", label="II", screen_affinity=0),
    Group("3", label="III", screen_affinity=0),
    Group("4", label="IV", screen_affinity=0),
    Group("5", label="V", screen_affinity=0),
    Group("6", label="VI", screen_affinity=0),
    Group("7", label="VII", screen_affinity=0),
    Group("8", label="VIII", screen_affinity=0),
    Group("9", label="IX", screen_affinity=0),
    # External monitor groups (1 - 9)
    Group("e1", label="1", screen_affinity=1),
    Group("e2", label="2", screen_affinity=1),
    Group("e3", label="3", screen_affinity=1),
    Group("e4", label="4", screen_affinity=1),
    Group("e5", label="5", screen_affinity=1),
    Group("e6", label="6", screen_affinity=1),
    Group("e7", label="7", screen_affinity=1),
    Group("e8", label="8", screen_affinity=1),
    Group("e9", label="9", screen_affinity=1),
]

for name in [str(i) for i in range(1, 10)]:
    keys.extend([
        Key([mod], name, lazy.to_screen(0), lazy.group[name].toscreen(0), desc=f"Switch to group {name} on laptop"),
        Key([mod, "shift"], name, lazy.window.togroup(name, switch_group=True), desc=f"Move focused window to group {name}"),
    ])

external_groups = [(f"e{i}", str(i)) for i in range(1, 10)]
if external_monitor_connected():
    for name, key in external_groups:
        keys.extend([
            Key(["mod1"], key, lazy.to_screen(1), lazy.group[name].toscreen(1), desc=f"Switch to external group {name}"),
            Key(["mod1", "shift"], key, lazy.window.togroup(name, switch_group=True), desc=f"Move focused window to external group {name}"),
        ])

# ---------------------- THEME (Gruvbox Dark) ----------------------
gruvbox = {
    "bg0": "#1d2021",
    "bg1": "#3c3836",
    "bg2": "#504945",
    "bg3": "#665c54",
    "fg": "#ebdbb2",
    "fg1": "#fbf1c7",
    "gray": "#928374",
    "red": "#cc241d",
    "green": "#98971a",
    "yellow": "#d79921",
    "blue": "#458588",
    "purple": "#b16286",
    "aqua": "#689d6a",
    "orange": "#d65d0e",
}

# ---------------------- LAYOUTS ----------------------
layout_theme = {
    "border_width": 4,
    "margin": 0,
    "border_focus": gruvbox["blue"],
    "border_normal": gruvbox["bg2"],
}

layouts = [
   layout.Columns(**layout_theme),
#   layout.MonadTall(**layout_theme),
]

# ---------------------- WIDGET DEFAULTS ----------------------
widget_defaults = dict(
    font="FiraCode Nerd Font",
    fontsize=12,
    padding=3,
    foreground=gruvbox["fg"],
    background=gruvbox["bg0"],
)
extension_defaults = widget_defaults.copy()

# ----------------------WALLPAPER------------------------

wallpaper = None
for i in {"jpg", "png"}:
    path = f"/home/r3xye/wallpapers/1.{i}"
    if os.path.exists(path):
        wallpaper = path
        break

# ---------------------- SCREENS ----------------------
screens = [
    Screen(
        top=bar.Bar(
            [
                widget.TextBox(
                    text=" Tilted ",
                    fontsize=16,
                    foreground=gruvbox["fg1"],
                    background=gruvbox["bg1"],
                    padding=8,
                ),
                widget.Sep(linewidth=1, padding=8, foreground=gruvbox["bg3"], background=gruvbox["bg0"]),
                widget.GroupBox(
                    font="FiraCode Nerd Font",
                    fontsize=12,
                    margin_y=3,
                    margin_x=0,
                    padding_y=6,
                    padding_x=8,
                    borderwidth=2,
                    active=gruvbox["blue"],
                    inactive=gruvbox["gray"],
                    this_current_screen_border=gruvbox["orange"],
                    this_screen_border=gruvbox["bg2"],
                    highlight_color=gruvbox["bg2"],
                    rounded=False, 
                    highlight_method="block",
                    block_highlight_text_color=gruvbox["fg1"],
                    visible_groups=["1", "2", "3", "4", "5", "6", "7", "8", "9"],
                ),
                widget.Sep(linewidth=1, padding=8, foreground=gruvbox["bg3"], background=gruvbox["bg0"]),
                widget.WindowName(
                    font="FiraCode Nerd Font",
                    fontsize=13,
                    foreground=gruvbox["fg"],
                    max_chars=20,
                    padding=8,
                    empty_group_string="I hate python",
                    center_aligned=True,
                ),
                widget.Prompt(),

                widget.Sep(linewidth=1, padding=8, foreground=gruvbox["bg3"], background=gruvbox["bg0"]),

                widget.TextBox(text="", fontsize=14, padding=4),
                widget.CPU(format="{load_percent:2.0f}%", fontsize=12, padding=4),

                widget.TextBox(text="", fontsize=14, padding=4),
                widget.Memory(format="{MemUsed:.0f}{mm}", fontsize=12, padding=4),

                widget.TextBox(text="", fontsize=14, padding=4),
                widget.Net(interface="wlan0", format="{down}", fontsize=12, padding=4),

                widget.TextBox(text="", fontsize=14, padding=4),
                widget.Battery(format="{percent:2.0%}", fontsize=12, padding=4),

                widget.TextBox(text="", fontsize=14, padding=4),
                widget.CheckUpdates(
                    distro="Arch",
                    no_update_string="0",
                    display_format="{updates}",
                    fontsize=12,
                    padding=4,
                    mouse_callbacks={"Button1": lazy.spawn("alacritty -e sudo pacman -Syu")},
                ),

                widget.Sep(linewidth=1, padding=8, foreground=gruvbox["bg3"], background=gruvbox["bg0"]),
                widget.TextBox(text="", fontsize=14, padding=4),
                widget.Clock(format="%Y-%m-%d %a %I:%M %p", fontsize=12, padding=4),

               widget.Systray(),
            ],
            28,
            background=gruvbox["bg0"]
        ),
        wallpaper=wallpaper,
        wallpaper_mode="fill",
    ),
    Screen(
        top=bar.Bar(
            [
                widget.TextBox(
                    text=" Tilted ",
                    fontsize=16,
                    foreground=gruvbox["fg1"],
                    background=gruvbox["bg1"],
                    padding=8,
                ),
                widget.Sep(linewidth=1, padding=8, foreground=gruvbox["bg3"], background=gruvbox["bg0"]),
                widget.GroupBox(
                    font="FiraCode Nerd Font",
                    fontsize=12,
                    margin_y=3,
                    margin_x=0,
                    padding_y=6,
                    padding_x=8,
                    borderwidth=2,
                    active=gruvbox["blue"],
                    inactive=gruvbox["gray"],
                    this_current_screen_border=gruvbox["orange"],
                    this_screen_border=gruvbox["bg2"],
                    highlight_color=gruvbox["bg2"],
                    rounded=False,
                    highlight_method="block",
                    block_highlight_text_color=gruvbox["fg1"],
                    visible_groups=["e1", "e2", "e3", "e4", "e5", "e6", "e7", "e8", "e9"],
                ),
                widget.Sep(linewidth=1, padding=8, foreground=gruvbox["bg3"], background=gruvbox["bg0"]),
                widget.WindowName(
                    font="FiraCode Nerd Font",
                    fontsize=13,
                    foreground=gruvbox["fg"],
                    max_chars=20,
                    padding=8,
                    empty_group_string="I hate python",
                    center_aligned=True,
                ),
                widget.Prompt(),
                widget.Sep(linewidth=1, padding=8, foreground=gruvbox["bg3"], background=gruvbox["bg0"]),
                widget.TextBox(text="", fontsize=14, padding=4),
                widget.CPU(format="{load_percent:2.0f}%", fontsize=12, padding=4),
                widget.TextBox(text="", fontsize=14, padding=4),
                widget.Memory(format="{MemUsed:.0f}{mm}", fontsize=12, padding=4),
                widget.TextBox(text="", fontsize=14, padding=4),
                widget.Net(interface="wlan0", format="{down}", fontsize=12, padding=4),
                widget.TextBox(text="", fontsize=14, padding=4),
                widget.Battery(format="{percent:2.0%}", fontsize=12, padding=4),
                widget.TextBox(text="", fontsize=14, padding=4),
                widget.CheckUpdates(
                    distro="Arch",
                    no_update_string="0",
                    display_format="{updates}",
                    fontsize=12,
                    padding=4,
                    mouse_callbacks={"Button1": lazy.spawn("alacritty -e sudo pacman -Syu")},
                ),
                widget.Sep(linewidth=1, padding=8, foreground=gruvbox["bg3"], background=gruvbox["bg0"]),
                widget.TextBox(text="", fontsize=14, padding=4),
                widget.Clock(format="%Y-%m-%d %a %I:%M %p", fontsize=12, padding=4),
                widget.Systray(),
            ],
            28,
            background=gruvbox["bg0"],
        ),
        wallpaper=wallpaper,
        wallpaper_mode="fill",
    ),
]

# ---------------------- MOUSE ----------------------
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

# ---------------------- FLOATING ----------------------
floating_layout = layout.Floating(
    float_rules=[
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),
        Match(wm_class="makebranch"),
        Match(wm_class="maketag"),
        Match(wm_class="ssh-askpass"),
        Match(title="branchdialog"),
        Match(title="pinentry"),
    ]
)

auto_fullscreen = True
focus_on_window_activation = "smart"
follow_mouse_focus = False
focus_previous_on_window_remove = False
reconfigure_screens = True
auto_minimize = True

wmname = "LG3D"
