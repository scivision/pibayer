#!/usr/bin/env python
"""
On Raspberry Pi:

apt install python3-{nose,numpy,matplotlib,picamera,h5py}

pip install tifffile==0.6
"""
from setuptools import setup

setup(name='pibayer',
      packages=['pibayer'],
      author='Michael Hirsch, Ph.D.',
      version='0.5.0',
	  description='Acquire raw Bayer-masked image from Raspberry Pi camera and write to HDF5 or TIFF.',
	  url='https://github.com/scivision/raspicam-raw-bayer',
      classifiers=[
      'Intended Audience :: Science/Research',
      'Development Status :: 4 - Beta',
      'License :: OSI Approved :: MIT License',
      'Topic :: Scientific/Engineering :: Medical Science Apps.',
      'Programming Language :: Python :: 3',
      ],
      install_requires=['picamera','numpy','nose'],
      extras_require={'write':['tifffile','h5py'],
                      'plot':['matplotlib']}
	  )
