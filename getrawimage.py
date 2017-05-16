#!/usr/bin/env python3
"""
Demo of reading raw Bayer 10-bit data from Raspberry Pi camera chip using PiCamera module.
This code runs ON the Raspberry Pi directly.

* can only read full chip, no binning or ROI: 2592x1944 pixel image with current imaging chip

Michael Hirsch, Ph.D.
https://scivision.co
"""
from pibayer import pibayerraw

if __name__ == '__main__':
    from argparse import ArgumentParser
    p = ArgumentParser(description='Raspberry Pi Picamera demo with raw Bayer data')
    p.add_argument('-e','--exposure',help='exposure time [seconds]',type=float)
    p.add_argument('-8','--bit8',help="convert output to 8-bit",action='store_true')
    p.add_argument('-p','--plot',help='show live plot',action='store_true')
    p = p.parse_args()

    print('press Ctrl C  to end program')
    bsum,img = pibayerraw(p.exposure, p.bit8, p.plot)

