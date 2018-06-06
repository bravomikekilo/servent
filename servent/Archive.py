import h5py as h5
import numpy as np
import logging


class Archive(object):

    def __init__(self, experiment):
        super(Archive, self).__init__()
        self.filename = experiment + '.hdf5'
        self.file = None
        self.loggers = dict()
        self.runs = dict()

    def __enter__(self):
        print('create archive file')
        self.file = h5.File(self.filename, 'w')
        self.runs['default'] = self.file.create_group('default')
        self.run = self.runs['default']
        return self

    def set_run(self, run):
        if run in self.runs:
            self.run = self.runs[run]
        else:
            self.run = self.file.create_group(run)
            self.runs[run] = self.run

    def back_default(self):
        self.run = self.runs['default']

    def getLogger(self, key, shape, axis=0):
        if key in self.loggers:
            return self.loggers[key]
        else:
            base_shape = [] if shape is None else list(shape)
            maxshape = tuple([None] + base_shape)
            data_shape = tuple([1] + base_shape)
            print('create dataset')
            dataset = self.run.create_dataset(key, data_shape, maxshape=maxshape)
            logger = ArchiveLogger(dataset, key, shape, axis=axis)
            self.loggers[key] = logger
            return logger


    def __exit__(self, type, value, traceback):
        print('on exit')
        if self.file is not None:
            for _, logger in self.loggers.items():
                logger.flush()
            print('close file')
            self.file.close()



class ArchiveLogger(object):

    def __init__(self, dataset, key, shape, axis=0, buffer_size=100):
        super(ArchiveLogger, self).__init__()
        self.key = key
        self.shape = shape
        self.dataset = dataset
        self.is_scaler = shape is None or shape == (1,)
        self.index = 0
        self.buffer_size = buffer_size
        self.buffer = self.create_buffer(self.buffer_size)
        self.buffer_index = 0


    def create_buffer(self, buffer_size):
        if self.is_scaler:
            return np.zeros((100,))
        else:
            buffer_shape = tuple([100] + list(self.shape))
            return np.zeros(buffer_shape)

    def log(self, info):

        def sample_log(info):
            if self.buffer_index == self.buffer_size:
                self.flush()
            self.buffer[self.buffer_index] = info
            self.buffer_index += 1

        if np.isscalar(info):
            sample_log(info)
            return
        info_shape = info.shape

        if len(info_shape) == len(self.shape):
            assert info_shape == self.shape, 'inconsistent info shape for key %s' % (self.key)
            sample_log(info)
        else:
            assert len(info_shape.shape) == len(self.shape) + 1, 'bad shape info for key %s' % (self.key)
            num_info = info_shape[0]
            if num_info > self.buffer_size:
                self.flush()
                self._write_to_dataset(info)
                return

            if num_info + self.buffer_index >= self.buffer_size:
                num_remain = self.buffer_size - self.buffer_index
                self.buffer[self.buffer_index:] = info[:num_remain]
                self.flush()
                self.buffer_index = num_info - num_remain
                self.buffer[:self.buffer_index] = info[num_remain:]
            else:
                self.buffer[self.buffer_index: self.buffer_index + num_info] = info


    def _write_to_dataset(self, array):
        l = array.shape[0]
        size = list(self.dataset.shape)
        size[0] = self.index + l
        print(size)
        self.dataset.resize(size)
        print(self.dataset.shape)
        print('Archive target shape', self.dataset[self.index: self.index + l].shape)
        print('Archive array shape', array.shape)
        self.dataset[self.index: self.index + l] = array
        self.index += l

    def flush(self):
        print('Archive flushing')
        self._write_to_dataset(self.buffer[:self.buffer_index])
        self.buffer_index = 0


