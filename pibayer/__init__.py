# -*- coding: utf-8 -*-
import logging
from pathlib import Path
import numpy as np
import xarray
from time import sleep
from picamera import PiCamera
import picamera.array
from typing import Tuple

KEY = 'imgs'  # handle to write inside the output file
CLVL = 1  # ZIP compression level
REDGAIN = 1.
BLUEGAIN = 1.
ISO = 100


def _outconv(cam, Nimg, img):
    i = 0
    with picamera.array.PiBayerArray(cam, output_dims=2) as S:
        while i < Nimg:
            yield S
            img[i] = S.array
            i += 1


def bayerseq(Nimg: int, exposure_sec: float) -> xarray.DataArray:

    with PiCamera() as cam:  # load camera driver
        setparams(cam, exposure_sec)  # wait till after sleep() so that gains settle before turning off auto
        r, c = getparams(cam)

        img = np.empty((Nimg, r, c), dtype=np.uint16)

        print('image 1 /', Nimg, 'exposure [sec.]', cam.exposure_speed/1e6)

        cam.start_preview(alpha=200)
        cam.capture_sequence(_outconv(cam, Nimg, img), 'jpeg',
                             burst=False, bayer=True, use_video_port=False)

        print('image', Nimg, '/', Nimg, 'exposure [sec.]', cam.exposure_speed/1e6)

        attrs = {
            'exposure_sec': cam.exposure_speed/1e6,
            'shutter_sec': cam.shutter_speed/1e6,
            'analog_gain': float(cam.analog_gain),
            'awb_gains': np.array(cam.awb_gains).astype(float)
        }

    img = xarray.DataArray(img, name=KEY, attrs=attrs)

    return img


def writeframes(outfn: Path, img: xarray.DataArray):
    """writes image stack to disk"""
    assert img.ndim == 3

    if outfn is None:
        return

    outfn = Path(outfn).expanduser()

    print('writing', outfn)

    if outfn.suffix == '.nc':
        # chunksizes made only few % difference in save time and size
        # fletcher32 had no noticable impact
        # complvl+1 had little useful impact
        enc = {KEY: {'zlib': True, 'complevel': CLVL, 'fletcher32': True,
                     'chunksizes': (1, img.shape[1], img.shape[2])}}
        img.to_netcdf(outfn, mode='w', encoding=enc)
    elif outfn.suffix == '.h5':  # HDF5
        import h5py
        with h5py.File(outfn, 'w') as f:
            f.create_dataset(KEY,
                             data=img,
                             shape=img.shape,
                             dtype=img.dtype,
                             compression='gzip',
                             compression_opts=CLVL,
                             chunks=(1, img.shape[1], img.shape[2]),
                             shuffle=True, fletcher32=True)

            for k, v in img.attrs.items():
                f[k] = v
    elif outfn.suffix in ('.tif', '.tiff'):  # TIFF
        import imageio
        imageio.imsave(outfn, img)


def sixteen2eight(I: np.ndarray, Clim: tuple) -> np.ndarray:
    """
    scipy.misc.bytescale had bugs

    inputs:
    ------
    I: 2-D Numpy array of grayscale image data
    Clim: length 2 of tuple or numpy 1-D array specifying lowest and highest expected values in grayscale image
    Michael Hirsch, Ph.D.
    """
    Q = normframe(I, Clim)
    Q *= 255  # stretch to [0,255] as a float
    return Q.round().astype(np.uint8)  # convert to uint8


def normframe(I: np.ndarray, Clim: tuple) -> np.ndarray:
    """
    inputs:
    -------
    I: 2-D Numpy array of grayscale image data
    Clim: length 2 of tuple or numpy 1-D array specifying lowest and highest expected values in grayscale image
    Michael Hirsch, Ph.D.
    """
    Vmin = Clim[0]
    Vmax = Clim[1]

    return (I.astype(np.float32).clip(Vmin, Vmax) - Vmin) / (Vmax - Vmin)  # stretch to [0,1]


