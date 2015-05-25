#!/usr/bin/env python

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
    Initialized = False
    
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
