[![Build Status](https://travis-ci.com/scivision/pibayer.svg?branch=master)](https://travis-ci.com/scivision/pibayer)
[![Maintainability](https://api.codeclimate.com/v1/badges/66560126d66fb438a9d4/maintainability)](https://codeclimate.com/github/scivision/raspicam-raw-bayer/maintainability)

# Raspicam raw Bayer mask pixels

Acquire RAW Bayer-masked images with Raspberry Pi camera (before demosaicking). 
Writes HDF5, NetCDF or TIFF compressed image stacks.


## Install

To be installed directly on the Raspberry Pi, using Python &ge; 3.5:
```sh
python3 -m pip install -e .
```

Running the self-test must be done on a Raspberry Pi with camera module:
```python
python3 -m pytest
```

### Tips
* Avoid MMAL errors: `raspi-config` &rarr; Advanced Options &rarr; Memory Split should be 128 MB, not 64 MB.
* Fix error "ImportError: libf77blas.so.3: cannot open shared object file: No such file or directory" by:
  ```sh
  apt install libatlas-dev
  ```

## Examples

Setting of exposure time manually (seconds) is mandatory to avoid mistakes in experiments.

### RAW live video display
```sh
./getrawimage.py 0.01 -a
```

### Dump image stack to disk

* NetCDF: `./getrawimage.py 0.01 output.nc`
* HDF5: `./getrawimage.py 0.01 output.h5`
* TIFF: `./getrawimage.py 0.01 output.tif`

## Command-Line Options

* `-a` GPU-based preview, for aiming camera (fast) 
* `-p` use Matplotlib for slow, live (10 seconds per frame) display 
* `-e` exp_sec manually set exposure time, up to one second (there are still some auto-set gains) 
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
