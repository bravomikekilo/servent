import os
import numpy as np
import h5py as h5

def data_summary(X, to_console=False):
    # mean, var, shape, dtype
    ma = np.max(X)
    mi = np.min(X)
    mean = np.mean(X)
    var = np.var(X)
    shape = X.shape
    dtype = X.dtype
    if to_console:
        print("    max: {}".format(ma))
        print("    min: {}".format(mi))
        print("    mean: {}".format(mean))
        print("    var: {}".format(var))
        print("    shape: {}".format(shape))
        print("    dtype: {}".format(dtype))
    return mean, var, shape, dtype

def inspect_file(filename):
    basename = os.path.basename(filename)
    [_, ext] = basename.rsplit('.', maxsplit=1)
    print('filename: {}'.format(filename))
    if ext == 'npy':
        array = np.load(filename)
        print('filename: {}'.format(basename))
        data_summary(array, to_console=True)

    elif ext in ['h5', 'mat', 'hdf5']:
        with h5.File(filename) as f:
            for k in f.keys():
                print('  array under key "{}":'.format(k))
                data_summary(f[k], to_console=True)

    else:
        print("unknown filename extension")