def setparams(c: PiCamera, exposure_sec: float):
    # http://picamera.readthedocs.io/en/release-1.13/recipes1.html#consistent-capture

    # exposure_speed: readonly

    print('camera startup gain autocal')

    c.iso = ISO

    sleep(2)  # at least 0.5..0.75 seconds to let camera settle to final gain value.

    c.shutter_speed = int(exposure_sec * 1e6)
    c.exposure_mode = 'off'

    awb_gains = c.awb_gains
    c.drc_strength = 'off'  # in order here
    c.awb_mode = 'off'  # auto white balance
    print('auto AWB gains were',
          float(awb_gains[0]), float(awb_gains[1]))
    # c.awb_gains = awb_gains
    c.awb_gains = (REDGAIN, BLUEGAIN)  # 0.0...8.0  (red,blue)

    c.framerate = 30  # [frames/sec] caps maximum shutter length
#   c.brightness(50)
#   c.contrast(0)
    c.image_denoise = False
    c.image_effect = 'none'
    c.still_stats = False


def getparams(c: PiCamera) -> Tuple[int, int]:
    """
    need to read new image to update values set in prior step!
    """

    img = grabframe(c)
    print('image size', img.shape)

    print('analog gain', float(c.analog_gain))
    if not 0.9 < c.analog_gain < 1.1:
        logging.warning('analog gain')

    # print('digital gain',float(c.digital_gain))
    np.testing.assert_allclose(float(c.digital_gain), 1.,
                               rtol=0.1)

    # print('auto white balance:',c.awb_mode)
    assert c.awb_mode == 'off'

    # print('AWB Red gain',float(c.awb_gains[0]),
    #      '   AWB Blue gain',float(c.awb_gains[1]))
    # np.testing.assert_allclose(list(map(float,c.awb_gains)),
    #                           (REDGAIN,BLUEGAIN),
    #                           rtol=0.01)

    # print('brightness',c.brightness,
    #      '     contrast',c.contrast)
    assert c.brightness == 50
    assert c.contrast == 0

    # print('dynamic range compression', c.drc_strength)
    assert c.drc_strength == 'off'

    # print('exposure compensation', c.exposure_compensation)
    assert c.exposure_compensation == 0

    # print('exposure mode', c.exposure_mode)
    assert c.exposure_mode == 'off'

    print('exposure speed [ms]', c.exposure_speed/1e3,
          '   shutter speed [ms]', c.shutter_speed/1e3)
    assert c.shutter_speed > 0

    print('framerate [frames/sec]', c.framerate)

    # print('image denoise', c.image_denoise)
    assert not c.image_denoise

    # print('image effect', c.image_effect)
    assert c.image_effect == 'none'

    # print('ISO', c.iso)
    assert c.iso == ISO

#    print('exposure metering mode', c.meter_mode)
    assert c.meter_mode == 'average'

    # print('rotation angle', c.rotation)
    assert c.rotation == 0

    # print('saturation', c.saturation)
    assert c.saturation == 0

    # print('Sensor mode',c.sensor_mode)
    assert c.sensor_mode == 0

    # print('sharpness', c.sharpness)
    assert c.sharpness == 0

    # print('still stats',c.still_stats)
    assert not c.still_stats

    return img.shape


def grabframe(cam: PiCamera, bit8: bool=False):
    #   tic = time()
    with picamera.array.PiBayerArray(cam, output_dims=2) as S:
        cam.capture(S, 'jpeg', bayer=True, use_video_port=False)

        img = S.array  # must be under 'with'

    assert isinstance(img, np.ndarray) and img.ndim == 2
# %% linear scale 10-bit to 8-bit
    if bit8:
        img = sixteen2eight(img, (0, 2**10))
#   print('{:.1f} sec. to grab frame'.format(time()-tic))
    return img
