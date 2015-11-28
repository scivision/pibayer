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
from io import BytesIO
from numpy import frombuffer,uint16,uint8,delete,s_,ones
from pdb import set_trace

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
