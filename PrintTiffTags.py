#!/usr/bin/env python
"""
Simply prints tags requested in a TIFF image
"""
from pathlib import Path
import tifffile

def printtags(fn:Path, tlist:list):
    fn = Path(fn).expanduser()

    with tifffile.TiffFile(str(fn)) as tif:
        for page in tif:
            for tag in page.tags.values():
                t = tag.name, tag.value
                if tag.name in tlist:
                    print(t)

if __name__ == '__main__':
    from argparse import ArgumentParser
    p = ArgumentParser()
    p.add_argument('fn',help='TIFF file to print tags from')
    p.add_argument('-t','--tags',help='tag numbers to print',nargs='+',default=['33434'],type=str)
    p = p.parse_args()


    printtags(p.fn,p.tags)