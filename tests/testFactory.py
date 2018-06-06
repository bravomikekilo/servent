from servent import Factory

_factory = Factory()

register = _factory.register

create = _factory.interface

@register('123')
class OneTwoThree(object):

    def __init__(self):
        super(OneTwoThree, self).__init__()
        self.arr = [1, 2, 3]


@register('array')
class ArrayContent(object):

    def __init__(self, *args):
        super(ArrayContent, self).__init__()
        self.content = [arg for arg in args]



@register('kwargone')
class KwArgOne(object):

    def __init__(self, keyword='next'):
        super(KwArgOne, self).__init__()
        self.content = keyword


@register('keyword')
class keyword(object):

    def __init__(self, **kwargs):
        super(keyword, self).__init__()
        self.content = kwargs

@register('function')
def example_func():
    return 'example_function_output'






