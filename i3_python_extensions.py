#!/usr/bin/env python3
#    ____   _____  _____  _____  _____  __     _____  _____  _____  _____  __     ____   _____
#   |    \ |  _  ||   | ||     ||   __||  |   | __  ||     ||   | ||  _  ||  |   |    \ |   __|
#   |  |  ||     || | | ||-   -||   __||  |__ |    -||  |  || | | ||     ||  |__ |  |  ||__   |
#   |____/ |__|__||_|___||_____||_____||_____||__|__||_____||_|___||__|__||_____||____/ |_____|
#
#   github: https://github.com/danielronalds
#
#   I3 Pythons scripts
#
#   Includes:
#   Toggling i3bar
#   Autotiling
#   Floating
#
#   By default workspace 1 is floating
#

# Importing needed libraries
from i3ipc import Connection, Event
import keyboard
import os

# Establishing connection with i3 window manager
i3 = Connection()

# Setting default var's, change these to tweak settings
# such as which workspaces are floating by default
tiling = True
bar_visible = False # In the i3 config file, i3bar is set to invisible
floating_once = False
floating_workspaces = [
    True, # Workspace 1 will float windows by default
    False,
    False,
    False,
    False,
    False,
    False,
    False,
    False,
]
resize = True # All floating windows will be auto resized when they are first launched

class Floating:
    """ Encloses all the methods surrounding floating in the script. """
    def set_floating(self, i3, e):
        """ 
        Method to set windows to floating when they are opened 
        by the user, and auto resize them if desired by the user.
        """
        # GET global var floating_once
        global floating_once
        # GET the current workspace
        current_workspace = get_workspace()
        # IF the current workspace is floating, send the floating command.
        if floating_workspaces[current_workspace]:
            i3.command("floating enable")
            # IF autoresizing of new windows is true, resize window to 800x600 pixels.
            if resize:
                i3.command("resize set 800 600")
            # IF floating_once is true, set floating_once 
            # and current workspace floating to false.
            if floating_once:
                floating_once = False
                floating_workspaces[current_workspace] = False

    def toggle_floating_once(self):
        """ 
        Method to set the next opened window to floating 
        when the user presses the assigned keybind.
        """
        # GET global var floating_once and set it true.
        global floating_once
        floating_once = True
        # GET the current workspace and set it to floating.
        current_workspace = get_workspace()
        floating_workspaces[current_workspace] = True
        # SEND a desktop notification telling the user 
        # the next window will be floated.
        message = "Floating once"
        send_notification(message)

    def toggle_floating(self):
        """ 
        Method that toggles whether the program floats new windows, 
        then sends a desktop notification informing the user what 
        the current setting is.
        """
        # GET the current workspace and set toggle wether it is floating or not.
        current_workspace = get_workspace()
        floating_workspaces[current_workspace] = not floating_workspaces[
            current_workspace
        ]
        # SEND a desktop notification telling the user whether 
        # the current workspace is set to floating or not.
        if floating_workspaces[current_workspace]:
            message = "Floating enabled"
        else:
            message = "Floating disabled"
        send_notification(message)

    def toggle_resize(self):
        """ 
        Method that toggles whether the program automatically resizes new 
        windows, then sends a desktop notification informing the user what 
        the current setting is.
        """
        # GET global var resize and toggle it.
        global resize
        resize = not resize
        # SEND a desktop notification telling the user whether 
        # new windows will be auto resized or not.
        if resize:
            message = "Resize enabled"
        else:
            message = "Resize disabled"
        send_notification(message)


class Tiling:
    """ Encloses all the methods surrounding auto tiling of new windows in the script. """
    def toggle_tiling(self):
        """ 
        Method that is called when the assigned keybinding is presed that toggles 
        whether the program automatically arranges new windows into a tiling spiral 
        pattern, then sends a desktop notification informing the user what the 
        current setting is. 
        """
        # GET global var tiling and toggle it's value.
        global tiling
        tiling = not tiling
        # SEND a desktop notification telling the user whether 
        # new windows will be auto tiled or not.
        if tiling:
            message = "Tiling Auto"
        else:
            message = "Tiling Manual"
        send_notification(message)

    def set_tiling(self, i3, e):
        """
        Method that is called when a window is focused by the user
        that sets whether the next window should be tiled beside or 
        below the current window so that it follows a spiral pattern.
        """
        # GET the current window
        current_window = i3.get_tree().find_focused()
        # IF tiling is set to true, then arrange where the next window will be tiled.
        if tiling:
            # IF the current window is taller than it is wide, then the 
            # next window should be tiled beside the current window,
            if current_window.rect.height > current_window.rect.width:
                i3.command("split v")
            # ELSE it should be tiled underneath the current window.
            else:
                i3.command("split h")


class Bar:
    """ Encloses all the methods for controlling the i3bar"""
    def toggle_bar(self):
        """
        A method that is called when the assigned keybinding is pressed 
        that toggles the bar_visible var variable then sets the i3bar to
        either visible or invisible to align with the bar_visible var value.
        """
        # GET the global var bar_visible and toggle it's value.
        global bar_visible
        bar_visible = not bar_visible
        # IF bar_visible is true, then set the i3bar to visible, 
        if bar_visible:
            i3.command("bar mode dock")
            message = "Bar Shown"
        # ELSE set it invisible
        else:
            i3.command("bar mode invisible")
            message = "Bar Hidden"
        # SEND a desktop notification to the user updating them of the bar's new status
        send_notification(message)


def send_notification(message):
    """
    Function that sends a desktop notification

    :param message: the message displayed in the notification
    """
    # The command for a notfication to show for 1500ms with the desired message
    notification = "notify-send -t 1500 " + message
    # Running the command
    os.system(notification)


def get_workspace():
    """
    Function that gets the user's current workspace
    in the i3 window manager.

    :return: the index value of the current workspace starting at zero
    """
    # GET the global i3 var to access the i3 window manager
    global i3
    # GET the current workspace's number assignment
    current_workspace = i3.get_tree().find_focused().workspace().num
    # So that it works better with arrays, RETURN the value starting at zero
    workspace_index = current_workspace - 1
    return workspace_index


def main():
    """ The main method """
    # Instantiating instances of the needed classes
    floating = Floating()
    tiling = Tiling()
    bar = Bar()
    
    # Assigning Ctrl+Alt+W to toggle the visibility of the i3bar
    keyboard.add_hotkey("ctrl+alt+w", lambda: bar.toggle_bar())
    
    # Telling i3 to call the set_tiling() method whenever a new window is focused
    i3.on(Event.WINDOW_FOCUS, tiling.set_tiling)
    # Assigning Ctrl+Alt+T to toggle auto tiling of windows
    keyboard.add_hotkey("ctrl+alt+t", lambda: tiling.toggle_tiling())
    
    # Telling i3 to call the set_floating() method whenever a new window is launched
    i3.on(Event.WINDOW_NEW, floating.set_floating)
    # Assinging Ctrl+Alt+R to toggle whether new windows should be resized or not
    keyboard.add_hotkey("ctrl+alt+r", lambda: floating.toggle_resize())
    # Assinging Ctrl+Alt+F to toggle floating mode for the current workspace
    keyboard.add_hotkey("ctrl+alt+f", lambda: floating.toggle_floating())
    # Assinging Ctrl+Alt+Shift+F to make the next launched window float
    keyboard.add_hotkey("ctrl+alt+shift+f", lambda: floating.toggle_floating_once())

    i3.main()


if __name__ == "__main__":
    main()
