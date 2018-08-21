from pathlib import Path
import xarray

KEY = 'imgs'  # handle to write inside the output file
CLVL = 1  # ZIP compression level


def writeframes(outfn: Path, img: xarray.DataArray):
    """writes image stack to disk"""
    assert img.ndim == 3

    if outfn is None:
        return

    outfn = Path(outfn).expanduser()

    print('writing', outfn)

    if outfn.suffix == '.nc':
        # chunksizes made only few % difference in save time and size
        # fletcher32 had no noticable impact
        # complvl+1 had little useful impact
        enc = {KEY: {'zlib': True, 'complevel': CLVL, 'fletcher32': True,
                     'chunksizes': (1, img.shape[1], img.shape[2])}}
        img.to_netcdf(outfn, mode='w', encoding=enc)
    elif outfn.suffix == '.h5':  # HDF5
        import h5py
        with h5py.File(outfn, 'w') as f:
            f.create_dataset(KEY,
                             data=img.values,
                             shape=img.shape,
                             dtype=img.dtype,
                             compression='gzip',
                             compression_opts=CLVL,
                             chunks=(1, img.shape[1], img.shape[2]),
                             shuffle=True, fletcher32=True)

            for k, v in img.attrs.items():
                f[k] = v
    else:  # assume stacked image format
        import imageio
        imageio.mimwrite(outfn, img.values)
