import numpy as np
import picamera
import picamera.array
from time import sleep
from matplotlib.pyplot import figure,draw,pause

def pibayerraw(exposure_sec, bit8:bool=False, plot:bool=False):
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
  try:
    with picamera.PiCamera() as cam: #load camera driver
        print('camera startup gain autocal')
        sleep(0.75) # somewhere between 0.5..0.75 seconds to let camera settle to final gain value.
        setparams(cam, exposure_sec) #wait till after sleep() so that gains settle before turning off auto
        getparams(cam)
#%% optional setup plot
        hi = _setupfig(cam,plot)
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
            if plot:
#                tic = time()
                hi.set_data(img) #2.7 sec
                draw()
                pause(0.01)
#                print('{:.1f} sec. to update plot'.format(time()-tic))

  except KeyboardInterrupt:
    return img


def grabframe(cam):

    with picamera.array.PiBayerArray(cam) as S:
        cam.capture(S, 'jpeg', bayer=True)

        img = S.array  # must be under 'with'

    assert isinstance(img,np.ndarray)

    return img


def _setupfig(cam, plot:bool):

    if plot:
        fg = figure()
        ax=fg.gca()

        img = grabframe(cam)

        hi = ax.imshow(img, cmap='gray')
        fg.colorbar(hi,ax=ax)


def sixteen2eight(I, Clim:tuple):
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


def normframe(I, Clim:tuple):
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
