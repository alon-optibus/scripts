from __future__ import division, print_function

from collections import defaultdict, OrderedDict
from functools import partial, wraps
from inspect import isgetsetdescriptor
from types import MethodType

from itertools import chain, imap, izip, repeat, starmap
from toolz import identity


########################################################################################################################
# <editor-fold desc="const">

NEW_LINE = '\n'

# </editor-fold>
########################################################################################################################
# <editor-fold desc="call statements">


def raise_(e):
    raise e


def pass_(*args, **kwargs):
    return


def get_(obj, key):
    return obj[key]


def yield_(obj):
    yield obj


def call_(f):
    return f()


# </editor-fold>
# <editor-fold desc="empty dict">


class EmptyDict (object):
    __slots__ = ()

    _instance = {}

    def __new__(cls):
        return cls._instance

    def __getitem__(self, key):
        raise KeyError(key)

    def get(self, key, default=None):
        return default

    def keys(self):
        return iempty

    def iterkeys(self):
        return iempty

    def __contains__(self, key):
        return False

    def __repr__(self):
        return '{}()'.format(get_obj_type_name(self))

    pass


empty_dict = EmptyDict._instance = object.__new__(EmptyDict)

# </editor-fold>
########################################################################################################################
# <editor-fold desc="exceptions">


class MissingError (Exception):
    pass


class MissingBoolError (MissingError, ValueError):
    """
    raise if try to interpret as boolean an object with no boolean sense (such as `MissingType`).
    """
    pass


class MissingCallableError (MissingError, TypeError):
    pass


class MissingAttrError (MissingError, AttributeError):
    pass


class UndefinedException (Exception):
    """
    raise as default exception.
    """
    pass


# </editor-fold>
# <editor-fold desc="missing">


class MissingType (object):
    """
    `MissingType` objects ment to indicate a missing value (like `None`).
    Unlike `None`, `MissingType` class is not a singlton and `MissingType` object raises `MissingBoolError` when
    interpreted as boolean. i.e:

    >> bool(MissingType())

    >> _ = not MissingType()

    >> _ = MissingType() and ...

    >> _ = MissingType() or ...

    >> _ = ... if MISSING else ...

    >> if MissingType():
    >>     ...

    >> while MissingType():
    >>     ...

    """

    __slots__ = ()

    DEFAULT_EXCEPTION_FOR_BOOL = MissingBoolError('unable to infer bool value from missing value')
    DEFAULT_EXCEPTION_FOR_CALL = MissingCallableError('callable is missing')
    DEFAULT_EXCEPTION_FOR_ATTR = MissingAttrError('attribute is missing')

    def __repr__(self):
        return '<missing>'

    def __nonzero__(self):
        raise self.DEFAULT_EXCEPTION_FOR_BOOL

    def __call__(self, *args, **kwargs):
        raise self.DEFAULT_EXCEPTION_FOR_CALL

    def __get__(self, instance, owner):
        raise self.DEFAULT_EXCEPTION_FOR_ATTR

    pass


MISSING = MissingType()

# </editor-fold>
# <editor-fold desc="unmissing">


def unmissing_strict(value, default=MISSING, missing=MISSING, f=identity, catch=LookupError, raise_=MissingError):
    """
    :type value: Any
    :type default: Any
    :type missing: Any
    :type f:
    :type catch:
    :type raise_:
    :rtype:
    """
    if value is missing:
        if default is missing:
            raise MissingError(missing)
        return default
    return value


def unmissing(missing, *values):
    return unmissing_iter(missing, values)


def unmissing_iter(missing, it):

    for value in it:
        if value is not missing:
            return value

    return missing


def call_with_missing_if_missing(f, value, missing=MISSING, args=(), kwargs={}):

    if value is missing:
        return f(missing)

    return value


def call_if_missing(f, value, missing=MISSING, args=(), kwargs={}):

    if value is missing:
        return f(*args, **kwargs)

    return value


# </editor-fold>
# <editor-fold desc="lookup">


def get_item(src, key, default=MISSING, missing=MISSING, f=identity, catch=LookupError):
    # return get_next_item(src, keys=yield_(key), default=default, missing=missing, f=f, catch=catch)

    try:
        value = src[key]
    except catch:
        if default is missing:
            raise
        return default
    else:
        return f(value)


