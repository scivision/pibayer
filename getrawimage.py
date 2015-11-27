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
        setparams(cam)
        getparams(cam)
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
    print(img10.shape)
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
            
def setparams(c):
    c.awb_mode ='off' #auto white balance
#   c.brightness(50)
#   c.contrast(0)
    c.drc_strength = 'off'
    c.image_denoise = False
    c.image_effect = 'none'

def getparams(c):
    print('analog / digital gain {} / {}'.format(c.analog_gain,c.digital_gain))
    print('auto white balance {}'.format(c.awb_mode))
    print('brightness {}'.format(c.brightness))
    print('contrast {}'.format(c.contrast))    
    print('dynamic range compression {}'.format(c.drc_strength))
    print('exposure compensation {}'.format(c.exposure_compensation))
    print('exposure mode {}'.format(c.exposure_mode))
    print('exposure / shutter speed {} / {}'.format(c.exposure_speed,c.shutter_speed))
    print('image denoise {}'.format(c.image_denoise))    
    print('image effect {}'.format(c.image_effect))
    print('ISO {}'.format(c.iso))
    print('exposure metering mode {}'.format(c.meter_mode))
    print('rotation angle {}'.format(c.rotation))
    print('saturation {}'.format(c.saturation))
    print('sharpness {}'.format(c.sharpness))

if __name__ == '__main__':
    from argparse import ArgumentParser
    p = ArgumentParser(description='Raspberry Pi Picamera demo with raw Bayer data')
    p.add_argument('-q','--quiet',help="don't give timing info",action='store_true')
    p.add_argument('--demosaic',help='return demosaiced RGB image instead of raw Bayer data',action='store_true')
    p.add_argument('filename',help='output filename to write [png,jpg]')
    p = p.parse_args()

    img10,img8 = pibayerraw(p.filename,p.demosaic,p.quiet)
    
