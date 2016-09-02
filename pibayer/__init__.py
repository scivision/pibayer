try:
    from pathlib import Path
    Path().expanduser()
except (ImportError,AttributeError):
    from pathlib2 import Path
#    
from six import integer_types
from io import BytesIO
from numpy import frombuffer,uint16,uint8,s_,ones

def grabframe(cam):
        """
        http://picamera.readthedocs.org/en/release-1.10/recipes2.html#bayer-data
        """
        S = BytesIO()
        #tic = time()
        cam.capture(S,format='jpeg',bayer=True) #0.6 sec
        #print('{:.1f} sec to capture & retrieve image'.format(time()-tic))
        data = S.getvalue()[-6404096:] #take the last 6404096 bytes
        assert data[:4] == b'BRCM', 'Unable to locate Bayer data at end of buffer'
        # Strip header
        data = data[32768:]
        # Reshape into 2D pixels 3264x1952, then throw away blank rightmost 24 columns and bottom 8 rows.
        data = frombuffer(data, dtype=uint8).reshape((1952, 3264))[:1944, :3240]
        # Unpack 10-bit values; every 5 bytes contains the high 8-bits of 4
        # values followed by the low 2-bits of 4 values packed into the fifth
        # byte
        data = data.astype(uint16) << 2
        #tic = time()
        for byte in range(4): #0.3 sec
            data[:, byte::5] |= ((data[:, 4::5] >> ((4 - byte) * 2)) & 3)
     #   print('{:.1f} sec to unpack 10-bit data'.format(time()-tic))
        #data = delete(data, s_[4::5], axis=1) #1.2 sec.
#%% let's speed up elimination of the fifth byte columns -- 1.0 sec instead of 1.2 sec with np.delete
  #      tic = time()
        colmask = ones(data.shape[1]).astype(bool)
        colmask[s_[4::5]]=False
        data = data[:,colmask]
#        print('{:.1f} sec to eliminate fifth byte columns'.format(time()-tic))
        return data

def setparams(c,exposure_sec=None):
    c.awb_mode ='off' #auto white balance
    c.awb_gains = (1,1.) # 0.0...8.0  (red,blue)
    c.exposure_mode = 'off'
    c.iso= 100
    c.framerate=1 #this caps your maximum shutter length
    if isinstance(exposure_sec,(float,integer_types)):
        c.shutter_speed = int(exposure_sec * 1e6)
#   c.brightness(50)
#   c.contrast(0)
    c.drc_strength = 'off'
    c.image_denoise = False
    c.image_effect = 'none'

def getparams(c):
    print('analog , digital gain {} , {}'.format(c.analog_gain,c.digital_gain))
    print('auto white balance {}  , AWB gains {}'.format(c.awb_mode,c.awb_gains))
    print('brightness {}  contrast {}'.format(c.brightness,c.contrast))
    print('dynamic range compression {}'.format(c.drc_strength))
    print('exposure compensation {}'.format(c.exposure_compensation))
    print('exposure mode {}'.format(c.exposure_mode))
    print('exposure speed, shutter speed {} , {}  [microsec]'.format(c.exposure_speed,c.shutter_speed))
    print('image denoise {}'.format(c.image_denoise))
    print('image effect {}'.format(c.image_effect))
    print('ISO {}'.format(c.iso))
    print('exposure metering mode {}'.format(c.meter_mode))
    print('rotation angle {}'.format(c.rotation))
    print('saturation {}'.format(c.saturation))
    print('sharpness {}'.format(c.sharpness))