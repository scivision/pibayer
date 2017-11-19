# -*- coding: utf-8 -*-
import logging
from pathlib import Path
from datetime import datetime
import numpy as np
from time import sleep
from picamera import PiCamera
import picamera.array

KEY = '/imgs'  # handle to write inside the output file
CLVL = 1  # ZIP compression level
REDGAIN = 1.
BLUEGAIN = 1.
ISO=100

def _outconv(cam,Nimg,img):
    i = 0
    with picamera.array.PiBayerArray(cam, output_dims=2) as S:
        while i<Nimg:
            yield S
            img[i] = S.array
            i+=1


def bayerseq(Nimg:int, exposure_sec:float, bit8:bool=False,
               preview=None, outfn:Path=None):

    with PiCamera() as cam: #load camera driver
        setparams(cam, exposure_sec) #wait till after sleep() so that gains settle before turning off auto
        r,c = getparams(cam)

        img = np.empty((Nimg,r,c), dtype=np.uint16)

        print('image 1 /',Nimg,'exposure [sec.]',cam.exposure_speed/1e6)

        cam.start_preview(alpha=200)
        cam.capture_sequence(_outconv(cam,Nimg,img), 'jpeg',
                             burst=False, bayer=True, use_video_port=False)

        print('image',Nimg,'/',Nimg,'exposure [sec.]',cam.exposure_speed/1e6)

    return img


def writeframes(outfn:Path, img:np.ndarray, cam:PiCamera):
    """writes image stack to disk"""
    assert img.ndim == 2
    expsec = cam.exposure_speed/1e6
    shtsec = cam.shutter_speed/1e6
    again  = float(cam.analog_gain)

    if outfn is None:
        return

    outfn = Path(outfn).expanduser()

    print('writing',outfn)

    if outfn.suffix=='.nc':
        import xarray
        imgs = xarray.DataArray(img,
                                attrs={'exp_sec',expsec,'shutter_sec',shtsec,'analog gain',again})
        imgs.to_netcdf(outfn, mode='a', group=KEY)
    elif outfn.suffix=='.h5': # HDF5
        import h5py
        with h5py.file(outfn,'w') as f:
            f[KEY] = img
            f['exposure_sec']=expsec
            f['shutter_sec'] = shtsec
            f['analog_gain'] = again
    elif outfn.suffix in ('.tif','.tiff'): # TIFF
        import tifffile
        with tifffile.TiffWriter(str(outfn)) as f:
            f.save(img, compress=CLVL,
               extratags=[(33434,'f',1,expsec,False),
                          (37377,'f',1,shtsec,False),
                          (41991,'f',3,(again,float(cam.awb_gains[0]),float(cam.awb_gains[1])),False),
               ])


def updatepreview(img, hi, ht):
    if hi is not None:
        from matplotlib.pyplot import draw,pause
#       tic = time()
        hi.set_data(img) #2.7 sec
        ht.set_text(str(datetime.now()))
        draw()
        pause(0.01)
#       print('{:.1f} sec. to update plot'.format(time()-tic))


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


def setparams(c:PiCamera, exposure_sec:float):
    # http://picamera.readthedocs.io/en/release-1.13/recipes1.html#consistent-capture

    # exposure_speed: readonly

    print('camera startup gain autocal')

    c.iso = ISO

    sleep(2) # at least 0.5..0.75 seconds to let camera settle to final gain value.

    c.shutter_speed = int(exposure_sec * 1e6)
    c.exposure_mode = 'off'

    awb_gains = c.awb_gains
    c.drc_strength = 'off' # in order here
    c.awb_mode ='off' #auto white balance
    print('auto AWB gains were',
          float(awb_gains[0]),float(awb_gains[1]))
    #c.awb_gains = awb_gains
    c.awb_gains = (REDGAIN,BLUEGAIN) # 0.0...8.0  (red,blue)


    c.framerate=30 # [frames/sec] caps maximum shutter length
#   c.brightness(50)
#   c.contrast(0)
    c.image_denoise = False
    c.image_effect = 'none'
    c.still_stats=False


def getparams(c:PiCamera):
    """
    need to read new image to update values set in prior step!
    """

    img = grabframe(c)
    print('image size',img.shape)

    print('analog gain', float(c.analog_gain))
    if not 0.9 < c.analog_gain < 1.1:
        logging.warning('analog gain')

     #print('digital gain',float(c.digital_gain))
    np.testing.assert_allclose(float(c.digital_gain), 1.,
                                          rtol=0.1)

    #print('auto white balance:',c.awb_mode)
    assert c.awb_mode=='off'

    #print('AWB Red gain',float(c.awb_gains[0]),
    #      '   AWB Blue gain',float(c.awb_gains[1]))
    #np.testing.assert_allclose(list(map(float,c.awb_gains)),
    #                           (REDGAIN,BLUEGAIN),
    #                           rtol=0.01)

    #print('brightness',c.brightness,
    #      '     contrast',c.contrast)
    assert c.brightness==50
    assert c.contrast==0

    #print('dynamic range compression', c.drc_strength)
    assert c.drc_strength=='off'

    #print('exposure compensation', c.exposure_compensation)
    assert c.exposure_compensation==0

    #print('exposure mode', c.exposure_mode)
    assert c.exposure_mode == 'off'

    print('exposure speed [ms]',c.exposure_speed/1e3,
          '   shutter speed [ms]',c.shutter_speed/1e3)
    assert c.shutter_speed > 0

    print('framerate [frames/sec]',c.framerate)

    #print('image denoise', c.image_denoise)
    assert c.image_denoise==False

    #print('image effect', c.image_effect)
    assert c.image_effect=='none'

    #print('ISO', c.iso)
    assert c.iso == ISO

#    print('exposure metering mode', c.meter_mode)
    assert c.meter_mode=='average'

   # print('rotation angle', c.rotation)
    assert c.rotation==0

    #print('saturation', c.saturation)
    assert c.saturation==0

    #print('Sensor mode',c.sensor_mode)
    assert c.sensor_mode==0

    #print('sharpness', c.sharpness)
    assert c.sharpness==0

    #print('still stats',c.still_stats)
    assert c.still_stats == False

    return img.shape


def grabframe(cam:PiCamera, bit8:bool=False):
#   tic = time()
    with picamera.array.PiBayerArray(cam, output_dims=2) as S:
        cam.capture(S, 'jpeg', bayer=True, use_video_port=False)

        img = S.array  # must be under 'with'

    assert isinstance(img,np.ndarray) and img.ndim == 2
#%% linear scale 10-bit to 8-bit
    if bit8:
        img = sixteen2eight(img, (0,2**10))
#   print('{:.1f} sec. to grab frame'.format(time()-tic))
    return img
