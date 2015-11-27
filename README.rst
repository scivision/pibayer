======================
raspberrypi_raw_camera
======================
Acquire RAW images with Raspberry Pi camera (before demosaicking)

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

    ./bayer.py outraw.png

With timing:
0.2 sec to load API
2.5 sec to capture frame.
3.1 sec for 10->8 bit
8.0 sec for writing image to file

RGB Demosaicked Image
---------------------
::

    ./bayer.py outrgb.png --demosaic

With timing:
0.2 sec to load API
2.5 sec to capture frame.
10.0 sec to demosaic.
3.1 sec for 10->8 bit
12.0 sec for writing image to file

