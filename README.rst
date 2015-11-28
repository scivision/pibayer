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
The `picamera.array.PiBayerArray method <http://picamera.readthedocs.org/en/release-1.10/_modules/picamera/array.html#PiArrayOutput>`_ destripes the raw data and puts it into a stacked 3-D matrix (not demosaicked). 
Dimensions 1944 x 2592 x 3. 
If you use ImageJ, menu Image > Type > RGB Stack you can see the checkerboard effect this makes. Red is upper left, Green is lower left and upper right, Blue is lower right.

I didn't like that behavior, so with their code as an inspiration I made ``rawbayer.py`` that retrieves the image as a 1944 x 2592 2-D array.

