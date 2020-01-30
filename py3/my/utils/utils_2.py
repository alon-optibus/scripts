from functools import partial
from itertools import chain
from types import MethodType
from typing import Any, Iterable, Optional, Callable, TypeVar, Type

from toolz import identity

from my.utils.iter_1 import all_iter_eq

T0 = TypeVar('T0')

########################################################################################################################
# <editor-fold desc="missing">


class MissingType:
    __slots__ = ()

    DEFAULT_EXCEPTION_FOR_BOOL = ValueError('unable to infer bool value from missing value')

    def __repr__(self):
        return '<missing>'

    def __bool__(self):
        raise self.DEFAULT_EXCEPTION_FOR_BOOL


MISSING = MissingType()

# </editor-fold>
# <editor-fold desc="exceptions">

DEFAULT_EXCEPTIONS = {}


def default_exception(type_: Type[Exception], cache=DEFAULT_EXCEPTIONS):

    try:
        return cache[type_]
    except KeyError:
        pass

    cache[type_] = new = type_()
    return new


class MyException (Exception):
    __slots__ = ()
    __str__ = Exception.__repr__

    default_exceptions = DEFAULT_EXCEPTIONS

    def __eq__(self, other):
        return type(self) is type(other) and attr_eq('args', self, other)

    @classmethod
    def default(cls):
        return default_exception(cls)


class UndefinedException (MyException):
    __slots__ = ()


class IsMissing (MyException):
    __slots__ = ()


def to_exception(*value, default: Type[Exception] = UndefinedException) -> BaseException:

    if len(value) == 1 and isinstance(value, BaseException):
        return value

    return default(*value)


def raise_(
        exception: BaseException = UndefinedException.default()
):
    raise exception


def raise_if(
        flag: Any,
        exception: BaseException = UndefinedException.default(),
):
    return raise_(exception) if flag else flag


def exception_eq(
        a: BaseException,
        b: BaseException,
) -> bool:
    if not isinstance(a, BaseException):
        raise TypeError(get_type_name(a))
    return type(a) is type(b) and attr_eq('args', a, b)


# </editor-fold>
# <editor-fold desc="assertions">


def valid(value, default=MISSING, missing=MISSING, func: Callable = identity, *, _scope=BaseException):
    return assert_cls_not(value=value, scope=_scope, default=default, missing=missing, func=func)


def unvalid(value, default=MISSING, missing=MISSING, func: Callable = identity, *, _scope=BaseException):
    return assert_cls(value=value, scope=_scope, default=default, missing=missing, func=func)


def assert_cls_not(value, scope: type, default=MISSING, missing=MISSING, func: Callable = identity):
    return unmissing(default, missing) if isinstance(func(value), scope) else value


def assert_cls(value, scope: type, default=MISSING, missing=MISSING, func: Callable = identity):
    return value if isinstance(func(value), scope) else unmissing(default, missing)


def assert_(value, default=MISSING, missing=MISSING, func: Callable = identity):
    return value if func(value) else unmissing(default, missing)


def assert_is(value, other, default=MISSING, missing=MISSING, func: Callable = identity):
    return value if func(value) is other else unmissing(default, missing)


def assert_is_not(value, other, default=MISSING, missing=MISSING, func: Callable = identity):
    return value if func(value) is not other else unmissing(default, missing)


def assert_seq(value, iterable: Iterable, default=MISSING, missing=MISSING, func: Callable = iter):
    return value if all_iter_eq(func(value), iterable) else unmissing(default, missing)


def assert_set(value, iterable: Iterable, default=MISSING, missing=MISSING, func: Callable = set):
    return value if all(item in func(value) for item in iterable) else unmissing(default, missing)


def unmissing(value, missing=MISSING, exception=IsMissing.default()):
    return raise_(exception) if value is missing else value


# </editor-fold>
# <editor-fold desc="lookup">


def get_item(
        source: Any,
        key: Any,
        default: Any = MISSING,
        missing: Any = MISSING,
) -> Any:

    try:
        return source[key]

    except LookupError:

        if default is missing:
            raise

        return default


def get_attr(
        source: Any,
        name: str,
        default: Any = MISSING,
        missing: Any = MISSING,
) -> Any:

    try:
        return getattr(source, name)

    except AttributeError:

        if default is missing:
            raise

        return default