def get_next_item(src, keys, default=MISSING, missing=MISSING, f=identity, catch=LookupError, raise_=LookupError):
    # return get_next(iget_item(src, keys, h=iraise), default=default, missing=missing, f=f, catch=catch)

    for key in keys:
        try:
            value = src[key]
        except catch:
            pass
        else:
            return f(value)

    if default is missing:
        raise raise_(keys)

    return default


def is_item_missing(obj, key, missing=MISSING):
    try:
        value = get_item(obj, key, default=missing, missing=missing)
    except LookupError:
        return True
    else:
        return value is missing


def get_lookup_keys(obj):

    if isinstance(obj, dict):
        return obj.iterkeys()

    try:
        keys = obj.keys
    except AttributeError:
        pass
    else:
        return keys()

    raise TypeError()

# </editor-fold>
########################################################################################################################
# <editor-fold desc="func">


def partial_(func, args=(), keywords={}):
    o = object.__new__(partial)
    o._func = func
    o._args = args
    o._keywords = keywords
    return o


def make_const(value):

    def const(*args, **kwargs):
        return value

    const.func_name = '{}({})'.format(const.func_name, repr(value))

    return const


def make_const_raise(e):

    def const_raise(*args, **kwargs):
        raise e

    const_raise.func_name = '{}({})'.format(const_raise.func_name, repr(e))

    return const_raise


def make_cache_by_kwargs(names):

    cache = {}

    def maker(func):

        @wraps(func)
        def wrapper(*args, **kwargs):

            key = tuple(imap(kwargs.__getitem__, names))

            try:
                return cache[key]
            except KeyError:
                pass

            value = cache[key] = func(*args, **kwargs)

            return value

        setattr(wrapper, 'cache', cache)

        return wrapper
    return maker


make_const_raise.stop_iteration = make_const_raise(StopIteration())

# </editor-fold>
########################################################################################################################
# <editor-fold desc="iter">

iempty = iter(())
repeat_empty = repeat(())
repeat_empty_dict = repeat({})


def ireturn(f):
    yield f()


def iraise(e):
    yield raise_(e)


def ipass(*args, **kwargs):
    return iempty


def itry(g, h=ipass, catch=Exception):

    try:
        for value in g():
            yield value

    except catch as e:
        for value in h(e):
            yield value


def itry1(f, h=ipass, catch=Exception):

    try:
        yield f()

    except catch as e:
        for value in h(e):
            yield value


def ipartial(function, *iterables):
    return imap(partial, repeat(function), *iterables)


def star_tuple(*items):
    return items


def itry_map(f, args_it=repeat_empty, kwargs_it=repeat_empty_dict, catch=(), h=ipass):

    for args, kwargs in izip(args_it, kwargs_it):

        try:
            yield f(*args, **kwargs)

        except catch as e:
            for value in h(e):
                yield value


def iget_item(obj, keys, h=ipass, catch=LookupError, getter=get_):
    return itry_map(obj.__getitem__, args_it=izip(keys), catch=LookupError, h=h)


def iget_attr(obj, names, h=ipass, catch=AttributeError):
    return itry_map(MethodType(getattr, obj), args_it=izip(names), catch=AttributeError, h=h)


def iget_next(it, default=MISSING, missing=MISSING, h=ipass, catch=StopIteration):
    return itry_map(MethodType(next, it), catch=AttributeError, h=h)


def yield_next(it):

    try:
        yield next(it)
    except StopIteration:
        pass


def make_iconst(value, n=1):

    if n is None:

        def iconst(*args, **kwargs):
            return repeat(value)

    else:

        def iconst(*args, **kwargs):
            return repeat(value, n)

    iconst.func_name = '{}({}, times={})'.format(iconst.func_name, repr(value), n)

    return iconst


def get_next(it, default=MISSING, missing=MISSING, f=identity, catch=StopIteration):
    try:
        value = next(it)
    except catch:
        if default is missing:
            raise
        return default
    else:
        return f(value)


def extend_iter(it, *extension):
    return chain(it, extension)


