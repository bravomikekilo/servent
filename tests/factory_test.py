

from testFactory import create

def factory_test():
    onetwothree = create('123')
    assert onetwothree.arr == [1, 2, 3]

    array = create('array', 'a', 'b', 'c')
    assert array.content == ['a', 'b', 'c']

    kwargone = create('kwargone', keyword='test')
    assert kwargone.content == 'test'

    d = {'1': 'one', '2': 'two', '3': 'three'}
    keyword = create('keyword', **d)
    assert keyword.content == d

    function = create('function')
    assert function == 'example_function_output'






