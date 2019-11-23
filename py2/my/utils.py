from __future__ import division, print_function

import os
from contextlib import contextmanager
from itertools import imap, izip, chain
from collections import OrderedDict, namedtuple
from functools import wraps
from textwrap import dedent
import weakref
from numbers import Number

from euclid.utils.lookup_utils import MISSING, make_type_based_eq
from toolz import identity

REPR = repr
LINESEP = os.linesep

inf = float('inf')

########################################################################################################################


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


########################################################################################################################
# <editor-fold desc="attrs">


def get_attr(o, name, default=MISSING, missing=MISSING, f=identity):
    try:
        value = getattr(o, name)
    except AttributeError:
        if default is missing:
            raise
        return default
    else:
        return f(value)


def iter_attrs(src, attrs, default=MISSING, missing=MISSING):
    for attr in attrs:
        yield get_attr(src, attr, default, missing)


def make_attr_cache(name, missing=MISSING):

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


# </editor-fold>
########################################################################################################################
# <editor-fold desc="repr">

REPR_START__LIST = '['
REPR_END__LIST = ']'

REPR_START__TUPLE = '('
REPR_END__TUPLE = ')'

REPR_START__SET = '{'
REPR_END__SET = '}'


def code_repr(obj, level=0, tab='\t', start='', end='', obj_param=()):

    tabs = tab * level
    obj_type_name = type(obj).__name__

    if obj_type_name in obj_param:

        yield tabs + start + obj_type_name + '('

        for param in obj_param[obj_type_name]:

            try:
                value = getattr(obj, param)

            except AttributeError:
                yield tabs + tab + param + '=,'

            else:

                for line in code_repr(
                        obj=value,
                        level=level+1,
                        tab=tab,
                        start=param + '=',
                        end=',',
                        obj_param=obj_param,
                ):
                    yield line

        yield tabs + ')' + end

    elif isinstance(obj, list):

        if len(obj):

            yield tabs + start + '['

            for value in obj:
                for line in code_repr(
                        obj=value,
                        level=level+1,
                        tab=tab,
                        end=',',
                        obj_param=obj_param,
                ):
                    yield line

            yield tabs + ']' + end

        else:
            yield tabs + start + '[]' + end

    elif isinstance(obj, tuple):

        if len(obj):

            yield tabs + start + '('

            for value in obj:
                for line in code_repr(
                        obj=value,
                        level=level+1,
                        tab=tab,
                        end=',',
                        obj_param=obj_param,
                ):
                    yield line

            yield tabs + ')' + end

        else:
            yield tabs + start + '()' + end

    elif isinstance(obj, dict):

        for line in code_repr(
            obj=obj.items(),
            level=level,
            tab=tab,
            start=start + obj_type_name + '(',
            end=')' + end,
            obj_param=obj_param,
        ):
            yield line

    else:

        yield tabs + start + repr(obj) + end

    pass


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


ConstRepr.empty = ConstRepr('')


def get_type_name(o, default=MISSING, missing=MISSING):
    return get_attr(type(o), '__name__', default, missing)


