# Volumio-remote
Touchscreen remote for Volumio

Tested on RPi Zero WH with Hyperpixel 4" touchscreen display

In order to run as the pi user to access the framebuffer, you'll need to add it to the video group:

usermod -a -G video pi

To start this at boot, create a service file and launch the bash script with it: 

![photo](https://1.bp.blogspot.com/-mDwaKdFdqfc/YPHnZPylrEI/AAAAAAAAulY/35117lUgsLkalz2kztdiJ4QzCGtbUAo2wCLcBGAsYHQ/s2048/07D67D8F-2DB2-4EA0-8367-378C0C2192A2.jpeg)

