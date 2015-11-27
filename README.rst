======================
raspberrypi_raw_camera
======================
Acquire RAW images with Raspberry Pi camera (before demosaicking).

The `picamera.array.PiBayerArray method <http://picamera.readthedocs.org/en/release-1.10/_modules/picamera/array.html#PiArrayOutput>`_ destripes the raw data and puts it into a stacked 3-D matrix (not demosaicked). 
Dimensions 1944 x 2592 x 3. If you use ImageJ, menu Image > Type > RGB Stack you can see the checkerboard effect this makes. Red is upper left, Green is lower left and upper right, Blue is lower right.

If you don't like this destriped version, let me know and I'll make an option to leave it striped like my Sumix program does. That is, to return a 3888 x 5184 2-D array.

Prereqs
=======
::
    
    sudo apt-get install python3-scipy python3-picamera

Examples
========
There are more efficient ways to do this. The examples capture a single frame and write to disk.
The times given with with a non-overclocked Raspberry Pi 2, Debian Jessie, kernel 4.1.7, Python 3.4.2, SciPy 0.14
In real use we'd think of smarter ways to speed things up.


RAW Bayer filtered image
------------------------
::

    ./getrawimage.py outraw.png

With timing:

0.2 sec to load API

2.5 sec to capture frame.

3.1 sec for 10->8 bit

8.0 sec for writing image to file

RGB Demosaicked Image
---------------------
::

    ./getrawimage.py outrgb.png --demosaic

With timing:

0.2 sec to load API

2.5 sec to capture frame.

10.0 sec to demosaic.

3.1 sec for 10->8 bit

12.0 sec for writing image to file