class ReprManager (list):
    __slots__ = '_level', '_tab', '_tabs', 'repr_by_typ', 'min_split', 'bound',

    DEFAULT_TAB = ' ' * 4
    LINESEP = LINESEP

    def __init__(self, level=0, bound=None, tab=DEFAULT_TAB, min_split=3):
        self._level = level
        self.bound = bound
        self._tab = tab
        self._tabs = self._tab * self._level
        self.repr_by_typ = {
            list: self.default_repr_for_list,
            set: self.default_repr_for_list,
            frozenset: self.default_repr_for_list,
            tuple: self.default_repr_for_tuple,
        }
        self.min_split = min_split

    def append(*args, **kwargs):
        self = args[0]
        line = args[1]
        args = args[2:]

        value = line.format(*args, **kwargs)

        if self and self.bound is not None and self._level > self.bound:
            self[-1] += value
        else:
            super(ReprManager, self).append(self._tabs + value)

        return self

    def extend(self, lines):
        for line in lines:
            self.append(line)
        return self

    def new_line(self):
        return self.append('')

    def format(*args, **kwargs):
        self = args[0]
        line = args[1]
        args = args[2:]
        self.append(line.format(*args, **kwargs))
        return self

    def __iadd__(self, n):
        self._level += n
        self._tabs = self._tab * self._level
        return self

    def __isub__(self, n):
        self._level -= n
        self._tabs = self._tab * self._level
        return self

    def set_level(self, level):
        self._level = level
        self._tabs = self._tab * self._level
        return self

    def print(self, sep=None, mode='w', **kwargs):

        with open_file(kwargs.get('file'), mode) as f:

            kwargs['file'] = f

            if sep is None:
                for line in self:
                    print(line, **kwargs)
            else:
                print(sep.join(self), **kwargs)

        return self

    def get_repr(self, obj, default=None):
        for typ in type(obj).__mro__:
            try:
                return self.repr_by_typ[typ]
            except LookupError:
                pass
        return default

    def eval(*args, **kwargs):
        self, = args
        # return eval('\n'.join(self), kwargs)

        exec dedent('\n'.join(self)) in kwargs

        return kwargs

    def code_break(self, break_line='#'*80):
        self.new_line()
        self.append(break_line)
        self.new_line()
        return self

    def join(self, sep='\n'):
        """
        :type sep: basestring
        :rtype: ReprManager
        """
        self[:] = [sep.join(self)]
        return self

    @property
    def is_bounded(self):
        return self.bound is not None and self._level >= self.bound

    @property
    def width(self):
        return max(imap(len, self))

    # <editor-fold desc="repr utils">

    empty = ConstRepr.empty

    def const(self, value):
        return ConstRepr(value)

    def type_name_repr(self, obj, default='', missing=MISSING):
        """
        :type obj: Any
        :type default: basestring
        :rtype: basestring
        """
        return repr(get_type_name(obj, self.const(default), missing))

    # def attr_repr(self, obj, attr, default='', missing=MISSING):
    #     return ''
    #     # return self.repr(get_attr(obj, attr))

    # </editor-fold>
    # <editor-fold desc="default repr">

    def flat_repr(self, obj, start='', end='', f=repr):
        return self.append(start + f(obj) + end)

    def default_repr_for_tuple(self, obj, start='', end=''):

        obj_fields = getattr(type(obj), '_fields', None)

        bounded = self.is_bounded
        sep = ', ' if bounded else ','

        if obj_fields is not None:
            return self.default_repr_for_data_class(obj, attrs=obj_fields, start=start, end=end)

        if type(obj) is not tuple:
            start = '{}({}'.format(type(obj).__name__, start)
            end = '{})'.format(end)

        if len(obj) >= self.min_split:

            self.append(start + '(')

            self += 1

            for value in obj:
                self.repr(
                    obj=value,
                    end=sep,
                )

            self -= 1

            if bounded:
                self[-1] = self[-1][:-1] + '){}'.format(end)
            else:
                self.append('){}', end)

        else:
            self.append(start + '(')

            n = len(obj) - 1

            for i, value in enumerate(obj):

                sub = type(self)(bound=self.bound-self._level).repr(
                    obj=value,
                    end=(('' if len(obj) > 1 else sep) if i == n else ', ')
                )

                sub_iter = iter(sub)

                self[-1] += next(sub_iter)

                for line in sub_iter:
                    self.append(line)

            self[-1] += (')' + end)

        return self

    def default_repr_for_list(self, obj, start='', end=''):

        bounded = self.is_bounded
        sep = ', ' if bounded else ','

        if type(obj) is not list:
            start = '{}({}'.format(type(obj).__name__, start)
            end = '{})'.format(end)

        if len(obj):

            self.append(start + '[')

            self += 1

            for value in obj:
                self.repr(
                    obj=value,
                    end=sep,
                )

            self -= 1

            if bounded:
                self[-1] = self[-1][:-len(sep)] + ']{}'.format(end)
            else:
                self.append(']{}', end)

        else:
            self.append(start + '[]' + end)

        return self

    def default_repr_for_dict(self, obj, start='', end=''):
        return self.default_repr_for_list(sorted(obj.iteritems()), start=start, end=end)

    def default_repr_for_ordered_dict(self, obj, start='', end=''):
        return self.default_repr_for_list(obj.iteritems(), start=start, end=end)

    def default_repr_for_data_class(self, obj, start='', end='', attrs='_fields'):
        """
        :type obj: Any
        :type start: basestring
        :type end: basestring
        :type attrs: Any
        :rtype: ReprManager
        """

        name = get_type_name(obj)
        bounded = self.is_bounded
        sep = ', ' if bounded else ','

        if isinstance(attrs, basestring):
            attrs = getattr(obj, attrs)

        self.append('{}{}(', start, name)
        self += 1

        for attr in attrs:
            self.repr(
                getattr(obj, attr, self.empty),
                start='{}='.format(attr),
                end=sep,
            )

        self -= 1

        if bounded:
            self[-1] = self[-1][:-len(sep)] + '){}'.format(end)
        else:
            self.append('){}', end)

        return self

    # </editor-fold>
    # <editor-fold desc="full repr">

    def full_repr__info_fields(self, o, start='', end=''):
        return self.default_repr_for_data_class(
            o,
            start=start,
            end=end,
            attrs=o._info_fields
        )

    # </editor-fold>

    def __repr__(self):
        raise TypeError()

    def repr(self, obj, start='', end=''):
        """
        :type obj: Any
        :type start: basestring
        :type end: basestring
        :rtype: ReprManager
        """

        by_typ = self.get_repr(obj)

        if by_typ is not None:
            by_typ(obj, start=start, end=end)
            return self

        obj_fields = getattr(type(obj), '_fields', None)

        if obj_fields is not None:
            return self.default_repr_for_data_class(obj, attrs=obj_fields, start=start, end=end)

        return self.flat_repr(obj, start=start, end=end)

    pass


