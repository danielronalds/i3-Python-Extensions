#!/usr/bin/env python3
#   ____   _____  _____  _____  _____  __     _____  _____  _____  _____  __     ____   _____ 
#  |    \ |  _  ||   | ||     ||   __||  |   | __  ||     ||   | ||  _  ||  |   |    \ |   __|
#  |  |  ||     || | | ||-   -||   __||  |__ |    -||  |  || | | ||     ||  |__ |  |  ||__   |
#  |____/ |__|__||_|___||_____||_____||_____||__|__||_____||_|___||__|__||_____||____/ |_____|
#  
#  github: https://github.com/danielronalds                                                   
#  
#  I3 Pythons scripts
#  
#  Includes:
#  Toggling i3bar
#  Autotiling
#  Floating
#  

from i3ipc import Connection, Event
import keyboard
import os

tiling = True 
bar = False 

def toggle_tiling():
    global tiling
    tiling = not tiling	
    if tiling:
        message = "Tiling Auto"
    else:
        message = "Tiling Manual"
    send_notification(message)

def set_tiling(i3, e):
    win = i3.get_tree().find_focused()
    if tiling:
        if win.rect.height > win.rect.width:
            i3.command('split v')
        else:
            i3.command('split h')

def toggle_bar(i3):
    global bar
    bar = not bar	
    if bar:
        i3.command('bar mode dock')
        message = "Bar Shown"
    else:
        i3.command('bar mode invisible')
        message = "Bar Hidden"
    send_notification(message)

def send_notification(message):
    notification = "notify-send -t 1500 " + message
    os.system(notification)

def main():
    i3 = Connection()

    # Auto tiling
    i3.on(Event.WINDOW_FOCUS, set_tiling) 
    keyboard.add_hotkey('ctrl+alt+t', lambda: toggle_tiling()) 

    # Toggle Bar
    keyboard.add_hotkey('ctrl+alt+w', lambda: toggle_bar(i3))

    i3.main()

if __name__ == "__main__":
    main()