# </editor-fold>
########################################################################################################################
# <editor-fold desc="Namespace">


class NamespaceClassType (type):

    def __repr__(cls):
        return '{}({})'.format(cls.__name__, star_join_format(cls.items(), fmt='{}={!r}', sep=', '))

    def keys(cls):
        for name in dir(cls):
            if not name.startswith('_'):
                yield name

    def values(cls):
        for name in cls.keys():
            yield cls[name]

    def items(cls):
        for name in cls.keys():
            yield name, cls[name]

    def __getitem__(cls, name):

        if not name.startswith('_'):

            try:
                return getattr(cls, name)
            except AttributeError:
                pass

        raise KeyError(name)

    pass


class NamespaceClass (object):

    __metaclass__ = NamespaceClassType

    def __new__(cls, *args, **kwargs):
        raise TypeError('{!r} is a namespace class'.format(cls.__name__))

    pass


# </editor-fold>
########################################################################################################################
# <editor-fold desc="attr">


def get_attr(
        obj,
        name,
        default=MISSING,
        missing=MISSING,
        f=identity,
        catch=AttributeError,
):
    """

    return get_next_attr(obj, names=yield_(name), default=default, missing=missing, f=f, catch=catch)

    :type obj:
    :type name:
    :type default:
    :type missing:
    :type f:
    :type catch:
    :rtype:
    """

    try:
        value = getattr(obj, name)

    except catch:
        if default is missing:
            raise
        return default

    else:
        return f(value)


def get_next_attr(
        obj,
        names,
        default=MISSING,
        missing=MISSING,
        f=identity,
        catch=AttributeError,
        raise_=AttributeError,
):
    """
    return get_next(iget_attr(obj, names, h=iraise), default=default, missing=missing, f=f, catch=catch)

    :type obj:
    :type names:
    :type default:
    :type missing:
    :type f:
    :type catch:
    :rtype:
    """

    for name in names:
        try:
            value = getattr(obj, name)
        except catch:
            pass
        else:
            return f(value)

    if default is missing:
        raise raise_(names)

    return default


def attr_items(
        obj,
        names,
        default=MISSING,
        missing=MISSING,
        f=identity,
        catch=AttributeError,
):
    for name in names:
        yield name, get_attr(
            obj=obj,
            name=name,
            default=default,
            missing=missing,
            f=f,
            catch = catch
        )


def is_attr_missing(obj, name, missing=MISSING):
    return getattr(obj, name, missing) is missing


def make_lazy_attr(name, missing=MISSING):

    def maker(func):

        @wraps(func)
        def wrapper(o, *args, **kwargs):

            value = getattr(o, name, missing)

            if value is not missing:
                return value

            value = func(o, *args, **kwargs)

            setattr(o, name, value)

            return value

        return wrapper

    return maker


def remove_attr(obj, name, strict=False):
    try:
        delattr(obj, name)
    except AttributeError:
        if strict:
            raise
        return False
    else:
        return True


def set_attr(obj, name, value, missing=MISSING):

    if value is missing:
        remove_attr(obj, name)
    else:
        setattr(obj, name, value)

    return obj


def set_attr_default(obj, name, value):

    try:
        return getattr(obj, name)
    except AttributeError:
        pass

    setattr(obj, name, value)

    return value


def set_attr_default_factory(obj, name, f):

    try:
        return getattr(obj, name)
    except AttributeError:
        pass

    value = f()
    setattr(obj, name, value)

    return value


def set_attr_default_by_name(obj, name, f):

    try:
        return obj[name]
    except AttributeError:
        pass

    value = f(obj, name)
    setattr(obj, name, value)

    return value


def set_attr_protected(obj, name, value):

    if hasattr(obj, name):
        raise AttributeError('try to change value of non-empty protected attribute: {}'.format(name))
     
    setattr(obj, name, value)


class AttrDict (object):

    __slots__ = (
        'obj',
    )

    def __init__(self, obj):
        self.obj = obj

    def __getitem__(self, name):
        return getattr(self.obj, name)

    pass


