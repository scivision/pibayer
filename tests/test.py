#!/usr/bin/env python
from numpy.testing import run_module_suite
from tempfile import mkstemp
#
from pibayer import  pibayerraw
#
Nimg = 2
exposure_sec=0.1

def test_tiff():
    bit8 = False

    pibayerraw(Nimg, exposure_sec, bit8, preview=None,
               outfn=mkstemp('.tif')[1])

def test_h5():
    bit8 = False

    pibayerraw(Nimg, exposure_sec, bit8, preview=None,
               outfn=mkstemp('.h5')[1])

def test_gpu():
    bit8 = False

    pibayerraw(Nimg, exposure_sec, bit8, preview=5.)


def test_matplotlib():
    bit8 = False

    pibayerraw(Nimg, exposure_sec, bit8, preview='mpl')


if __name__ == '__main__':
    run_module_suite()