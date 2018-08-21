#!/usr/bin/env python
"""
Simply prints tags requested in a TIFF image.

Not a reliable way to transmit metadata--use NetCDF4/HDF5 instead in general.
"""
from pathlib import Path
import tifffile
from argparse import ArgumentParser


def main():
    p = ArgumentParser()
    p.add_argument('fn', help='TIFF file to print tags from')
    p.add_argument('-t', '--tags', help='tag numbers to print', nargs='+', type=str)
    p = p.parse_args()

    printtags(p.fn, p.tags)


def printtags(fn: Path, tlist: list):
    fn = Path(fn).expanduser()

    with tifffile.TiffFile(str(fn)) as tif:
        for i, page in enumerate(tif):
            print('\n** Image ', i, ' **')
            for tag in page.tags.values():
                t = tag.name, tag.value
                if tlist:
                    if tag.name in tlist:
                        print(t[0], t[1])
                else:
                    print(t[0], t[1])


if __name__ == '__main__':
    main()
