#!/usr/bin/env python
"""
first, do:

sudo apt install python3-numpy python3-matplotlib python3-picamera
"""
from setuptools import setup

setup(name='pibayer',
      packages=['pibayer'],
      author='Michael Hirsch, Ph.D.',
	  description='Python raw Bayer data from raspberry Pi camera',
	  url='https://github.com/scivision/raspberrypi_raw_camera/',
      install_requires=['picamera'],
	  )