def get_attr_repr(
        source: Any,
        name: str,
        default: Any = MISSING,
        missing: Any = MISSING,
) -> Any:

    try:
        value = getattr(source, name)

    except AttributeError:

        if default is missing:
            raise

        return default

    return repr(value)


def get_env(
        name: str,
        default: Any = MISSING,
        missing: Any = MISSING,
) -> Any:

    from os import getenv

    x = Stack()

    return (
            x(getenv(name)) is None
            and x(default) is missing
            and -x.init(LookupError(f'env: {repr(name)}'))
            or x.valid().pop()
    )

# </editor-fold>
# <editor-fold desc="attr">


def get_type_name(
        value: Any,
        default: Any = '<unknown type>',
        missing: Any = None,
) -> str:
    return get_attr(type(value), '__name__', default=default, missing=missing)


def attr_eq(name, a, b, missing=MISSING):
    return getattr(a, name, missing) == getattr(b, name, missing)


def attr_is(name, a, b, missing=MISSING):
    return getattr(a, name, missing) is getattr(b, name, missing)


def attr_same_status(name, a, b):
    return hasattr(a, name) == hasattr(b, name)


def tuple_attr(source, name):
    try:
        return getattr(source, name),
    except AttributeError:
        return ()


def set_attr_default(
        target: Any,
        name: str,
        value: Any = MISSING,
        missing: Any = MISSING,
) -> Any:

    if value is not missing:
        setattr(target, name, value)

    return target


# </editor-fold>
########################################################################################################################


class DualProperty:
    __slots__ = 'getter',

    # <editor-fold desc="constractors">

    def __init__(self, getter: Callable[[Optional[T0], Type[T0]], Any]) -> Any:
        self.getter = getter

    @classmethod
    def bound_ins_or_new(cls, func: Callable):
        return cls(partial(cls.get__bound_ins_or_new, func))

    @classmethod
    def bound_ins_or_cls(cls, func: Callable):
        return cls(partial(cls.get__bound_ins_or_cls, func))

    @classmethod
    def bound_ins_and_cls(cls, func: Callable):
        return cls(partial(cls.get__bound_ins_and_cls, func))

    @classmethod
    def bound_ins_or_make(cls, make, func=None):
        return (
            partial(cls.bound_ins_or_make, make)
            if func is None else
            cls(partial(cls.get__bound_ins_or_make, make, func))
        )

    @classmethod
    def bound_make(cls, make, func=None):
        return (
            partial(cls.bound_make, make)
            if func is None else
            cls(partial(cls.get__bound_make, make, func))
        )

    # </editor-fold>
    # <editor-fold desc="getters">

    def __get__(self, ins: Optional[T0], cls: Type[T0]):
        return self.getter(ins, cls)

    @staticmethod
    def get__bound_ins_or_new(func: Callable, ins: Optional[T0], cls: Type[T0]):
        return MethodType(func, cls() if ins is None else ins)

    @staticmethod
    def get__bound_ins_or_cls(func: Callable, ins: Optional[T0], cls: Type[T0]):
        return MethodType(func, cls if ins is None else ins)

    @staticmethod
    def get__bound_ins_and_cls(func: Callable, ins: Optional[T0], cls: Type[T0]):
        return partial(func, ins, cls)

    @staticmethod
    def get__bound_ins_or_make(make: Callable, func: Callable, ins: Optional[T0], cls: Type[T0]):
        return MethodType(func, make(cls) if ins is None else ins)

    @staticmethod
    def get__bound_make(make: Callable, func: Callable, ins: Optional[T0], cls: Type[T0]):
        return MethodType(func, make(ins, cls))

    # </editor-fold>


########################################################################################################################