def discard_attr(
        obj,
        attr,
):
    """
    delete attribute of a given object if it exists and doesn't raise exception otherwise.
    :param obj:
    :param attr: string - attribute name
    """
    try:
        delattr(obj, attr)
    except AttributeError:
        pass


def copy_attr(
        source_obj,
        source_attr,
        target_obj,
        target_attr,
        discard_attr=discard_attr,
):
    """
    Copy attribute state and value from one object to another. if the attribute exists in the source object, this
    function will try to set an attribute of the same value to the target object and raise AttributeError if
    failed. If the attribute is missing in the source object, this function will try to delete the proper attribute
    from the target object but will not raise any exception if failed.
    :param source_obj:
    :param source_attr: string - attribute name in the source object.
    :param target_obj:
    :param target_attr: string - attribute name in the target object.
    """
    try:
        val = getattr(source_obj, source_attr)
    except AttributeError:
        discard_attr(target_obj, target_attr)
    else:
        setattr(target_obj, target_attr, val)


class ContextAttr (object):
    """
    Capture attribute state (missing or exists with value) of an object and reset it to the same state when exit
    context.
    """

    __slots__ = (
        'obj',
        'attr',
        'exit_val',
    )

    def __init__(self, obj, attr):
        self.obj = obj
        self.attr = attr

    def __enter__(self, copy_attr=copy_attr):

        copy_attr(
            source_obj=self.obj,
            source_attr=self.attr,
            target_obj=self,
            target_attr='exit_val',
        )

    def __exit__(self, exc_type, exc_val, exc_tb, copy_attr=copy_attr):

        copy_attr(
            source_obj=self,
            source_attr='exit_val',
            target_obj=self.obj,
            target_attr=self.attr,
        )


def get_getsetdescriptor(cls):
    for base in cls.__mro__:
        val = base.__dict__.get('__dict__')
        if isgetsetdescriptor(val):
            return val


def vars_static(obj):

    getsetdescriptor = get_getsetdescriptor(type(obj))

    if getsetdescriptor is not None:
        return getsetdescriptor.__get__(obj)


def getattr_static(obj, attr, default=MISSING, missing=MISSING):

    for base in chain(getattr(obj, '__mro__', (obj,)), getattr(type(obj), '__mro__', ())):

        base_vars = vars_static(base)

        if base_vars is None:
            continue

        try:
            return base_vars[attr]
        except KeyError:
            continue

    if default is missing:

        raise AttributeError(
            '{} has no attribute {}'.format(
                (
                    'type object {}'.format(getattr(obj, __name__, '?'))
                    if isinstance(obj, type) else
                    '{} object'.format(getattr(type(obj), __name__, '?'))
                ),
                attr,
            )
        )

    return default


def make_attr_cache(name, missing=None):

    def maker(func):

        @wraps(func)
        def wrapper(o, *args, **kwargs):

            value = getattr(o, name, missing)

            if value is not missing:
                return value

            value = func(o, *args, **kwargs)

            setattr(o, name, value)

            return value

        return wrapper

    return maker


class DescriptorUnderContextManager (object):

    __slots__ = (
        'descriptor',
        'context_manager',
    )

    def __init__(self, descriptor, context_manager):
        self.descriptor = descriptor
        self.context_manager = context_manager

    @classmethod
    def by_name(cls, owner, name, context_manager):
        return cls(
            descriptor=getattr_static(owner, name),
            context_manager=context_manager,
        )

    @classmethod
    def wrap(cls, owner, name, context_manager):

        self = cls.by_name(
            owner=owner,
            name=name,
            context_manager=context_manager,
        )

        setattr(owner, name, self)

        return self

    @classmethod
    def make(cls, context_manager, names):

        def maker(cls_, context_manager=context_manager, names=names):

            if isinstance(context_manager, basestring):
                context_manager = getattr(cls_, context_manager)

            if isinstance(names, basestring):
                names = getattr(cls_, names)

            for name in names:
                cls.wrap(owner=cls_, name=name, context_manager=context_manager)

            return cls_

        return maker

    def __get__(self, instance, owner):
        with self.context_manager:
            return self.descriptor.__get__(instance, owner)

    def __set__(self, instance, value):
        with self.context_manager:
            self.descriptor.__set__(instance, value)

    def __delete__(self, instance):
        with self.context_manager:
            self.descriptor.__delete__(instance)

    pass


