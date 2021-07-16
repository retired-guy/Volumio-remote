"""functions for controlling mpd/mpx radio via python"""

import subprocess
import requests

baseurl = "http://volumio.local/api/v1/commands/?cmd="

def reboot():
    """reboot pi"""
    subprocess.call('mpc stop', shell=True)
    subprocess.call('reboot', shell=True)

def poweroff():
    """shutdown pi"""
    subprocess.call('mpc stop', shell=True)
    subprocess.call('poweroff', shell=True)

def volume_up():
    requests.get(baseurl + "volume&volume=plus")

def volume_down():
    requests.get(baseurl + "volume&volume=minus")

def pause():
    """pause radio playing"""
    requests.get(baseurl + "pause")

def play(pos):
    requests.get(baseurl + "play")

def toggle():
    requests.get(baseurl + "toggle")

def play_next():
    """play next station"""
    requests.get(baseurl + "next")

def play_previous():
    """play next station"""
    requests.get(baseurl + "prev")

