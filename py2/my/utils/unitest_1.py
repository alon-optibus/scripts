from __future__ import print_function, division

########################################################################################################################
# <editor-fold desc="dummy objects">
from my.utils import get_obj_type_name, join_repr, iget_attr, get_attr


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

        return 'Dummy({})'.format(', '.join([get_attr(self, "name", "", f=repr)] + [
            '{}={}'.format(key, repr(val))
            for key, val in self.__dict__.items()
        ]))

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

    __str__ = Exception.__repr__

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

        mcs.cache[name] = new = super(DummyException, mcs).__new__(
            mcs,
            '{}({})'.format(getattr(mcs, "__name__", ""), name),
            bases + (AnyDummyException,),
            namespace,
        )

        return new

    def wrap(cls, func):

        def wrapper(*args, **kwargs):

            value = func(*args, **kwargs)

            info = CallInfoForDummyExceptionWrapper(
                func=func,
                args=args,
                kwargs=kwargs,
                value=value,
            )

            raise cls(info)

        return wrapper

    pass


class CallInfoForDummyExceptionWrapper (object):

    __slots__ = (
        'func',
        'args',
        'kwargs',
        'value',
    )

    _fields = (
        'func_name',
        'args',
        'kwargs',
        'value',
    )

    @property
    def func_name(self):
        return self.func.__name__

    def __init__(
            self,
            func=None,
            args=None,
            kwargs=None,
            value=None,
    ):
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.value = value
        pass

    def __repr__(self):
        return '{}({})'.format(
            get_obj_type_name(self, ''),
            join_repr(iget_attr(self, self._fields), kw=self._fields),
        )

    pass


# </editor-fold>
########################################################################################################################
