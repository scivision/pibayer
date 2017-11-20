from pathlib import Path
import numpy as np
from time import sleep
#
from picamera import PiCamera
#
from . import setparams, getparams,KEY,CLVL,grabframe

def pibayerraw(Nimg:int, exposure_sec:float, bit8:bool=False,
               preview=None, outfn:Path=None):
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
        setparams(cam, exposure_sec) #wait till after sleep() so that gains settle before turning off auto
        getparams(cam)
#%% optional setup plot
        hi,ht = _preview(cam, preview, bit8)
        if isinstance(preview,(int,float)): # GPU preview
            return
#%% optional setup output file
        f = _writesetup(outfn, Nimg, grabframe(cam, bit8))
#%% main loop
        try:
            cam.start_preview(alpha=200)  # doesn't help dying exposure problem
            for i in range(Nimg):
                img = grabframe(cam, bit8)
#%% write this frame to output file
                writeframe(f, i, img, cam)
#%% plot--not recommended due to very slow 10 seconds update
#                updatepreview(img, hi, ht)
        except KeyboardInterrupt:
            pass # cleanup, close camera. Might need to press Ctrl C a couple times.

    if f is not None:
        f.close()


def _preview(cam:PiCamera, preview, bit8:bool):

    hi=None; ht=None

    if isinstance(preview,(int,float)):
        print('Preview-only mode runs for ',preview,' seconds, or Ctrl-C.')
        try:
            cam.start_preview()
            sleep(preview)
        except KeyboardInterrupt:
            cam.stop_preview()
        finally:
            cam.stop_preview()
    elif preview=='mpl':
        from matplotlib.pyplot import figure
        fg = figure()
        ax=fg.gca()

        img = grabframe(cam, bit8)

        hi = ax.imshow(img, cmap='gray')
        fg.colorbar(hi,ax=ax)
        ht = ax.set_title('')

    return hi,ht


def _writesetup(outfn:Path, Nimg:int, img:np.ndarray):
    if not outfn:
        return

    outfn = Path(outfn).expanduser()

    # note: these file types must be .close() when done!
    if outfn.suffix == '.nc':
        f=outfn
    elif outfn.suffix == '.h5':
        import h5py
        f = h5py.File(outfn,'w',libver='earliest')
        f.create_dataset(KEY,
                         shape=(Nimg,img.shape[0],img.shape[1]),
                         maxshape=(None,img.shape[0],img.shape[1]),
                         dtype=img.dtype,
                         compression='gzip',
                         compression_opts=CLVL,
                         chunks=True)
    elif outfn.suffix in ('.tif','.tiff'):
        import tifffile
        f = tifffile.TiffWriter(str(outfn)) # NO append/compress keywords
    else:
        raise ValueError('unknown file type {}'.format(outfn))

    print('writing',outfn)

    return f

def writeframe(f, i:int, img:np.ndarray, cam:PiCamera):
    assert img.ndim == 2
    expsec = cam.exposure_speed/1e6
    shtsec = cam.shutter_speed/1e6
    again  = float(cam.analog_gain)

    print('writing image #',i,'exp_sec',expsec,'shutter_sec',shtsec,'analog gain',again,
          '\r',end="",flush=True)

    if f is None:
        return

    if isinstance(f,Path) and f.suffix=='.nc':
        import xarray
        imgs = xarray.DataArray(img,
                                attrs={'exp_sec',expsec,'shutter_sec',shtsec,'analog gain',again})
        imgs.to_netcdf(f, mode='a', group=KEY)
    elif 'h5py' in str(f.__class__): # HDF5
        f[KEY][i,:,:] = img
        f['exposure_sec']=expsec
        f['shutter_sec'] = shtsec
        f['analog_gain'] = again
    elif 'tifffile' in str(f.__class__): # TIFF
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
