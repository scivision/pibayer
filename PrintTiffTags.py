#!/usr/bin/env python
"""
Simply prints tags requested in a TIFF image
"""
from pathlib import Path
import tifffile

def printtags(fn:Path, tlist:list):
    fn = Path(fn).expanduser()

    with tifffile.TiffFile(str(fn)) as tif:
        for i,page in enumerate(tif):
            print('\n** Image ',i,' **')
            for tag in page.tags.values():
                t = tag.name, tag.value
                if tlist:
                    if tag.name in tlist:
                        print(t[0],t[1])
                else:
                    print(t[0],t[1])
            

if __name__ == '__main__':
    from argparse import ArgumentParser
    p = ArgumentParser()
    p.add_argument('fn',help='TIFF file to print tags from')
    p.add_argument('-t','--tags',help='tag numbers to print',nargs='+',type=str)
    p = p.parse_args()


    printtags(p.fn,p.tags)
