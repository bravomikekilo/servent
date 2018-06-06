import logging
from servent import LoggingProxy, Archive
import visualdl
import h5py as h5
import numpy as np


def scalar_test():

    log_dir = 'visual_test'
    visualLogger = visualdl.LogWriter(log_dir, sync_cycle=20)
    logging.basicConfig(format='[%(asctime)s][%(levelname)s] %(message)s')
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)


    try:
        with Archive('proxy_test') as archive:
            proxy = LoggingProxy(visualLogger, archive ,logger)
            with proxy.in_run('train'):
                hello = proxy.scalar('hello')

            for i in range(1000):
                if i == 768:
                    raise ValueError('intented')
                hello(i, i)
    except Exception as e:
        if e.args[0] != 'intented':
            raise e

    with h5.File('proxy_test.hdf5', 'r') as f:
        label = f['train/scalar/hello']
        assert label.shape == (768,)
        for i in range(768):
            assert label[i] == i, 'content error'


def tensor_test():

    log_dir = 'visual_test'
    visualLogger = visualdl.LogWriter(log_dir, sync_cycle=20)
    logging.basicConfig(format='[%(asctime)s][%(levelname)s] %(message)s')
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)


    try:
        with Archive('proxy_test') as archive:
            proxy = LoggingProxy(visualLogger, archive ,logger)
            with proxy.in_run('train'):
                hello = proxy.tensor('tensor', (10,))

            for i in range(1000):
                if i == 768:
                    raise ValueError('intented')
                hello(i,  i * np.ones((10,)))
    except Exception as e:
        if e.args[0] != 'intented':
            raise e

    with h5.File('proxy_test.hdf5', 'r') as f:
        label = f['train/tensor/tensor']
        assert label.shape == (768, 10)
        for i in range(768):
            assert np.all(label[i] == i * np.ones(10,))

