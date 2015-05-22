#!/usr/bin/env python
# vim: set fileencoding=utf-8

from PIL import Image,ImageFilter
import sys;

shade = " `~*aobBN%$#O8"


def squish(val, in_min, in_max, out_min, out_max):
	return (val - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def img_to_shades(name):
	img = Image.open(name)
	img = img.convert("L").filter(ImageFilter.DETAIL)

	imWidth, imHeight = img.size

	pixels = img.load()

	for y in range(0, imHeight):
		for x in range(0, imWidth):
			pix = pixels[x,y]
			shade_idx = squish(pix, 0, 256, 5, 0);
			sys.stdout.write(shade[shade_idx])
		sys.stdout.write('\n')

if __name__ == "__main__":
	for fname in sys.argv[1:]:
 		img_to_shades(fname)	