class ReprManager2 (list):

    __slots__ = (
        '_level',
        '_tab',
        '_tabs',
        'irepr_by_typ',
        'bound',
    )

    DEFAULT_TAB = ' ' * 4
    LINESEP = LINESEP

    REPR_START__LIST = REPR_START__LIST
    REPR_END__LIST = REPR_END__LIST
    REPR_START__TUPLE = REPR_START__TUPLE
    REPR_END__TUPLE = REPR_END__TUPLE

    REPR_SEP = ','
    REPR_FLAT_SEP = ', '

    _tab_cache = {}

    def __init__(self, level=0, bound=None, tab=DEFAULT_TAB):

        self._tab = tab
        self._tabs = default_factory(self._tab_cache, tab, list)
        self.level = level

        self.bound = bound

        self.irepr_by_typ = {
            list: self.irepr_list,
            tuple: self.irepr_tuple,
            dict: self.irepr_dict,
            set: self.irepr_set,
        }

        pass

    def _fill_tabs(self):

        for n in xrange(len(self._tabs), self._level+1):
            self._tabs.append(self._tab * n)

        return self

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, value):
        self._level = value
        self._fill_tabs()
        
    @property
    def tabs(self):
        return self._tabs[self._level]

    @property
    def bounded(self):
        return self.bound is not None and self._level > self.bound

    def __iadd__(self, n):
        if n:
            self.level += n
        return self

    def __isub__(self, n):
        if n:
            self.level -= n
        return self

    def append(self, line, *args, **kwargs):
        """
        :type line: Union[basestring, Tuple[basestring, int]]
        :rtype: ReprManager2
        """

        if isinstance(line, tuple):
            line, level = line
        else:
            level = 0

        # line = line.format(*args, **kwargs)

        if level < 0:
            self += level

        if self and self.bounded:
            self[-1] += line
        else:
            super(ReprManager2, self).append(self.tabs + line)

        if level > 0:
            self += level

        return self

    def extend(self, lines, start='', end=''):
        """
        :type lines: Iterable[basestring]
        :type start: basestring
        :type end: basestring
        :rtype: ReprManager2
        """

        lines = iter(lines)

        try:
            line = next(lines)

        except StopIteration:
            return self

        else:
            self.append((start + line[0], line[1]))

        for line in lines:
            self.append(line)

        self[-1] += end

    def repr(self, o):
        self.extend(self.irepr(o))
        return self

    def print(self, sep=None, **kwargs):

        if sep is not None:
            return print(sep.join(self), **kwargs)

        for line in self:
            print(line, **kwargs)

        return self

    # <editor-fold desc="irepr">

    def irepr(self, o, start='', end=''):

        it = iter(get_item_by_type(self.irepr_by_typ, type(o), self.irepr_default)(o))

        try:
            first_line = next(it)
        except StopIteration:
            return

        try:
            line = next(it)
        except StopIteration:
            yield start + first_line[0] + end, first_line[1]
        else:
            yield start + first_line[0], first_line[1]

            for next_line in it:
                yield line
                line = next_line

            yield line[0] + end, line[1]

    def irepr_default(self, o):
        yield repr(o), 0

    def irepr_list(self, o):
        return self.irepr_seq(
            o,
            start=REPR_START__LIST if type(o) is list else type(o).__name__ + REPR_START__TUPLE + REPR_START__LIST,
            end=REPR_END__LIST if type(o) is list else REPR_END__LIST + REPR_END__TUPLE,
        )

    def irepr_tuple(self, o):
        return self.irepr_seq(
            o,
            start=REPR_START__TUPLE if type(o) is tuple else type(o).__name__ + REPR_START__TUPLE,
            end=REPR_END__TUPLE,
        )

    def irepr_set(self, o):
        return self.irepr_seq(
            o,
            start=REPR_START__SET if type(o) is set else type(o).__name__ + REPR_START__TUPLE + REPR_START__LIST,
            end=REPR_END__SET if type(o) is set else REPR_END__LIST + REPR_END__TUPLE,
        )

    def irepr_dict(self, o):
        return self.irepr_enclose(
            start=type(o).__name__ + REPR_START__TUPLE + REPR_START__LIST,
            end=REPR_END__LIST + REPR_END__TUPLE,
            it=self.irepr_iter(o.iteritems()) if len(o) else None
        )

    def irepr_iter(self, o):

        bounded = self.bounded

        sep = ', ' if bounded else ','

        it = iter(o)

        try:
            item = next(it)
        except StopIteration:
            return

        for next_item in it:

            for line in self.irepr(item, end=sep):
                yield line

            item = next_item

        for line in self.irepr(item, end=('' if bounded else sep)):
            yield line

    def irepr_enclose(self, start, end, it=None):

        if it is None:
            yield start + end, 0
            return

        yield start, 1

        for item in it:
            yield item

        yield end, -1

    def irepr_seq(self, o, start=REPR_START__LIST, end=REPR_END__LIST):
        return self.irepr_enclose(
            start=start,
            end=end,
            it=self.irepr_iter(o) if len(o) else None
        )

    def irepr_attrs(self, o, attrs, default=''):

        bounded = self.bounded

        sep = ', ' if bounded else ','

        # yield type(o).__name__ + self.REPR_START__TUPLE, 1

        for name in attrs:
            try:
                value = getattr(o, name)
            except AttributeError:
                yield name + '=' + default
            else:
                for line in self.irepr(
                    value,
                    start=name + '=',
                    end=sep,
                ):
                    yield line

        # yield self.REPR_END__TUPLE, -1

    # </editor-fold>
    pass


