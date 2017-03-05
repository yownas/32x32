#!/usr/bin/env python

# (This is an example similar to an example from the Adafruit fork
#  to show the similarities. Most important difference currently is, that
#  this library wants RGB mode.)
#
# A more complex RGBMatrix example works with the Python Imaging Library,
# demonstrating a few graphics primitives and image loading.
# Note that PIL graphics do not have an immediate effect on the display --
# image is drawn into a separate buffer, which is then copied to the matrix
# using the SetImage() function (see examples below).
# Requires rgbmatrix.so present in the same directory.

# PIL Image module (create or load images) is explained here:
# http://effbot.org/imagingbook/image.htm
# PIL ImageDraw module (draw shapes to images) explained here:
# http://effbot.org/imagingbook/imagedraw.htm

from PIL import Image
from PIL import ImageDraw
import time
import re
from threading import Thread
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
from random import randint

# Configuration for the matrix
options = RGBMatrixOptions()
options.rows = 32
options.chain_length = 1
options.parallel = 1
options.pwm_bits = 11 			# 1..11
options.brightness = 100		# 1..100
options.pwm_lsb_nanoseconds = 150
options.hardware_mapping = 'adafruit-hat-pwm'  # If you have an Adafruit HAT: 'adafruit-hat'

matrix = RGBMatrix(options = options)

font = graphics.Font()
#font.LoadFont("fonts/7x13.bdf")
font.LoadFont("fonts/4x6.bdf")
textColor = graphics.Color(0, 0, 0)

# RGB example w/graphics prims.
# Note, only "RGB" mode is supported currently.
image = Image.new("RGB", (32, 32))

# 4 rows of text
text=["","","$TIME","",""]
text_new=["","","","",""]
tcol=[[128,128,128], [128,128,128], [128,128,128], [128,128,128], [128,128,128]]
tpos=[0,0,0,0,0]
tspd=[1,1,1,1,1]

matrix.Clear()
imagename="img/bliss.ppm"
image = Image.open(imagename)  # Can be larger than matrix if wanted!!
showbg=False
EXIT=False

def updateThread():
  global showbg
  global image

  print "(updateThread)"
  while not EXIT:
    if showbg:
      matrix.SetImage(image, 0, 0)
    else:
      matrix.Clear()

    # Show texts
    for l in range(0, len(text)):
      # Search-replace-doit
      tmp_text = text[l].replace("$TIME", time.strftime("%H:%M:%S"))
      tmp_text = tmp_text.replace("$DATE", time.strftime("%y-%m-%d"))
      tmp_text = tmp_text.replace("$LONGDATE", time.strftime("%Y-%m-%d %j"))
      tmp_text = tmp_text.replace("%%A", time.strftime("%A"))

      r = str(tcol[l][0])
      g = str(tcol[l][1])
      b = str(tcol[l][2])

      if re.match("[0-9]*-[0-9]*", r):
        t = r + ":-:-:"
        o,v,d,j = t.split(":", 3)
        min,max = o.split("-", 1)
        min=int(min)
        max=int(max)
        if v == "-":
          v = 0
        if d == "-":
          d = 1
        v=int(v)+int(d)
        if (v < min):
          d=-int(d)
          v = min
        if (v > max):
          d=-int(d)
          v = max
        tcol[l][0] = str(o) + ":" + str(v) + ":" + str(d)
        r=v
      elif re.match("^r", r):
        t = r + ":0:255:"
        j,start,stop,j = t.split(":", 3)
        r = randint(int(start), int(stop))

      if re.match("[0-9]*-[0-9]*", g):
        t = g + ":-:-:"
        o,v,d,j = t.split(":", 3)
        min,max = o.split("-", 1)
        min=int(min)
        max=int(max)
        if v == "-":
          v = 0
        if d == "-":
          d = 1
        v=int(v)+int(d)
        if (v < min):
          d=-int(d)
          v = min
        if (v > max):
          d=-int(d)
          v = max
        tcol[l][1] = str(o) + ":" + str(v) + ":" + str(d)
        g=v
      elif re.match("^r", g):
        t = g + ":0:255:"
        j,start,stop,j = t.split(":", 3)
        g = randint(int(start), int(stop))

      if re.match("[0-9]*-[0-9]*", b):
        t = b + ":-:-:"
        o,v,d,j = t.split(":", 3)
        min,max = o.split("-", 1)
        min=int(min)
        max=int(max)
        if v == "-":
          v = 0
        if d == "-":
          d = 1
        v=int(v)+int(d)
        if (v < min):
          d=-int(d)
          v = min
        if (v > max):
          d=-int(d)
          v = max
        tcol[l][2] = str(o) + ":" + str(v) + ":" + str(d)
        b=v
      elif re.match("^r", b):
        t = b + ":0:255:"
        j,start,stop,j = t.split(":", 3)
        b = randint(int(start), int(stop))

      textColor = graphics.Color(int(r), int(g), int(b))

      graphics.DrawText(matrix, font, int(tpos[l]), (l+1)*6, textColor, tmp_text)
      if len(tmp_text) > 8 or tpos[l] > 0:
        tpos[l]=float(tpos[l]-float(tspd[l]))
      if len(tmp_text) <= 8 and tpos[l] < -(len(tmp_text)+8)*4:
        tpos[l]=0
      if len(tmp_text) > 8 and tpos[l] < -(len(tmp_text)+8)*4:
        tpos[l]=32
        text[l]=text_new[l]

    # Sleep
    time.sleep(0.03)

