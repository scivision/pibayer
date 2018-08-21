#!/usr/bin/env python
import pytest
import tempfile
from pibayer import pibayerraw
#
Nimg = 2
exposure_sec = 0.1


def test_tiff():
    bit8 = False

    with tempfile.NamedTemporaryFile(suffix='.tif')[1] as fn:
        pibayerraw(Nimg, exposure_sec, bit8, preview=None, outfn=fn)


def test_h5():
    bit8 = False

    with tempfile.NamedTemporaryFile(suffix='.h5')[1] as fn:
        pibayerraw(Nimg, exposure_sec, bit8, preview=None, outfn=fn)


def test_gpu():
    bit8 = False

    pibayerraw(Nimg, exposure_sec, bit8, preview=5.)


def test_matplotlib():
    bit8 = False

    pibayerraw(Nimg, exposure_sec, bit8, preview='mpl')


if __name__ == '__main__':
    pytest.main(['-x', __file__])
