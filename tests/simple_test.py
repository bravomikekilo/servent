import h5py as h5
import servent
import numpy as np

def integrity_test():
    try:
        with servent.Archive('test') as archive:

            label = archive.getLogger('label', (10,))

            for i in range(1000):
                if i == 768:
                    raise ValueError('intented')
                label.log(i * np.ones((10,)))

    except Exception as e:
        if e.args[0] != 'intented':
            raise e

    with h5.File('test.hdf5', 'r') as f:
        label = f['default/label']
        assert label.shape == (768, 10)
        for i in range(768):
            assert np.all(label[i] == i * np.ones(10,))


def scaler_test():
    try:
        with servent.Archive('test') as archive:

            label = archive.getLogger('label', None)

            for i in range(1000):
                if i == 768:
                    raise ValueError('intented')
                label.log(i)

    except Exception as e:
        if e.args[0] != 'intented':
            raise e

    with h5.File('test.hdf5', 'r') as f:
        label = f['default/label']
        assert label.shape == (768,)
        for i in range(768):
            assert label[i] == i, 'content error'


def multi_dimension_test():
    try:
        with servent.Archive('test') as archive:

            label = archive.getLogger('label', None)

            for i in range(1000):
                if i == 768:
                    raise ValueError('intented')
                label.log(i)

    except Exception as e:
        if e.args[0] != 'intented':
            raise e

    with h5.File('test.hdf5', 'r') as f:
        label = f['default/label']
        assert label.shape == (768,)
        for i in range(768):
            assert label[i] == i, 'content error'

