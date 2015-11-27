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
from time import time
from scipy.misc import bytescale,imsave
#
from picamera import PiCamera
import picamera.array as camarray

def pibayerraw(fn,demosaic,quiet):
    tic = time()
    with PiCamera() as cam: #load camera driver
        with camarray.PiBayerArray(cam) as S: #prepare to read raw
            if not quiet:
                print('{:.1f} sec to load API'.format(time()-tic));tic=time()
            cam.capture(S, 'jpeg', bayer=True) #grab single raw frame
            if not quiet: 
                print('{:.1f} sec to capture frame.'.format(time()-tic)); tic=time()
#%% optional demosaic (raw->RGB)    
            if demosaic:
                img10 = S.demosaic()
                if not quiet: 
                    print('{:.1f} sec to demosaic.'.format(time()-tic)); tic=time()
            else:
                img10 = S.array
#%% linear scale 10-bit to 8-bit 
    img8 = bytescale(img10,0,1024,255,0)
    if not quiet: 
        print('{:.1f} sec for 10->8 bit'.format(time()-tic));tic=time()
#%% write to PNG or JPG or whatever based on file extension
    if fn:
        imsave(fn,img8)
        if not quiet: 
            print('{:.1f} sec for writing image to file'.format(time()-tic))

    return img10,img8    
            
if __name__ == '__main__':
    from argparse import ArgumentParser
    p = ArgumentParser(description='Raspberry Pi Picamera demo with raw Bayer data')
    p.add_argument('-q','--quiet',help="don't give timing info",action='store_true')
    p.add_argument('--demosaic',help='return demosaiced RGB image instead of raw Bayer data',action='store_true')
    p.add_argument('filename',help='output filename to write [png,jpg]')
    p = p.parse_args()

    img10,img8 = pibayerraw(p.filename,p.demosaic,p.quiet)
    
