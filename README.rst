======================
raspberrypi_raw_camera
======================
Acquire RAW images with Raspberry Pi camera (before demosaicking).

NOTE: The PiCamera API has updated since I wrote this, there are substantially faster processing methods now available.
Let me know if you're interested.

:author: Michael Hirsch, Ph.D.

.. contents::

setup
=======
This is meant to be installed directly on the Raspberry Pi::

    sudo apt install python3-numpy python3-matplotlib python3-picamera

    python setup.py develop

Examples
========
There are more efficient ways to do this.
Would like to get better control of "fixed" exposure times.

RAW Bayer filtered image stream displayed on screen via Matplotlib
-------------------------------------------------------------------
::

    ./getrawimage.py -p

RAW Bayer filtered image save to disk
---------------------------------------------
::

    ./getrawimage.py out.png

Command-Line Options
===================

-p                      use Matplotlib for live (5 seconds per frame) display
-e exp_sec      manually set exposure time, up to one second (TODO there are still some auto-set gains)
-8                      output 8-bit array instead of default 10-bit array


Reference
========
In contrast to the 3-D array returned by the `picamera.array.PiBayerArray method <http://picamera.readthedocs.org/en/release-1.10/_modules/picamera/array.html#PiArrayOutput>`_ method,
my program collects the raw Bayer data and puts it into a  2-D matrix (not demosaicked).
Dimensions 1944 x 2592.

The output ``bsum`` is these groups of 4 pixels summed, yielding a 972x1296 pixel array.