# </editor-fold>
########################################################################################################################
# <editor-fold desc="key manager">


KeyWithType = namedtuple('KeyWithType', ['typ', 'key'])


def repr_for_key_with_type(self):
    """
    :type self: KeyWithType
    :rtype: str 
    """
    return '{}({}, {})'.format(
        type(self).__name__,
        self.typ.__name__,
        repr(self.key),
    )


def eq_for_key_with_type(self, other, base_eq=tuple.__eq__):
    return type(self) is type(other) and base_eq(self, other)


def ne_for_key_with_type(self, other, base_ne=tuple.__ne__):
    return type(self) is not type(other) or base_ne(self, other)


KeyWithType.__repr__ = repr_for_key_with_type
KeyWithType.__eq__ = eq_for_key_with_type
KeyWithType.__ne__ = ne_for_key_with_type


class KeyManager (object):
    # <editor-fold desc="class variables">

    __slots__ = (
        'put_by_typ',
        'get_by_typ',
        'key_by_typ',
        'ref',
    )

    KeyWithType = KeyWithType

    identity_types = (
        Number,
        basestring,
        tuple,
        frozenset,
    )

    # </editor-fold>
    # <editor-fold desc="constructors">

    def __init__(self):
        self.put_by_typ = OrderedDict()
        self.key_by_typ = OrderedDict()
        self.get_by_typ = OrderedDict()
        self.ref = weakref.WeakValueDictionary()

    # </editor-fold>
    # <editor-fold desc="basic methods">

    def put(self, obj):
        get_item_by_type(self.put_by_typ, type(obj), default=self.default_put)(obj)
        return obj

    def put_iter(self, *it):
        for obj in chain.from_iterable(it):
            self.put(obj)
        return self

    def key(self, obj):
        return get_item_by_type(self.key_by_typ, type(obj), default=self.default_key)(obj)

    def get(self, key, default=MISSING, missing=MISSING):

        try:
            return self.ref[key]
        except (KeyError, TypeError):
            pass

        if isinstance(key, self.KeyWithType):
            return get_item_by_type(
                self.get_by_typ,
                key[0],
                default=self.default_get_by_typ,
            )(
                key,
                default=default,
                missing=missing,
            )

        if isinstance(key, self.identity_types):
            return key

        return self.default_get(key, default=default, missing=missing)

    # </editor-fold>
    # <editor-fold desc="default methods">
    
    def default_put(self, obj):

        if isinstance(obj, self.identity_types):
            return obj

        key = self.key(obj)
        self.ref[key] = obj
        return obj

    def default_key(self, obj):

        try:
            fields = obj._fields
        except AttributeError:
            pass
        else:
            return self.key_by_attrs(obj, names=fields)

        if isinstance(obj, self.identity_types):
            return obj

        return self.default_key_by_type_error(type(obj))

    def default_get(self, key, default=MISSING, missing=MISSING):
        if default is missing:
            raise KeyError(key)
        raise default

    def default_get_by_typ(self, key, default=MISSING, missing=MISSING):
        """
        :type key: KeyWithType
        :type default: Any
        :type missing: Any
        :rtype: Any
        """
        return key.typ(*key.key)

    def default_key_by_type_error(self, typ):
        raise TypeError(
            'key manager ({}) can`t assign key to type {}'.format(
                repr(type(self).__name__),
                repr(typ.__name__),
            ),
        )

    def default_key_error(self, key):
        raise KeyError(key)

    # </editor-fold>
    # <editor-fold desc="utils">

    def key_by_attr(self, obj, name, key_with_type=KeyWithType):
        key = getattr(obj, name)
        return key if key_with_type is None else key_with_type(typ=type(obj), key=key)

    def key_by_attrs(self, obj, names, key_with_type=KeyWithType):
        key = tuple(imap(self.key, iter_attrs(obj, names)))
        return key if key_with_type is None else key_with_type(typ=type(obj), key=key)

    def make_key_by_attr(self, name, key_with_type=KeyWithType):

        def key(obj):
            return self.key_by_attr(
                obj=obj,
                name=name,
                key_with_type=key_with_type,
            )

        return key

    def make_key_by_attrs(self, names, key_with_type=KeyWithType):

        is_str = isinstance(names, basestring)

        def key(obj):
            return self.key_by_attrs(
                obj=obj,
                names=(getattr(obj, names) if is_str else names),
                key_with_type=key_with_type,
            )

        return key

    # </editor-fold>
    pass


# </editor-fold>
########################################################################################################################


@contextmanager
def open_file(obj, mode='r'):

    opened = False

    if isinstance(obj, basestring):
        obj = open(obj, mode)
        opened = True

    yield obj

    if opened and obj is not None:
        obj.close()
    pass


def bound(*args, **kwargs):

    def call(f):
        return f(*args, **kwargs)

    return call


def call(f):
    return f()


def default_factory(o, key, default):

    try:
        return o[key]
    except LookupError:
        pass

    value = o[key] = default()

    return value


def get_item(src, key, default=MISSING, missing=MISSING):
    try:
        return src[key]
    except LookupError:
        if default is missing:
            raise
        return default


get_item.bound = get_item.__get__

########################################################################################################################


def get_first_item(src, keys, default=MISSING, missing=MISSING):

    for key in keys:
        try:
            return src[key]
        except LookupError:
            pass

    if default is missing:
        raise KeyError(keys)

    return default


def get_item_by_type(src, typ, default=MISSING, missing=MISSING):
    return get_first_item(src, typ.__mro__, default, missing)


########################################################################################################################
