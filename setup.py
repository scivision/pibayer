#!/usr/bin/env python
req = ['picamera','numpy','xarray','nose']
# %%
from setuptools import setup,find_packages

setup(name='pibayer',
      packages=find_packages(),
      author='Michael Hirsch, Ph.D.',
      version='0.6.0',
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
      install_requires=req,
      extras_require={'io':['tifffile','h5py','netcdf4'],
                      'plot':['matplotlib'],},
      python_requires='>=3.5',
      )
