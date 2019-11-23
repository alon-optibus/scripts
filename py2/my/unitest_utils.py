from __future__ import print_function, division
from my.utils import get_attr

# <editor-fold desc="dummy objects">


class AnyDummy (object):
    __slots__ = 'name', '__dict__'

    cache = {}

    def __new__(cls, name=None, **kw):

        if name is None:
            new = super(AnyDummy, cls).__new__(cls)

        else:
            try:
                new = cls.cache[name]
            except KeyError:
                cls.cache[name] = new = super(AnyDummy, cls).__new__(cls)

        new.name = name
        new.__dict__.update(kw)

        return new

    def __repr__(self):
        return 'Dummy({})'.format(get_attr(self, "name", f=repr))

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
            return super(DummyType, mcs).__new__(
                mcs,
                '{}()'.format(getattr(mcs, "__name__", "")),
                bases + (AnyDummy,),
                namespace,
            )

        mcs.cache[name] = new = super(DummyType, mcs).__new__(
            mcs,
            '{}({})'.format(getattr(mcs, "__name__", ""), name),
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

    cache = {}

    def __new__(cls, *args):
        try:
            return cls.cache[args]
        except (KeyError, TypeError):
            pass

        cls.cache[args] = new = super(AnyDummyException, cls).__new__(cls)

        return new

    __str__ = Exception.__repr__

    def __eq__(self, o):
        return type(self) is type(o) and getattr(self, 'args') == getattr(o, 'args')

    def raise_(self):
        raise self


class DummyException (type):

    cache = {}

    def __new__(mcs, name, bases=(), namespace={}):

        try:
            return mcs.cache[name]
        except KeyError:
            pass

        mcs.cache[name] = new = super(DummyException, mcs).__new__(
            mcs,
            '{}({})'.format(getattr(mcs, "__name__", ""), name),
            bases + (AnyDummyException,),
            namespace,
        )

        return new


def raise_dummy_exception(name, *args):
    raise DummyException(name)(*args)


# </editor-fold>