def ordered_dir(obj, include_protected=True):

    try:
        slots = [
            typ.__slots__
            for typ in type(obj).__mro__[:-1]
        ]

    except AttributeError:
        names = dir(obj)
    else:
        names = chain.from_iterable(reversed(slots))

    if include_protected:
        return names

    return (
        name
        for name in names
        if not name.startswith('_')
    )


def ordered_vars(obj, include_protected=True):

    for name in ordered_dir(obj, include_protected=include_protected):

        try:
            value = getattr(obj, name)
        except AttributeError:
            pass
        else:
            yield name, value


def get_attr_len(
        obj,
        name,
        default=MISSING,
        missing=MISSING,
        f=identity,
        catch=(AttributeError, TypeError),
):

    try:
        value = len(getattr(obj, name))

    except catch:
        if default is missing:
            raise
        return default

    else:
        return f(value)


# </editor-fold>
########################################################################################################################
# <editor-fold desc="collections">


def remove_item(obj, key, strict=False):
    try:
        del obj[key]
    except KeyError:
        if strict:
            raise
        return False
    else:
        return True


def set_item(obj, key, value, missing=MISSING):

    if value is missing:
        remove_item(obj, key)
    else:
        obj[key] = value

    return obj


def set_item_default(obj, key, value):

    try:
        return obj[key]
    except LookupError:
        pass

    obj[key] = value

    return value


def set_item_default_factory(obj, key, f):

    try:
        return obj[key]
    except LookupError:
        pass

    value = f()
    obj[key] = value

    return value


def set_item_default_by_name(obj, key, f):

    try:
        return obj[key]
    except LookupError:
        pass

    value = f(obj, key)
    obj[key] = value

    return value


class ConstructorDict (OrderedDict):

    __slots__ = (
        'key_from_args',
        'constructor',
    )

    def __init__(self, key_from_args, constructor):
        """
        :param key_from_args: args of constructor -> key
        :type key_from_args: Callable
        :param constructor: args of constructor -> value
        :type constructor: Callable
        """

        self.key_from_args = key_from_args
        self.constructor = constructor

    def get_or_craete(*args, **kwargs):

        self = args[0]
        args = args[1:]

        key = self.key_from_args(*args, **kwargs)

        try:
            return self[key]
        except KeyError:
            pass

        value = self[key] = self.constructor(*args, **kwargs)

        return value

    pass


# </editor-fold>
########################################################################################################################
# <editor-fold desc="types">


def get_item_by_type(src, typ, default=MISSING, missing=MISSING, f=identity, catch=LookupError):
    return get_next_item(src, typ.__mro__, default=default, missing=missing, f=f, catch=catch)


# </editor-fold>
########################################################################################################################
# <editor-fold desc="type assertions">


def assert_type(obj, typ):

    assert isinstance(obj, typ), 'unexpected type: {} (expected: {})'.format(
        repr(type(obj).__name__),
        repr(typ.__name__),
    )

    return obj


def iassert_type(it, typ):
    for obj in it:
        yield assert_type(obj, typ)


# </editor-fold>
########################################################################################################################
# <editor-fold desc="repr">


def get_obj_type_name(obj, default=MISSING, missing=MISSING, f=identity, catch=AttributeError):
    return get_type_name(typ=type(obj), default=default, missing=missing, f=f, catch=catch)


def get_type_name(typ, default=MISSING, missing=MISSING, f=identity, catch=AttributeError):
    if not isinstance(typ, type):
        typ = type(typ)
    return get_attr(typ, '__name__', default=default, missing=missing, f=f, catch=catch)


class ConstRepr (object):
    __slots__ = 'value',

    _cache = {}

    def __new__(cls, value):
        try:
            return cls._cache[value]
        except KeyError:
            pass

        o = cls._cache[value] = super(ConstRepr, cls).__new__(cls)
        o.value = value
        return o

    def __repr__(self):
        return self.value


def join_repr(it, sep=', ', kw=()):

    it = iter(it)

    return sep.join(chain(
        imap('{}={!r}'.format, kw, it),
        imap(repr, it),
    ))


