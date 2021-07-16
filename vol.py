import requests
import textwrap
import io,os,sys,time
import pigpio
import re
import radiocontrols as rdc
import screencontrols as scr

from evdev import InputDevice, categorize, ecodes
import time
from time import sleep
from threading import Thread

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from PIL import ImageOps
#import numpy as np

## Touchscreen event worker thread
def event_thread():
  for event in dev.read_loop():
    if event.type == ecodes.EV_KEY:
      absevent = categorize(event)
      if absevent.event.value == 0:
        handle_event(dev)

## Red and Blue color channels are reversed from normal RGB on pi framebuffer
def swap_redblue(img):
  "Swap red and blue channels in image"
  r, g, b, a = img.split()
  return Image.merge("RGBA", (b, g, r, a))



## Paint image to screen at position
def blit(img, pos):

  size = img.size
  w = size[0]
  h = size[1]
#  x = pos[0]
#  y = pos[1]

#  n = np.array(img)
#  n[:,:,[0,1,2]] = n[:,:,[2,1,0]]
#  fb[y:y+h,x:x+w] = n

  img = swap_redblue(img)
  fb.seek(4 * ((pos[1]) * fbw + pos[0]))

  iby = img.tobytes()
  for i in range(h):
    fb.write(iby[4*i*w:4*(i+1)*w])
    fb.seek(4 * (fbw - w), 1)

## Clear the screen, set backlight brightness
def initscreen():

  # set screen brightless
  try:
    scr.screenon()
  except Exception:
    pass

  img = Image.new('RGBA', (800, 480))
  blit(img,(0,0))

  displaycontrols(False)

def displayprogress(progress):
  progress = seek / duration * 370
  img = Image.new('RGBA', (370, 6))  

  draw = ImageDraw.Draw(img)
  draw.line((0,0,progress,0),fill='red',width=6)

  blit(img,(430,410))

## Paint << || >> and vol controls
def displaycontrols(status):

  img = Image.new('RGBA',size=(370,70),color=(0,0,0,255))

#  img.paste(ctls[0], (0,0))
  img.paste(ctls[6], (5,10))
  img.paste(ctls[5], (170,10))
  img.paste(ctls[1], (240,10))
  img.paste(ctls[2], (310,10))

  if status:
    img.paste(ctls[4], (90,10))
  else:
    img.paste(ctls[3], (90,10))

  blit(img,(430,410))

## Display artist, song title, album title
def displaymeta(data):

  img = Image.new('RGBA',size=(370,410),color=(0,0,0,255))

  tw1 = textwrap.TextWrapper(width=15)
  tw2 = textwrap.TextWrapper(width=20)
  s = "\n"

  try:
    artist = data["artist"]
  except:
    artist = ""

  try:
    title = data["title"]
  except:
    title = ""

  try:
    album = data["album"]
  except:
    album = ""

  try:
    status = data["status"]
  except:
    status = ""

  try:
    bitdepth = data["bitdepth"].split(' ')[0]
  except:
    bitdepth = ""
    pass

  try:
    samplerate = data["samplerate"]
  except:
    samplerate = ""
    pass

  try:
    tracktype = data["trackType"]
  except:
    tracktype = ""
    pass

  if artist is None: 
    artist = ""
  if title is None:
    title = ""
  if album is None:
    album = ""

  artist = s.join(tw2.wrap(artist))
  album = s.join(tw2.wrap(album))

  draw = ImageDraw.Draw(img)
  draw.text((10,50), artist, (191,245,245),font=fonts[1])
  draw.text((10,200), album, (255,255,255),font=fonts[1])
  if len(bitdepth) > 0:
    draw.text((10,380), samplerate+'/'+bitdepth+' '+tracktype, (255,255,255),font=fonts[2])

  blit(img,(430,0))

  img = Image.new('RGBA',size=(800,50),color=(0,0,0,255))
  draw = ImageDraw.Draw(img)
  draw.text((0,0),  title, (255,255,255),font=fonts[0])

  blit(img,(0,0))

## Grab the album cover and display
def getcoverart(cover_url):

  if cover_url[0] == '/':
    cover_url = "http://volumio.local" + cover_url

  try:
    img = Image.open(requests.get(cover_url, stream=True).raw)
    img = img.resize((430,430))
    img = img.convert('RGBA')

    blit(img,(0,50))
  except Exception as e:
    print(e)
    pass

## Handle Touchscreen events
def handle_event(dev):

  x1 = dev.absinfo(ecodes.ABS_X).value
  y1 = dev.absinfo(ecodes.ABS_Y).value
  x=int((y1/480)*800)
  y=int(480-(x1/800)*480)
  scr.screenon()

  if x >= 430 and y >= 400:
    if x>= 740:
      rdc.volume_up()
    elif x>= 670:
      rdc.volume_down()
    elif x>= 600:
      rdc.play_next()
    elif x>= 520:
      rdc.toggle()
    else:
      rdc.play_previous()      

## URL to Volumio instance REST API
url = 'http://volumio.local/api/v1/getState'

ctls = [] 
ctls.append( Image.open('./images/fond.png') )
ctls.append( Image.open('./images/volumedown.png') )
ctls.append( Image.open('./images/volumeup.png') )
ctls.append( Image.open('./images/play.png') )
ctls.append( Image.open('./images/pause.png') )
ctls.append( Image.open('./images/next.png') )
ctls.append( Image.open('./images/previous.png') )

fonts = []
fonts.append( ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 30) )
fonts.append( ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', 28) )
fonts.append(  ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', 18) )

data = None
ticks = 0
old_nowplaying = ''
old_url = ''
old_status = ''
seek = 0
duration = 0
progress = 0

#h, w, c = 480, 800, 4
#fb = np.memmap('/dev/fb0', dtype='uint8',mode='w+', shape=(h,w,c))
fbw, fbh = 800, 480   # framebuffer dimensions
fb = open("/dev/fb0", "wb")

## Touchscreen input device
dev = InputDevice('/dev/input/event1')

## Start event handler thread
t = Thread(target=event_thread)
t.start()

## Clear the screen
initscreen()

while True:
  try:
    resp = requests.get(url=url)
    data = resp.json()
    cover_url = data['albumart']
    nowplaying = data['title'] 
    status = data['status']
    try:
      seek = int(data['seek'])
      seek = seek / 1000.0
    except Exception:
      seek = 0

    try:
      duration = int(data['duration'])
    except Exception:
      duration = 0

    if status != 'play':
      scr.screenoff() 
      displaycontrols(False)
    elif status == 'play' and seek > 3:
      try:
        displayprogress(seek,duration)
      except Exception:
        progress = 0

    if status != old_status:
      old_status = status
      displayprogress(0)
      if status == 'play':
        displaycontrols(True)
        scr.screenon()

    if nowplaying != old_nowplaying or cover_url != old_url:
      old_nowplaying = nowplaying
      old_url = cover_url
      displaycontrols(True)
      displaymeta(data)
      getcoverart(cover_url)

  except Exception as e:
    print(e)
    pass

  time.sleep(1)

