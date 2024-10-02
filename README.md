# Huskontroller" 

## Touch Control Hardware
The following components are necessary to build the touch controls:
- Raspberry Pi 4
- Raspberry Pi Power Adapter
- 32GB microSD Card
- Pi Aluminum Heatsinks
- Official Raspberry Pi 7" Touch Display
- A USB to DB9 Serial adapter
- SmartiPi Touch Pro Case (Large)

The software as-is is designed to work with an Extron 1804 DO Switcher and most Panasonic projectors. (It will likely work with most Extron switchers, but I've only used it with this one model.) Different hardware can be used by replacing the "extron_serial.py" module with another module offering the same functions.

## Requirements to run the software
Python 3.x (Tested with 3.11, but it should be compatible pretty far back.)
pyserial 3.5
Kivy 2.1.0

Python can be installed from Python.org or via your distro's repo. I've been using the repo on Raspberry Pi OS.
pyserial can be installed with pip on a dev machine:
pip install pyserial
In Pi OS, I believe it's installed by default. If not, you'll need to install from repo:
sudo apt install python3-serial

This is similar with Kivy:
pip install kivy
And on Pi OS:
sudo apt install python3-kivy

The actual script is started with:
python3 Huskontroller.py

If you try to start it without having the necessary serial ports attached and configured, it may raise an error that it can't find the serial port. There is a test device called "test_serial.py" which may be used if needed for testing.

## Files/Folder Structure
The program relies on "Huskontroller.py", "Huskontroller.kv", and "extron_serial.py" in order to function. Huskontroller.py and Huskontroller.kv run the interface, with extron_serial.py sending the actual SIS commands to the Extron device via a serial connection. There's also a "test_serial.py" file, which can be used for testing in the case where a serial port is not connected. Implementation details are in the code of the software.

The folder also contains a "README.md" file, a "fonts" folder (the device uses Open Sans, as a font recommended by the university), an "images" folder, containing the background and some spare images, and a ".git" folder, which contains the git repo info for the folder.
