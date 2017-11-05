#!/usr/bin/env python
"""
Demo of reading raw Bayer 10-bit data from Raspberry Pi camera chip using PiCamera module.
This code runs ON the Raspberry Pi directly.

* can only read full chip, no binning or ROI

Requires Python >= 3.5
https://www.scivision.co/set-python-version-update-alternatives/

UnicodeDecodeError?
raspi-config, set locale: en_US.UTF-8 UTF-8  and same for default locale, then Reboot.

Michael Hirsch, Ph.D.
https://scivision.co
"""
from pibayer import pibayerraw

if __name__ == '__main__':
    import signal
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    from argparse import ArgumentParser
    p = ArgumentParser(description='Raspberry Pi Picamera demo with raw Bayer data')
    p.add_argument('-e','--exposure',help='exposure time [seconds]',type=float)
    p.add_argument('-8','--bit8',help="convert output to 8-bit",action='store_true')
    p.add_argument('-p','--plot',help='show live plot',action='store_true')
    p = p.parse_args()

    print('press Ctrl C  to end program')
    img = pibayerraw(p.exposure, p.bit8, p.plot)