class Stack (list):
    # <editor-fold desc="properties">

    __slots__ = ()

    @property
    def len(self) -> int:
        return len(self)

    @property
    def is_empty(self) -> bool:
        return len(self) == 0

    @property
    def is_single(self) -> bool:
        return len(self) == 1

    @property
    def is_multiple(self):
        return len(self) > 1

    @property
    def value(self):
        return self[0] if self.is_single else self

    @property
    def type(self):
        return type(self.value)

    @property
    def is_exception(self, _scope=BaseException):
        return isinstance(self.value, _scope)

    def __repr__(self) -> str:
        return f'{get_type_name(self)}({super().__repr__()})'

    # </editor-fold>
    # <editor-fold desc="constructors">

    def __init__(self, *values) -> None:
        super().__init__(values)

    def init(self, *values, _base_init=list.__init__) -> 'Stack':
        _base_init(self, values)
        return self

    @DualProperty.bound_ins_or_new
    def from_iter(self, source: Iterable, *, _base_init=list.__init__) -> 'Stack':
        _base_init(self, source)
        return self

    # </editor-fold>
    # <editor-fold desc="utils">

    def copy(self) -> 'Stack':
        cls = type(self)
        new = cls.__new__(cls)
        new.from_iter(self)
        return new

    def append(self, x: Any) -> 'Stack':
        super().append(x)
        return self

    def clear(self) -> 'Stack':
        super().clear()
        return self

    def chop(self):
        self.pop()
        return self

    def extend(self, iterable: Iterable) -> 'Stack':
        super().extend(iterable)
        return self

    def reverse(self) -> 'Stack':
        super().reverse()
        return self

    def sort(self, *, key: 'Optional[Callable]' = ..., reverse: bool = ...) -> 'Stack':
        super().sort(key=key, reverse=reverse)
        return self

    def map(self, func):
        return self.from_iter(list(map(func, self)))

    def expand(self):
        return self.from_iter(list(chain.from_iterable(self)))

    def stack(self, func=None):
        return type(self)(self) if func is None else self.init(func(self))

    # </editor-fold>
    # <editor-fold desc="context manager">

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val is not None:
            self.init(exc_val)
        return True

    # </editor-fold>
    # <editor-fold desc="handle exceptions">

    def unmissing(self, value, missing=MISSING):
        return self.raise_() if value is missing else self.init(value)

    def raise_(self):
        raise self[0] if self.is_exception else UndefinedException(*self)

    # </editor-fold>
    # <editor-fold desc="assertions">

    def valid(self, default=MISSING, missing=MISSING, func: Callable = identity, *, _scope=BaseException):
        return self.assert_cls_not(scope=_scope, default=default, missing=missing, func=func)

    def unvalid(self, default=MISSING, missing=MISSING, func: Callable = identity, *, _scope=BaseException):
        return self.assert_cls(scope=_scope, default=default, missing=missing, func=func)

    def assert_cls_not(self, scope: type, default=MISSING, missing=MISSING, func: Callable = identity):
        return self.unmissing(default, missing) if isinstance(func(self.value), scope) else self

    def assert_cls(self, scope: type, default=MISSING, missing=MISSING, func: Callable = identity):
        return self if isinstance(func(self.value), scope) else self.unmissing(default, missing)

    def assert_call(self, func, default=MISSING, missing=MISSING):
        return self if func(*self) else self.unmissing(default, missing)

    def assert_stack(self, default=MISSING, missing=MISSING, func: Callable = identity):
        return self if func(self) else self.unmissing(default, missing)

    def assert_(self, default=MISSING, missing=MISSING, func: Callable = identity):
        return self if func(self.value) else self.unmissing(default, missing)

    def assert_is(self, other, default=MISSING, missing=MISSING, func: Callable = identity):
        return self if func(self.value) is other else self.unmissing(default, missing)

    def assert_is_not(self, other, default=MISSING, missing=MISSING, func: Callable = identity):
        return self if func(self.value) is not other else self.unmissing(default, missing)

    def assert_seq(self, iterable: Iterable, default=MISSING, missing=MISSING, func: Callable = iter):
        return self if all_iter_eq(func(self), iterable) else self.unmissing(default, missing)

    def assert_set(self, iterable: Iterable, default=MISSING, missing=MISSING, func: Callable = set):
        return self if all(item in func(self) for item in iterable) else self.unmissing(default, missing)

    # </editor-fold>
    # <editor-fold desc="operators">

    def __mul__(self, func):  # _ * _
        return self.init(func(*self))

    def __pow__(self, func):  # _ ** _
        return self.from_iter(func(*self))

    __truediv__ = append  # _ / _
    __floordiv__ = extend  # _ // _
    # __neg__ = chop  # -_
    __invert__ = clear  # ~_
    __or__ = map  # _ | _

    def __neg__(self):
        return False

    def __pos__(self):
        return True

    def __rtruediv__(self, value):
        self.append(value)
        return value

    def __call__(self, *values, _base_init=list.__init__):
        _base_init(self, values)
        return self.value

    # </editor-fold>
    pass


########################################################################################################################
