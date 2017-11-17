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
      version='0.5.1',
	  description='Acquire raw Bayer-masked image from Raspberry Pi camera and write image stack to HDF5 or TIFF.',
	  long_description=open('README.rst').read(),
	  url='https://github.com/scivision/raspicam-raw-bayer',
      classifiers=[
      'Intended Audience :: Science/Research',
      'Development Status :: 4 - Beta',
      'License :: OSI Approved :: MIT License',
      'Topic :: Scientific/Engineering :: Medical Science Apps.',
      'Programming Language :: Python :: 3',
      ],
      install_requires=['picamera','numpy','nose'],
      extras_require={'io':['tifffile==0.6','h5py'],
                      'plot':['matplotlib'],},
      python_requires='>=3.6',
	  )
