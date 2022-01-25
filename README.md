# i3_python_extensions
This script aims to extend the features of the i3wm through the i3ipc python library

Included features are
- A basic script to toggle the i3bar to manage systray icons
- A floating mode that is workspace specific
- Autotiling of windows in a spiral pattern

## Installation
First install the required python librarys, this will need to be installed with sudo as the script requires sudo to run
```
sudo pip install keyboard i3ipc
```
Then add the following line to your i3 config file
```
exec_always echo "SUDOPASSWORD" | sudo -S python3 /PATH/TO/i3_python_extensions.py
```