def readThread():
  print "(readThread)"

  # Init
  txt="redraw"
  global showbg
  global imagename
  global image
  global EXIT
  global text
  global tcol
  global tpos

  # Loop
  while not EXIT:
    # print "Parse: " + txt
    for i in txt.split(";"):
      c = i.split(" ")  
      # Nop
      if (c[0] == "nop"):
        # Nop-doit
        print "Zzzz..."
        time.sleep(1)
      # Clear text
      elif (c[0] == "ctxt"):
        c,n = i.split(" ", 1)
        if int(n) < len(text) and int(n) >= 0: 
          text[int(n)] = ""
          text_new[int(n)] = ""
          tpos[int(n)] = 0
      # Display clock
      elif (c[0] == "clock"):
        c,n = i.split(" ", 1)
        if int(n) < len(text) and int(n) >= 0: 
          text[int(n)] = "$TIME"
      # Display date
      elif (c[0] == "date"):
        c,n = i.split(" ", 1)
        if int(n) < len(text) and int(n) >= 0: 
          text[int(n)] = "$DATE"
      # Show text
      elif (c[0] == "txt"):
        c,n,t = i.split(" ", 2)
        if int(n) < len(text) and int(n) >= 0: 
          text_new[int(n)] = t
          # Emergency check
          if len(text[int(n)]) > 1000:
            text[int(n)] = ""
          if len(text[int(n)]) > 8 or len(text_new[int(n)]) > 8:
            # If old text was long - add new text
            text[int(n)] += "        " + t
          else:
            # Else - just set new text
            text[int(n)] = t
            # Scroll long text?
            if len(text[int(n)]) > 8:
              tpos[int(n)] = 32
            else:
              tpos[int(n)] = 0
        else:
           print n + " out of range!"
      # Replace text
      elif (c[0] == "rtxt"):
        c,n,t = i.split(" ", 2)
        if int(n) < len(text) and int(n) >= 0: 
          text_new[int(n)] = t
          # If old text is not scrolling, set new pos.
          if len(text[int(n)]) <= 8:
            # Scroll long text?
            if len(text_new[int(n)]) > 8:
              tpos[int(n)] = 32
            else:
              tpos[int(n)] = 0
          text[int(n)] = t
        else:
           print n + " out of range!"
      # Set text-color
      elif (c[0] == "tcol"):
        c,n,r,g,b = i.split(" ", 4)
        if int(n) < len(text) and int(n) >= 0: 
          tcol[int(n)][0] = r
          tcol[int(n)][1] = g
          tcol[int(n)][2] = b
      # Set text-speed
      elif (c[0] == "tspd"):
        c,n,s = i.split(" ", 2)
        if int(n) < len(text) and int(n) >= 0: 
          tspd[int(n)] = s
      # Clear background
      elif (c[0] == "clr"):
        matrix.Clear()
        showbg=False
      # Load background image 
      elif (c[0] == "load"):
        c,file = i.split(" ", 1)
        try:
          image = Image.open(file)  # Can be larger than matrix if wanted!!
          imagename = file
          showbg=True
        except:
          print "ERROR: loading file " + file
          image = Image.open(imagename)  # Can be larger than matrix if wanted!!
      # Exit
      elif (c[0] == "exit"):
        print "Bye bye."
        matrix.Clear()
        EXIT=True
        return

    txt = raw_input()

try:
  print "Starting threads."
  tUpdate = Thread(target=updateThread, args=() )
  tUpdate.start()
  tRead = Thread(target=readThread, args=() )
  tRead.start()
  print "Done."
except:
  print "Can not start threads."