def join_format(it, fmt='{}', sep=''):
    return sep.join(imap(fmt.format, it))


def star_join_format(it, fmt='{}', sep=''):
    return sep.join(starmap(fmt.format, it))


def get_type_label(obj, default=MISSING, missing=MISSING):

    try:
        return obj._type_label
    except AttributeError:
        pass

    return get_type_name(obj, default=default, missing=missing)


def join_attr_repr(
        obj,
        names,
        default='',
        missing=MISSING,
        f=repr,
        catch=AttributeError,
        fmt='{}={}',
        sep=', ',
):
    return star_join_format(
        attr_items(
            obj=obj,
            names=names,
            default=default,
            missing=missing,
            f=f,
            catch = catch
        ),
        fmt=fmt,
        sep=sep,
    )


def join_collection_attr_repr(
        obj,
        names,
        default='?',
        missing=MISSING,
        catch=AttributeError,
        fmt='{}*{},',
        sep=' ',
):
    return star_join_format(
        (
            (get_attr_len(obj, name, default=default, f='{:,}'.format), name)
            for name in obj._collection_attrs
        ),
        fmt=fmt,
        sep=sep,
    )

def get_function_name(back=1):
    from inspect import currentframe, getframeinfo

    frame = currentframe()

    for _ in xrange(back):
        frame = frame.f_back

    return getframeinfo(frame).function


def fstr(*args, **kwargs):
    return get_fstr(
        fmt=args[0],
        args=args[1:],
        kwargs=kwargs,
        back=2,
    )


def get_fstr(fmt, args=(), kwargs={}, back=1):
    from inspect import currentframe, getframeinfo

    frame = currentframe()

    for _ in xrange(back):
        frame = frame.f_back

    variables = dict(frame.f_globals)
    variables.update(frame.f_locals)
    variables.update(kwargs)
    
    function_name = getframeinfo(frame).function

    return fmt.format(function_name, *args, **variables)


def tree_format(value, level, indent='|', conn='+ '):
    return '{}{}{}'.format(indent * level, conn, value)


def print_break():
    return print('_______________________________________________________________________________________________\n')


# </editor-fold>
# <editor-fold desc="repr_standard">


class ReprStandard (object):

    DEFAULT_FMT = '{label}({info})'
    DEFAULT_INFO_SEP = ', '
    DEFAULT_FMT__INFO = '{};'

    __slots__ = (
        'fmt',
        'info_sep',
    )

    def __init__(
            self,
            fmt=MISSING,
            info_sep=MISSING,
    ):
        self.fmt = unmissing_strict(fmt, self.DEFAULT_FMT)
        self.info_sep = unmissing_strict(info_sep, self.DEFAULT_INFO_SEP)
        pass

    def __call__(self, obj):
        return self.format(obj)

    def format(self, obj):
        return self.fmt.format(**self.param(obj))

    def param(self, obj):
        return dict(
            label=self.format_label(obj),
            info=self.format_info(obj),
        )

    def format_label(self, obj):
        return get_type_label(obj, default='<unknown_type>')

    def format_info(self, obj):
        return join_format(self.info_parts(obj), fmt='{};', sep=' ')

    def info_parts(self, obj):
        return filter(None, [
            self.format_info_attrs(obj),
            self.format_collection_attrs(obj),
        ])

    def format_info_attrs(self, obj):

        try:
            info_attrs = self.get_obj_info_attrs(obj)
        except AttributeError:
            return None

        return join_attr_repr(obj, obj._info_attrs)

    def format_collection_attrs(self, obj):

        try:
            collection_attrs = self.get_obj_collection_attrs(obj)
        except AttributeError:
            return None

        return join_collection_attr_repr(obj, collection_attrs)

    def get_obj_info_attrs(self, obj):
        return obj._info_attrs

    def get_obj_collection_attrs(self, obj):
        return obj._collection_attrs

    def __get__(self, instance, owner):
        return owner if instance is None else MethodType(self.__call__, instance)

    pass


repr_standard = ReprStandard()

# </editor-fold>
########################################################################################################################
