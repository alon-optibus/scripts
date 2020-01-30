from functools import lru_cache
from typing import Any
from unittest import TestCase

from my.utils import get_attr_repr, exception_eq


########################################################################################################################
# <editor-fold desc="dummy objects">


class AnyDummy:
    __slots__ = 'name', '__dict__'

    cache: dict

    def __new__(cls, name=None, **kw) -> Any:

        if name is None:
            new = super().__new__(cls)

        else:
            try:
                new = cls.cache[name]
            except KeyError:
                cls.cache[name] = new = super().__new__(cls)

        new.name = name
        new.__dict__.update(kw)

        return new

    def __repr__(self) -> str:
        return f'Dummy({get_attr_repr(self, "name", "")})'

    pass


class DummyType (type):
    __slots__ = ()

    cache = {}

    def __new__(mcs, name=None, bases=(), namespace=None):

        try:
            return mcs.cache[name]
        except KeyError:
            pass

        if namespace is None:
            namespace = {}

        namespace['cache'] = {}

        if name is None:
            return super().__new__(
                mcs,
                f'{getattr(mcs, "__name__", "")}()',
                bases + (AnyDummy,),
                namespace,
            )

        mcs.cache[name] = new = super().__new__(
            mcs,
            f'{getattr(mcs, "__name__", "")}({name})',
            bases + (AnyDummy,),
            namespace,
        )

        return new

    def __init__(cls, *a, **kw):
        pass


Dummy = DummyType()


# </editor-fold>
# <editor-fold desc="dummy exceptions">


class AnyDummyException (Exception):
    __eq__ = exception_eq
    __str__ = Exception.__repr__
    __new__ = lru_cache(maxsize=None, typed=True)(Exception.__new__)

    def raise_(self):
        raise self

    pass


class DummyException (type):

    cache = {}

    def __new__(mcs, name, bases=(), namespace={}):

        try:
            return mcs.cache[name]
        except KeyError:
            pass

        mcs.cache[name] = new = super().__new__(
            mcs,
            f'{getattr(mcs, "__name__", "")}({name})',
            bases + (AnyDummyException,),
            namespace,
        )

        return new


def raise_dummy_exception(name, *args):
    raise DummyException(name)(*args)


# </editor-fold>
########################################################################################################################


class MyTestCase (TestCase):
    __slots__ = ()

    def assertType(
            self,
            value,
            type_,
            msg=None,
    ):
        self.assertIs(type(value), type_, msg=msg)

    def assertException(
            self,
            exception: BaseException,
            exc_type: [BaseException],
            *args,
            msg=None,
    ):
        self.assertType(exception, exc_type, msg=msg)
        self.assertEqual(exception.args, args, msg=msg)


########################################################################################################################
