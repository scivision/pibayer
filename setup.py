#!/usr/bin/env python
from setuptools import setup
import subprocess,sys,os

with open('requirements.txt', 'r') as f:
    req = f.read().split('\n')
    req = [os.path.basename(sys.executable)+'-'+r for r in req if r]

try:
    cmd = ['sudo','apt-get','install'] + req
    print(' '.join(cmd))
    subprocess.check_call(cmd)
    ok=True
except Exception as e:
    ok = False

setup(name='pibayer',
	  description='Python raw Bayer data from raspberry Pi camera',
	  url='https://github.com/scivision/raspberrypi_raw_camera/',
      install_requires=['pathlib2'],
      packages=['pibayer']
	  )

if not ok:
    print('\n *** please execute')
    print(' '.join(cmd))
