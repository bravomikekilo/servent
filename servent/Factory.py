
class Factory(object):

    def __init__(self):
        super(Factory, self).__init__()
        self.store = dict()

    @property
    def interface(self):

        def create(name, *args, **kwargs):
            return self.produce(name, *args, **kwargs)
        return create


    def add(self, k, v):
        if k in self.store:
            raise KeyError("can't register name {} twice!".format(v))
        self.store[k] = v

    @property
    def register(self):
        store = self.store
        # the register function, with parameter
        def register_func(name):
            def reg(f):
                if name in store:
                    raise KeyError("can't register name {} twice!".format(name))
                store[name] = f
                return f
            return reg

        return register_func

    def produce(self, name, *args, **kwargs):
        if name not in self.store:
            raise KeyError("name {} is not registered".format(name))
        return self.store[name](*args, **kwargs)


