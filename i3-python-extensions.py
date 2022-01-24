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
floating_once = False 
floating = False 
resize = False 


class Floating:
    def set_floating(self, i3, e):
        global floating_once
        global floating
        if floating:
            i3.command('floating enable')
            if resize:
                i3.command('resize set 960 720')
            if floating_once:
                floating_once = False	
                floating = False	
    
    def toggle_floating_once(self):
        global floating_once
        global floating
        floating_once = True	
        floating = True	
        message = "Floating once"
        send_notification(message)

    def toggle_floating(self):
        global floating
        floating = not floating	
        if floating:
            message = "Floating enabled"
        else:
            message = "Floating disabled"
        send_notification(message)
    
    def toggle_resize(self):
        global resize
        resize = not resize	
        if resize:
            message = "Resize enabled"
        else:
            message = "Resize disabled"
        send_notification(message)


class Tiling:
    def toggle_tiling(self):
        global tiling
        tiling = not tiling	
        if tiling:
            message = "Tiling Auto"
        else:
            message = "Tiling Manual"
        send_notification(message)
    
    def set_tiling(self, i3, e):
        win = i3.get_tree().find_focused()
        if tiling:
            if win.rect.height > win.rect.width:
                i3.command('split v')
            else:
                i3.command('split h')


class Bar:
    def toggle_bar(self, i3):
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
    floating = Floating()
    tiling = Tiling()
    bar = Bar()
    
    keyboard.add_hotkey('ctrl+alt+w', lambda: bar.toggle_bar(i3))

    i3.on(Event.WINDOW_FOCUS, tiling.set_tiling) 
    keyboard.add_hotkey('ctrl+alt+t', lambda: tiling.toggle_tiling()) 

    i3.on(Event.WINDOW_NEW, floating.set_floating)
    keyboard.add_hotkey('ctrl+alt+r', lambda: floating.toggle_resize()) 
    keyboard.add_hotkey('ctrl+alt+f', lambda: floating.toggle_floating()) 
    keyboard.add_hotkey('ctrl+alt+shift+f', lambda: floating.toggle_floating_once()) 

    i3.main()

if __name__ == "__main__":
    main()

