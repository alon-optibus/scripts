from __future__ import print_function, division

import unittest

from my.utils import KeyManager, inf
from my.unitest_utils import Dummy

########################################################################################################################


class TestKeyManager (unittest.TestCase):
    
    def test__(self):

        km = KeyManager()

        for obj in [
            'wow',
            42,
            4.2,
            inf,
            (inf, 'wow')
        ]:
            key = km.key(obj)
            print(key)
            self.assertIs(key, obj)
            self.assertIs(km.get(key), obj)

            km.put(obj)

        with self.assertRaises(TypeError) as e:
            _ = km.key(Dummy(0))

        print(e.exception)

        km.key_by_typ[Dummy] = km.make_key_by_attrs(names=['name'])

        key = km.key(Dummy(0))
        print(key)

        km.put(Dummy(0))

        self.assertIn(key, km.ref)
        self.assertEqual(len(km.ref), 1)

        self.assertIs(km.get(key), Dummy(0))

        del km.ref[key]

        class KeyForDummy (km.KeyWithType):
            __slots__ = ()

            @property
            def name(self):
                return self.key[0]

            def __repr__(self):
                return '{}({}, name={})'.format(
                    type(self).__name__,
                    self.typ.__name__,
                    repr(self.name),
                )

            pass
        
        km.key_by_typ[Dummy] = km.make_key_by_attrs(names=['name'], key_with_type=KeyForDummy)

        key = km.key(Dummy(0))
        print(key)

        km.put(Dummy(0))

        self.assertIn(key, km.ref)
        self.assertEqual(len(km.ref), 1)

        self.assertIs(km.get(key), Dummy(0))

        pass
    
    pass


########################################################################################################################
