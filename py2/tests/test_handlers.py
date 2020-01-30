from __future__ import print_function, division

import unittest

from my.utils.handlers_1 import *

########################################################################################################################


class DummyHandler (HandlerBase):
    __slots__ = (
        'index',
    )
    pass


class DummyOwner (HandlerBase):
    __slots__ = ()
    pass


o = DummyOwner()
h0 = DummyHandler(owner=o)

x = HandlerDict(owner=o, handler_type=DummyHandler)

x.put(h0)


########################################################################################################################


class Test0 (unittest.TestCase):
    
    def test__001(self):
        print(x, list(x))
        pass
    
    pass


########################################################################################################################
