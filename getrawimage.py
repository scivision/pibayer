#!/usr/bin/env python3
"""
Demo of reading raw Bayer 10-bit data from Raspberry Pi camera chip using PiCamera module.
This code runs ON the Raspberry Pi directly.

* can only read full chip, no binning or ROI

Requires Python >= 3.5
https://www.scivision.dev/set-python-version-update-alternatives/

UnicodeDecodeError?
raspi-config, set locale: en_US.UTF-8 UTF-8  and same for default locale, then Reboot.
"""

from pibayer import bayerseq, writeframes
from argparse import ArgumentParser


# NOTE: Didn't use SIGINT to allow camera to cleanup/close--avoid GPU memory leaks!
p = ArgumentParser(description="Raspberry Pi Picamera demo with raw Bayer data")
p.add_argument("exposure", help="exposure time [seconds]", type=float)
p.add_argument("outfn", help="HDF5, NetCDF4 or TIFF file to write image stack to", nargs="?")
p.add_argument("-n", "--numimg", help="number of images to write to disk", type=int, default=10)
p.add_argument("-8", "--bit8", help="convert output to 8-bit", action="store_true")
p.add_argument("-p", "--plot", help="show via Matplotlib (slow)s", action="store_true")
p = p.parse_args()

print("press Ctrl C  to end program")

img = bayerseq(p.numimg, p.exposure)

writeframes(p.outfn, img)
# %%
if p.plot:
    from matplotlib.pyplot import figure, draw, pause

    ax = figure().gca()
    for im in img:
        ax.imshow(im)
        draw()
        pause(0.05)
