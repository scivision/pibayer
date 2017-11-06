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
from matplotlib.pyplot import figure,show,draw,pause
from pibayer import pibayerraw,bayerseq

if __name__ == '__main__':
# NOTE: Didn't use SIGINT to allow camera to cleanup/close--avoid GPU memory leaks!
    from argparse import ArgumentParser
    p = ArgumentParser(description='Raspberry Pi Picamera demo with raw Bayer data')
    p.add_argument('exposure',help='exposure time [seconds]',type=float)
    p.add_argument('outfn',help='HDF5 or TIFF file to write image stack to',nargs='?')
    p.add_argument('-n','--numimg',help='number of images to write to disk',type=int,default=10)
    p.add_argument('-8','--bit8',help="convert output to 8-bit",action='store_true')
    p.add_argument('-a','--aim',help='seconds to preview fast GPU-based preview for aiming',type=float)
    p.add_argument('-p','--plot',help='show via Matplotlib (slow)s',action='store_true')
    p = p.parse_args()

    if p.aim:
        preview = p.aim
    elif p.plot:
        preview = 'mpl'
    else:
        preview = None

    print('press Ctrl C  to end program')
    
    #img = pibayerraw(p.numimg, p.exposure, p.bit8, preview, p.outfn)
    img = bayerseq(p.numimg, p.exposure, p.bit8, preview, p.outfn)

    if 0:
        ax = figure().gca()
        for i in range(img.shape[0]):
            ax.imshow(img[i])
            draw();pause(0.05)
