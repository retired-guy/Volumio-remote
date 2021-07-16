# Volumio-remote
Touchscreen remote for Volumio

Tested on RPi Zero WH with Hyperpixel 4" touchscreen display

In order to run as the pi user to access the framebuffer, you'll need to add it to the video group:

usermod -a -G video pi

To start this at boot, create a service file and launch the bash script with it: 

![photo](https://1.bp.blogspot.com/-TjEQ4zCdZQM/YPHhVj277FI/AAAAAAAAulQ/uRMsNUVCCqUgU4Ifisw5j0b3vm4qAT2lwCLcBGAsYHQ/s2048/63CD0291-683F-4E4E-B25B-8D1DDD3E6F0C.jpeg)

