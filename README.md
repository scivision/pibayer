# Raspicam raw Bayer mask pixels

[![PyPi Download stats](http://pepy.tech/badge/pibayer)](http://pepy.tech/project/pibayer)

Acquire RAW Bayer-masked images with Raspberry Pi camera (before demosaicking).
Writes HDF5, NetCDF or TIFF compressed image stacks.

Install directly on the Raspberry Pi

```sh
apt install python3-numpy

python3 -m pip install -e .
```

Running the self-test must be done on a Raspberry Pi with camera module:

```sh
python3 -m pip install -e .[tests]

python3 -m pytest
```

To install advanced (HDF5, NetCDF4) image writing libraries:

```sh
apt install python3-netcdf4 python3-h5py
```

## Tips

* Avoid MMAL errors: `raspi-config` &rarr; Advanced Options &rarr; Memory Split should be 128 MB, not 64 MB.
* Fix error "ImportError: libf77blas.so.3: cannot open shared object file: No such file or directory" by:
  ```sh
  apt install libatlas-dev
  ```

## Examples

Setting of exposure time manually (seconds) is mandatory to avoid mistakes in experiments.

### RAW live video display

```sh
python getrawimage.py 0.01 -a
```

### Dump image stack to disk

* NetCDF: `./getrawimage.py 0.01 output.nc`
* HDF5: `./getrawimage.py 0.01 output.h5`
* TIFF: `./getrawimage.py 0.01 output.tif`

## Command-Line Options

* `-a` GPU-based preview, for aiming camera (fast)
* `-p` use Matplotlib for slow, live (10 seconds per frame) display
* `-8` output 8-bit array instead of default 10-bit array

## Notes

[Constraints on exposure time](http://picamera.readthedocs.io/en/latest/fov.html#camera-modes)

---

> ValueError: cannot save to a group with the scipy.io.netcdf backend

is fixed by:

```sh
apt install libnetcdf-dev

pip install netcdf4
```
