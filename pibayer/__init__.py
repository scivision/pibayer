from __future__ import division
from io import BytesIO
import numpy as np
from picamera import PiCamera
from time import sleep
from matplotlib.pyplot import figure,draw,pause

def pibayerraw(exposure_sec, bit8=False, plot=False):
  """
    loop image acquisition, optionally plotting

    see http://picamera.readthedocs.io/en/release-1.13/recipes1.html?highlight=close#recording-video-to-a-file
    if you wish to record video to a file

    http://picamera.readthedocs.io/en/release-1.13/recipes1.html?highlight=close#capturing-to-a-pil-image
    if you wish to save image(s)
  """
  try:
    with PiCamera() as cam: #load camera driver
        print('camera startup gain autocal')
        sleep(0.75) # somewhere between 0.5..0.75 seconds to let camera settle to final gain value.
        setparams(cam, exposure_sec) #wait till after sleep() so that gains settle before turning off auto
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
                img = sixteen2eight(img10,(0,1024))
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

  except KeyboardInterrupt:
    return bsum,img

def bayersum(I):
    return  (I[1::2,0::2] +   #red
            (I[0::2,0::2] + I[1::2,1::2]) / 2 +    #green
             I[0::2,1::2])

def sixteen2eight(I,Clim):
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

def normframe(I,Clim):
    """
    inputs:
    -------
    I: 2-D Numpy array of grayscale image data
    Clim: length 2 of tuple or numpy 1-D array specifying lowest and highest expected values in grayscale image
    Michael Hirsch, Ph.D.
    """
    Vmin = Clim[0]; Vmax = Clim[1]

    return (I.astype(np.float32).clip(Vmin, Vmax) - Vmin) / (Vmax - Vmin) #stretch to [0,1]

def grabframe(cam):
    """
    http://picamera.readthedocs.org/en/release-1.10/recipes2.html#bayer-data
    """
    S = BytesIO()
    #tic = time()
    cam.capture(S, format='jpeg', bayer=True) #0.6 sec
    #print('{:.1f} sec to capture & retrieve image'.format(time()-tic))
# %% take the last 6404096 bytes
    data = S.getvalue()[-6404096:]
    assert data[:4] == b'BRCM', 'Unable to locate Bayer data at end of buffer'
# %% Strip header
    data = data[32768:]
# %% Reshape into 2D pixels 3264x1952, then throw away blank rightmost 24 columns and bottom 8 rows.
    data = np.frombuffer(data, dtype=np.uint8).reshape((1952, 3264))[:1944, :3240]
# %% Unpack 10-bit values
    """
    every 5 bytes contains the high 8-bits of 4 values followed by
    the low 2-bits of 4 values packed into the fifth byte
    """
    data = data.astype(np.uint16) << 2
    #tic = time()
    for byte in range(4): #0.3 sec
        data[:, byte::5] |= ((data[:, 4::5] >> ((4 - byte) * 2)) & 3)
 #   print('{:.1f} sec to unpack 10-bit data'.format(time()-tic))
    #data = delete(data, s_[4::5], axis=1) #1.2 sec.
# %% let's speed up elimination of the fifth byte columns -- 1.0 sec instead of 1.2 sec with np.delete
  #      tic = time()
    colmask = np.ones(data.shape[1]).astype(bool)
    colmask[np.s_[4::5]]=False
    data = data[:,colmask]
#        print('{:.1f} sec to eliminate fifth byte columns'.format(time()-tic))

    return data

def setparams(c, exposure_sec=None):
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

def getparams(c):
    print('analog , digital gain',c.analog_gain,c.digital_gain)
    print('auto white balance, AWB gains', c.awb_mode,c.awb_gains)
    print('brightness, contrast',c.brightness,c.contrast)
    print('dynamic range compression', c.drc_strength)
    print('exposure compensation', c.exposure_compensation)
    print('exposure mode', c.exposure_mode)
    print('exposure speed, shutter speed [microsec]',c.exposure_speed,c.shutter_speed)
    print('image denoise', c.image_denoise)
    print('image effect', c.image_effect)
    print('ISO', c.iso)
    print('exposure metering mode', c.meter_mode)
    print('rotation angle', c.rotation)
    print('saturation', c.saturation)
    print('sharpness', c.sharpness)