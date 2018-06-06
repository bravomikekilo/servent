import h5py as h5


def hdf5_summary(file):

    def summary_helper(file):
        print('keys:')
        for k in file.keys():
            print(k, file[k].shape)

    if type(file) == str:
        with h5.File(file) as f:
            summary_helper(f)
    else:
        summary_helper(file)


