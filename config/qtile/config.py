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

home = os.path.expanduser('~')

# Autostart
@hook.subscribe.startup_once
def autostart():
    subprocess.run(['xset', '-b'])
    subprocess.Popen(["picom", "--daemon"])

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
    Group("1", label="I"),
    Group("2", label="II"),
    Group("3", label="III"),
    Group("4", label="IV"),
    Group("5", label="V"),
    Group("6", label="VI"),
    Group("7", label="VII"),
    Group("8", label="VIII"),
    Group("9", label="IX"),
]

for i in groups:
    keys.extend([
        Key([mod], i.name, lazy.group[i.name].toscreen(), desc=f"Switch to group {i.name}"),
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name, switch_group=True), desc=f"Move focused window to group {i.name}"),
    ])

# ---------------------- LAYOUTS ----------------------
layout_theme = {
    "border_width": 4,
    "margin": 1,
    "border_focus": "#3a0f5e",
    "border_normal": "#200a40"
}

layouts = [
    layout.Columns(**layout_theme),
    layout.MonadTall(**layout_theme),
]

# ---------------------- WIDGET DEFAULTS ----------------------
widget_defaults = dict(
    font="FiraCode Nerd Font",
    fontsize=12,
    padding=3,
)
extension_defaults = widget_defaults.copy()

# ---------------------- SCREENS ----------------------
screens = [
    Screen(
        top=bar.Bar(
            [
                widget.TextBox(
                    text=" Tilted ",
                    fontsize=16,
                    foreground="#000000",
                    background="#ffffff",
                    padding=8,
                ),
                widget.Sep(linewidth=1, padding=8, foreground="#444444", background="#282c34"),
                widget.GroupBox(
                    font="FiraCode Nerd Font",
                    fontsize=12,
                    margin_y=3,
                    margin_x=0,
                    padding_y=6,
                    padding_x=8,
                    borderwidth=2,
                    active="#61afef",      
                    inactive="#5c6370",
                    rounded=False, 
                    highlight_method="block",
                    block_highlight_text_color="#ffffff",
                ),
                widget.Sep(linewidth=1, padding=8, foreground="#444444", background="#282c34"),
                widget.WindowName(
                    font="FiraCode Nerd Font",
                    fontsize=13,
                    foreground="#e5e9f0",
                    max_chars=20,
                    padding=8,
                    empty_group_string="I hate python",
                    center_aligned=True,
                ),

                widget.Sep(linewidth=1, padding=8, foreground="#444444", background="#282c34"),

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

                widget.Sep(linewidth=1, padding=8, foreground="#444444", background="#282c34"),
                widget.TextBox(text="", fontsize=14, padding=4),
                widget.Clock(format="%Y-%m-%d %a %I:%M %p", fontsize=12, padding=4),

               widget.Systray(),
            ],
            28,
            background="#1c1f24"
        ),
        wallpaper="/home/r3xye/wallpapers/1.png",
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
focus_previous_on_window_remove = False
reconfigure_screens = True
auto_minimize = True

wmname = "LG3D"
