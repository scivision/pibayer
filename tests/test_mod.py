#!/usr/bin/env python
import pytest
import pibayer

Nimg = 2
exposure_sec = 0.1


def test_acq_seq():
    img = pibayer.bayerseq(Nimg, exposure_sec)
    assert img.shape[0] == Nimg


if __name__ == "__main__":
    pytest.main(["-xv", __file__])
