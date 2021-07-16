# Volumio-remote
Touchscreen remote for Volumio

Tested on RPi Zero WH with Hyperpixel 4" touchscreen display

In order to run as the pi user to access the framebuffer, you'll need to add it to the video group:

usermod -a -G video pi

To start this at boot, create a service file and launch the bash script with it: https://www.raspberrypi.org/documentation/linux/usage/systemd.md
