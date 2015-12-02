======================
raspberrypi_raw_camera
======================
Acquire RAW images with Raspberry Pi camera (before demosaicking).

.. contents::

Prereqs
=======
::
    
    sudo apt-get install python3-scipy python3-picamera

Examples
========
There are more efficient ways to do this.

Would like to get better control of fixed exposure times.

RAW Bayer filtered image stream displayed on screen via Matplotlib
--------------------------------------------------------------------------------
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
The `picamera.array.PiBayerArray method <http://picamera.readthedocs.org/en/release-1.10/_modules/picamera/array.html#PiArrayOutput>`_ destripes the raw data and puts it into a  2-D matrix (not demosaicked). 
Dimensions 1944 x 2592.

The output ``bsum`` is these groups of 4 pixels summed, yielding a 972x1296 pixel array.

