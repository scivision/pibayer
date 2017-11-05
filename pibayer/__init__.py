# -*- coding: utf-8 -*-
from datetime import datetime
import numpy as np
from time import sleep
from matplotlib.pyplot import figure,draw,pause
from picamera import PiCamera
import picamera.array

def pibayerraw(exposure_sec:float, bit8:bool=False, plot:bool=False):
    """
    loop image acquisition, optionally plotting

    see http://picamera.readthedocs.io/en/release-1.13/recipes1.html?highlight=close#recording-video-to-a-file
    if you wish to record video to a file

    http://picamera.readthedocs.io/en/release-1.13/recipes1.html?highlight=close#capturing-to-a-pil-image
    if you wish to save image(s)

    Demosaick reference:
        https://github.com/scivision/pysumix/blob/master/pysumix/demosaic.py#L58
        may need adaptation for Raspberry Pi camera
    """
    with PiCamera() as cam: #load camera driver
        print('camera startup gain autocal')
        sleep(0.75) # somewhere between 0.5..0.75 seconds to let camera settle to final gain value.
        setparams(cam, exposure_sec) #wait till after sleep() so that gains settle before turning off auto
        getparams(cam)
#%% optional setup plot
        hi,ht = _setupfig(cam,plot)
#%% main loop, runs until Ctrl-C from user.
        while True:
#            tic = time()
            img10 = grabframe(cam)
#            print('{:.1f} sec. to grab frame'.format(time()-tic))
#%% linear scale 10-bit to 8-bit
            img = sixteen2eight(img10,(0,2**10)) if bit8 else img10
#%% plot
            if plot:
#                tic = time()
                hi.set_data(img) #2.7 sec
                ht.set_text(str(datetime.now()))
                draw()
                pause(0.01)
#                print('{:.1f} sec. to update plot'.format(time()-tic))


def grabframe(cam:PiCamera):

    with picamera.array.PiBayerArray(cam, output_dims=2) as S:
        cam.capture(S, 'jpeg', bayer=True)

        img = S.array  # must be under 'with'

    assert isinstance(img,np.ndarray) and img.ndim == 2

    return img


def _setupfig(cam:PiCamera, plot:bool):

    if plot:
        fg = figure()
        ax=fg.gca()

        img = grabframe(cam)

        hi = ax.imshow(img, cmap='gray')
        fg.colorbar(hi,ax=ax)
        ht = ax.set_title('')

        return hi,ht
    else:
        print('Live video preview disabled.')


def sixteen2eight(I:np.ndarray, Clim:tuple) -> np.ndarray:
    """
    scipy.misc.bytescale had bugs

    inputs:
    ------
    I: 2-D Numpy array of grayscale image data
    Clim: length 2 of tuple or numpy 1-D array specifying lowest and highest expected values in grayscale image
    Michael Hirsch, Ph.D.
    """
    Q = normframe(I,Clim)
    Q *= 255 # stretch to [0,255] as a float
    return Q.round().astype(np.uint8) # convert to uint8


def normframe(I:np.ndarray, Clim:tuple) -> np.ndarray:
    """
    inputs:
    -------
    I: 2-D Numpy array of grayscale image data
    Clim: length 2 of tuple or numpy 1-D array specifying lowest and highest expected values in grayscale image
    Michael Hirsch, Ph.D.
    """
    Vmin = Clim[0]
    Vmax = Clim[1]

    return (I.astype(np.float32).clip(Vmin, Vmax) - Vmin) / (Vmax - Vmin) #stretch to [0,1]


def setparams(c:PiCamera, exposure_sec:float=None):
    c.awb_mode ='off' #auto white balance
    c.awb_gains = (1,1.) # 0.0...8.0  (red,blue)
    c.exposure_mode = 'off'
    c.iso= 100
    c.framerate=1 #this caps your maximum shutter length
    if isinstance(exposure_sec,(float,int)):
        c.shutter_speed = int(exposure_sec * 1e6)
#   c.brightness(50)
#   c.contrast(0)
    c.drc_strength = 'off'
    c.image_denoise = False
    c.image_effect = 'none'


def getparams(c:PiCamera):
    print('analog gain',c.analog_gain,'   digital gain',c.digital_gain)
    print('auto white balance:',c.awb_mode)
    print('AWB Red gain',c.awb_gains[0],'   AWB Blue gain',c.awb_gains[1])
    print('brightness, contrast',c.brightness,c.contrast)
    print('dynamic range compression', c.drc_strength)
    print('exposure compensation', c.exposure_compensation)
    print('exposure mode', c.exposure_mode)
    print('exposure speed, shutter speed [μs]',c.exposure_speed,c.shutter_speed)
    print('image denoise', c.image_denoise)
    print('image effect', c.image_effect)
    print('ISO', c.iso)
    print('exposure metering mode', c.meter_mode)
    print('rotation angle', c.rotation)
    print('saturation', c.saturation)
    print('sharpness', c.sharpness)
