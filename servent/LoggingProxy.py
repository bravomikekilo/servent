import os

_join = os.path.join


class LoggingProxy(object):

    def __init__(self, visualLogger, archive, logger):
        super(LoggingProxy, self).__init__()
        self.run = 'default'
        self.visual = visualLogger
        self.archive = archive
        self.logger = logger

    def __enter__(self):
        return self

    def in_run(self, name):
        self.visual.mode(name)
        self.run = name
        self.archive.set_run(name)
        return self

    def __exit__(self, type, value, trace):
        self.run = 'default'
        self.archive.back_default()
        self.visual.__exit__(type, value, trace)

    def image(self, key):
        visual_logger = self.visual.image(_join('image', key))
        return ImageEndPoint(visual_logger)


    def tensor(self, key, shape):
        archive_logger = self.archive.getLogger(_join('tensor', key), shape)
        return TensorEndPoint(archive_logger)


    def scalar(self, key, as_text=False):
        archive_logger = self.archive.getLogger(_join('scalar', key), None)
        visual_logger = self.visual.scalar(_join('scalar', key))
        if not as_text:
            return ScalarEndPoint(archive_logger, visual_logger)
        else:
            return ScalarEndPoint(archive_logger, visual_logger, self.text(key))


    def scalarTuple(self, keys, as_text=False):
        loggers = [self.scalar(key, as_text=as_text) for key in keys]
        return ScalarTupleEndPoint(loggers)


    def text(self, key):
        return TextEndPoint(key, self.logger)



class ImageEndPoint(object):

    def __init__(self, visual_logger):
        super(ImageEndPoint, self).__init__()
        self.logger = visual_logger

    def __call__(self, step, X):
        self.logger.add_record(step, X)


class TensorEndPoint(object):

    def __init__(self, archive_logger):
        super(TensorEndPoint, self).__init__()
        self.logger = archive_logger

    def __call__(self, step, X):
        self.logger.log(X)


class ScalarEndPoint(object):

    def __init__(self, archive_logger, visual_logger, logger=None):
        super(ScalarEndPoint, self).__init__()
        self.archive = archive_logger
        self.visual = visual_logger
        self.logger = logger

    def __call__(self, step, X):
        self.archive.log(X)
        self.visual.add_record(step, X)
        if self.logger is not None:
            self.logger(step, X)


class ScalarTupleEndPoint(object):

    def __init__(self, scalarLoggers):
        super(ScalarTupleEndPoint, self).__init__()
        self.loggers = scalarLoggers

    def __call__(self, step, values):
        for v, logger in zip(values, self.loggers):
            logger(step, v)


class TextEndPoint(object):

    def __init__(self, key, logger):
        super(TextEndPoint, self).__init__()
        self.key = key
        self.logger = logger

    def __call__(self, step, info):
        self.logger.info('#{} {}: {}'.format(step ,self.key, info))
