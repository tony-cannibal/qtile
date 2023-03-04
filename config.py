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

from libqtile import bar, layout, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
import subprocess
import os
from colors import solarized_dark as colors

mod = "mod4"
terminal = "alacritty" 

key_scripts = [
        '~/.config/rofi/scripts/launcher_t2'
        ]

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "l", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "h", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod, "shift"], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod, "shift"], "c", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),

    Key([mod], "p", lazy.spawn(os.path.expanduser('~/.config/rofi/scripts/launcher_t2')), desc="rofi"),
    Key([mod], "period", lazy.screen.next_group(), desc="Next Workspace"),
    Key([mod], "comma", lazy.screen.prev_group(), desc="Previous Workspace"),
    Key([mod], "t", lazy.window.toggle_floating(), desc="Toggle Focused Floating"),
    Key([mod], "x", lazy.spawn(os.path.expanduser("~/.config/rofi/scripts/powermenu_t2")), desc="Power Menu"),
    Key([mod], "kp_add", lazy.spawn("pamixer -i 5"), desc="Power Menu"),
    Key([mod], "kp_subtract", lazy.spawn("pamixer -d 5"), desc="Power Menu"),
]


__groups = {
    1: Group("1"),
    2: Group("2", matches=[Match(wm_class=["firefox"])]),
    3: Group("3", matches=[Match(wm_class=["thunar", "pcmanfm"])]),
    4: Group("4", matches=[Match(wm_class=["deluge"])]),
    5: Group("5"),
    6: Group("6"),
    7: Group("7"),
    8: Group("8"),
}
groups = [__groups[i] for i in __groups]


def get_group_key(name):
    return [k for k, g in __groups.items() if g.name == name][0]

for i in groups:
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key([mod], str(get_group_key(i.name)),
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod1 + shift + letter of group = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(i.name),
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod1 + shift + letter of group = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )


window_options = {
    'border_width':2,
    'margin':6,
}

window_options['border_focus'] = colors['13']
window_options['border_normal'] = colors['1']

layouts = [
    layout.MonadTall(**window_options),
    # layout.Columns(border_focus_stack=["#d75f5f", "#8f3d3d"], border_width=4),
    layout.Max(),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font="terminus",
    fontsize=12,
    padding=4,
    foreground=colors['13'],
    background=colors['1'],
)

extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.GroupBox(
                    disable_drag=True,
                    this_current_screen_border=colors['13'],
                    # rounded=False,
                    highlight_method='text',
                    active=colors['7'], 
                    ##inactive=colors['1'],
                ),
                widget.Sep(padding=6),
                widget.WindowName(),
                widget.Sep(padding=6),
                # File System Script
                widget.GenPollText(
                    update_interval=3,
                    func=lambda: subprocess.check_output(os.path.expanduser('~/.config/qtile/bar_scripts/hdd-space.sh')).decode("utf-8")
                ),
                widget.Sep(padding=6),
                widget.PulseVolume(
                    fmt="VOL {}",
                    update_interval=0.1,
                ),
                widget.Sep(padding=6),
                # Ram Script
                widget.GenPollText(
                    update_interval=3,
                    func=lambda: subprocess.check_output(os.path.expanduser('~/.config/qtile/bar_scripts/mem.sh')).decode("utf-8")
                ),
                widget.Sep(padding=6),
                widget.KeyboardLayout(),
                widget.Sep(padding=6),
                widget.Clock(format="%I:%M %p"),
                widget.Sep(padding=6),
                widget.Systray(),
            ],
            24,
            border_width=[2, 2, 2, 2],  # Draw top and bottom borders
            border_color=[colors['13'], colors['13'], colors['13'], colors['13']]  # Borders are magenta
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = False
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ], **window_options
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"


startup = [
    'xset s off -dpms',
    'setxkbmap -option caps:swapescape',
    'numlockx &',
    'udiskie &',
    'lxpolkit &',
    'feh --bg-fill ~/Pictures/wallpapers/Solarized/sentre.jpg',
    'picom --config ~/.config/qtile/picom/picom.conf &',
    'mpd &'
]

for i in startup:
    subprocess.run(i, shell=True)
