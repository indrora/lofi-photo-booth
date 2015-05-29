#!/usr/bin/env python

import PIL
from PIL import Image
from PIL import ImageOps

class Printer(object):

    printer_options_double = [14, 27, 14]
    printer_options_reset = [15, 27, 15]
    lofi_name = [
        " _                _____ _ ",
        "| |    ___       |  ___(_)",
        "| |   / _ \ _____| |_  | |",
        "| |__| (_) |_____|  _| | |",
        "|_____\___/      |_|   |_|",
        "",
        " ____  _           _        ",
        "|  _ \| |__   ___ | |_ ___  ",
        "| |_) | '_ \ / _ \| __/ _ \ ",
        "|  __/| | | | (_) | || (_) |",
        "|_|   |_| |_|\___/ \__\___/ ",
        "",
        " ____              _   _     ",
        "| __ )  ___   ___ | |_| |__  ",
        "|  _ \ / _ \ / _ \| __| '_ \ ",
        "| |_) | (_) | (_) | |_| | | |",
        "|____/ \___/ \___/ \__|_| |_|" ]

    lp = None

    def __init__(self):
        self.lp = open("/dev/usb/lp0", "w")

    def Cut(self):
        self.lp.write("\x1e")
        self.lp.flush()

    def AdvancePaper(self, distance):
        """Advances the printer's paper by the provided distance in mm."""
        pixel_count = distance * 8
        while pixel_count > 0:
            if pixel_count > 255:
                self.lp.write(bytearray([27, 74, 255]))
                pixel_count -= 255
            else:
                self.lp.write(bytearray([27, 74, pixel_count]))
                break
        self.lp.flush()

    def PrintTest(self):

        # First we'll enter double-width and double-height mode.
        self.lp.write(bytearray(self.printer_options_double))
        self.lp.flush()

        for line in self.lofi_name:
            self.lp.write(line + "\n")
        self.lp.write("Initialization complete!\n")
        self.lp.flush()

        self.AdvancePaper(25)
        self.Cut()

        # Now we're restoring the non-doubled state.
        self.lp.write(bytearray(self.printer_options_reset))
        self.lp.flush()

    def PrintLarge(self, text):
        """Prints the supplied string in double-width, double-height mode."""
        self.lp.write(bytearray(self.printer_options_double))
        self.lp.write(text + "\n")
        self.lp.write(bytearray(self.printer_options_reset))
        self.lp.flush()

    def PrintImage(self, image):
        # Working on the assumption that this is an 80mm printer, which isn't
        # always certain. Future changes!
        ratio = 1.0
        if(img.size[0] > img.size[1]):
            ratio = float(img.size[1]) / float(img.size[0])
        elif(img.size[1] > img.size[0]):
            ratio = float(img.size[0]) / float(img.size[1])
        new_height = int(576 * ratio)

        img = image.resize((576, new_height), resample=PIL.Image.BILINEAR)
        img = img.convert("1")

        num_rows = img.size[1]
        num_rows_high = (num_rows >> 8) & 0xFF
        num_rows_low = num_rows & 0xFF

        print_image = []
        px = 0x00
        pindex = 0
        for pixel in img.getdata():
            if (pixel == 0):
                px += 1
            if (pindex > 6):
                print_image.append(px)
                pindex = 0
                px = 0x00
            else:
                px = px << 1
                pindex += 1

        self.lp.write(bytearray([27, 83, num_rows_high, num_rows_low]))
        self.lp.write(bytearray(print_image))
        self.lp.flush()
