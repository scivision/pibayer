#!/usr/bin/env python3
"""
Demo of reading raw Bayer 10-bit data from Raspberry Pi camera chip using PiCamera module.
Notes:
1) can only read full chip, no binning or ROI: 2592x1944 pixel image with current imaging chip
2) captures a single image
3) sudo apt-get install python3-picamera python3-scipy

Michael Hirsch
https://scivision.co
"""
from __future__ import division,absolute_import
from time import sleep,time
from scipy.misc import bytescale,imsave
from matplotlib.pyplot import figure,draw,pause
#
from picamera import PiCamera
#
from params import getparams,setparams
from rawbayer import grabframe

def pibayerraw(fn,exposure_sec,bit8,plot):
    with PiCamera() as cam: #load camera driver
        print('camera startup gain autocal')
        sleep(0.75) # somewhere between 0.5..0.75 seconds to let camera settle to final gain value.
        setparams(cam,exposure_sec) #wait till after sleep() so that gains settle before turning off auto
        getparams(cam)
#%% optional setup plot
        if plot:
            fg = figure()
            ax=fg.gca()
            hi = ax.imshow(bayersum(grabframe(cam)),cmap='gray')
            fg.colorbar(hi,ax=ax)
#%% main loop
        while True:
#            tic = time()
            img10 = grabframe(cam)
#            print('{:.1f} sec. to grab frame'.format(time()-tic))
#%% linear scale 10-bit to 8-bit
            if bit8:
                img = bytescale(img10,0,1024,255,0)
            else:
                img = img10
#%% sum Bayer pixel quads (this is NOT a typical grayscale conversion)
#            tic = time()
            bsum = bayersum(img) #0.09 sec
#            print('{:.2f} sec. to sum quad-pixel Bayer groups'.format(time()-tic))
            if plot:
#                tic = time()
                hi.set_data(bsum) #2.7 sec
                draw(); pause(0.01)
#                print('{:.1f} sec. to update plot'.format(time()-tic))
#%% write to PNG or JPG or whatever based on file extension
            if fn:
                imsave(fn,bsum)
                break

    return bsum,img

def bayersum(I):
    return  (I[1::2,0::2] +   #red
                  (I[0::2,0::2] + I[1::2,1::2]) / 2 +    #green
                  I[0::2,1::2])

if __name__ == '__main__':
    from argparse import ArgumentParser
    p = ArgumentParser(description='Raspberry Pi Picamera demo with raw Bayer data')
    p.add_argument('-e','--exposure',help='exposure time [seconds]',type=float)
    p.add_argument('-8','--bit8',help="convert output to 8-bit",action='store_true')
    p.add_argument('filename',help='output filename to write [png,jpg]',nargs='?')
    p.add_argument('-p','--plot',help='show live plot',action='store_true')
    p = p.parse_args()
   
    try:
        print('press Ctrl c  to end program')
        bsum,img = pibayerraw(p.filename, p.exposure,p.bit8, p.plot)
    except KeyboardInterrupt:
        pass
