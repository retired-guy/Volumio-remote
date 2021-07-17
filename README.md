# Volumio-remote
Touchscreen remote for Volumio

Tested on RPi Zero WH with Hyperpixel 4" touchscreen display

In order to run as the pi user to access the framebuffer, you'll need to add it to the video group:

usermod -a -G video pi

To start this at boot, create a service file and launch the Python script with it: 
https://www.raspberrypi.org/documentation/linux/usage/systemd.md


![photo](https://1.bp.blogspot.com/-bMR_Qcrbmps/YPHqeX-YxlI/AAAAAAAAulg/UmCgEL5ZA7oKJLWs_5bnZcY_5fssKgoTgCLcBGAsYHQ/s2048/1C13DC1D-89F6-43A9-AC26-7E8CD14AE02E.jpeg)

