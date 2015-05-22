#!/usr/bin/env python

import sys
import PIL
from PIL import Image
from PIL import ImageOps

img = Image.open(sys.argv[1]).convert("RGB")
img = ImageOps.autocontrast(img)

# We need to scale the image in a linear fashion

ratio = 1
if(img.size[0] > img.size[1]):
 ratio = float(img.size[1]) / float(img.size[0])
elif(img.size[1] > img.size[0]):
 ratio = float(img.size[0]) / float(img.size[1]) 

new_height = int(576 * ratio)

# now, scale the image and do it nicely.

img = img.resize((576, new_height ),resample=PIL.Image.BILINEAR )

img = img.convert("1")

lp = open("/dev/usb/lp0", "w")

num_rows = img.size[1]
num_rows_hi = ( num_rows >> 8 ) & 0xFF
num_rows_lo = num_rows & 0xFF

gfxtest = [27,83, num_rows_hi, num_rows_lo]

cvalue = 0x00;
cidx = 0;
for pixel in img.getdata():
  if(pixel == 0):
    cvalue += 1
  if(cidx == 7):
    gfxtest.append( cvalue)
    cvalue = 0
    cidx =0
  else:
    cvalue = cvalue << 1
    cidx += 1

gfxbytes = bytearray(gfxtest)

lp.write(gfxbytes)
lp.write("\n\n")
lp.write(sys.argv[1])
lp.write("\n\n\n\n\n\n\n\n\n\n\n\n\n\x1e\n");
lp.close()

