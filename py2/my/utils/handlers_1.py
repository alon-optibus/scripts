import weakref
from abc import ABCMeta
from collections import OrderedDict
from functools import total_ordering

from itertools import chain, imap, repeat, starmap

from my.utils import assert_type, extend_iter, get_obj_type_name, join_repr, MISSING, ordered_dir, remove_item, \
    set_attr_protected, star_join_format, tree_format, ordered_vars

########################################################################################################################

HANDLER_COLLECTION_INDICATOR = '_is_handler_collection'
HANDLER_TYPE_INDICATOR = '_handler_type'

########################################################################################################################
# <editor-fold desc="typed key">


class TypedTuple (tuple):
    __slots__ = ()

    _arg_labels = MISSING

    def __new__(cls, typ, args):
        """
        :type typ: type
        :type args: tuple
        :rtype: TypedKey
        """
        return super(TypedTuple, cls).__new__(cls, (typ,) + args)

    def __repr__(self):
        return '({}: {})'.format(get_label(self.typ), self.label_repr())

    def label_repr(self, sep=', '):
        return join_repr(self.args, kw=self.arg_labels)

    @property
    def typ(self):
        return self[0]

    @property
    def args(self):
        return self[1:]

    @property
    def arg_labels(self):

        try:
            return self._arg_labels
        except AttributeError:
            pass

        try:
            return self.typ._key_arg_labels
        except AttributeError:
            pass

        return ()

    pass


class TypedKey (TypedTuple):
    __slots__ = ()

    def __repr__(self):
        return '(#{}: {})'.format(get_label(self.typ), self.label_repr())

    pass


# </editor-fold>
# <editor-fold desc="labels">


def get_label(obj):

    try:
        return obj._label
    except AttributeError:
        pass

    if isinstance(obj, type):
        return obj.__name__

    return get_label(type(obj))


def get_owner_hierarchy_label(obj, sep='.', owner_name='owner'):
    return sep.join(imap(get_label, extend_iter(get_owners(obj, owner_name=owner_name), obj)))


# </editor-fold>
# <editor-fold desc="misc utils">


def assert_handler(obj, handler_type, owner):
    obj = assert_type(obj, handler_type)
    assert obj.owner is owner
    return obj


def get_owners(obj, owner_name='owner'):
    try:
        owner = getattr(obj, owner_name)
    except AttributeError:
        return ()
    else:
        return get_owners(owner, owner_name=owner_name) + (owner,)


def get_handler_dicts(obj):

    for name in ordered_dir(obj):

        if name.startswith('_'):
            continue

        try:
            value = getattr(obj, name)
        except AttributeError:
            continue

        if getattr(value, HANDLER_COLLECTION_INDICATOR, False):
            yield name, value

def assert_owner(owner):
    """
    :type owner: HandlerBase
    """
    assert isinstance(owner, HandlerBase)
    assert hasattr(owner, 'subjects')
    return owner

# </editor-fold>
########################################################################################################################

# <editor-fold desc="handler base class">


@total_ordering
class HandlerBase (object):

    __slots__ = (
        '__key',
        '__index',
        '__owner',
        '__subjects',
        '__weakref__',
    )

    _key_type = TypedKey
    _key_arg_labels = ()
    _label = MISSING

    # <editor-fold desc="owner property">

    @property
    def owner(self):
        return self.__owner()

    @owner.setter
    def owner(self, owner):
        """
        :type owner: HandlerBase
        """

        if owner is None:
            del self.owner
        else:
            assert_owner(owner)
            self.__owner = weakref.ref(owner)
            owner.__subjects.put(self)
            self._attach(owner)

    @owner.deleter
    def owner(self):
        """
        :type owner: HandlerBase
        """

        try:
            owner = self.owner
        except AttributeError:
            return

        del self.__owner
        owner.__subjects.remove(self)
        self._detach(owner)

    def has_owner(self):
        return hasattr(self, '__owner')

    # </editor-fold>
    # <editor-fold desc="subjects property">
    
    @property
    def subjects(self):
        return self.__subjects
    
    # </editor-fold>
    # <editor-fold desc="key property">

    @property
    def key(self):
        return self.__key

    # </editor-fold>
    # <editor-fold desc="index property">

    @property
    def index(self):
        return self.__index

    @index.setter
    def index(self, value):
        set_attr_protected(self, '_HandlerBase__index', value)

    @index.deleter
    def index(self):
        del self.__index

    # </editor-fold>

    def __init__(self, owner=None, key_args=()):
        self.__subjects = HandlerDict()
        self.__key = self._get_key(key_args=key_args)
        self.owner = owner

    def _attach(self, owner):
        pass

    def _detach(self, owner, strict=False):
        pass

    @classmethod
    def _get_key(cls, key_args):
        return cls._key_type(typ=cls, args=key_args)

    def __repr__(self):
        return '{label}[{key}]({handler_dicts})'.format(
            label=get_owner_hierarchy_label(self),
            handler_dicts=star_join_format((
                (len(handler_dict), name)
                for name, handler_dict in get_handler_dicts(self)
            ), fmt='{}*{}', sep=', '),
            key=self.key,
        )

    def __eq__(self, other):
        return self.__key == other.key

    def __ne__(self, other):
        return self.__key != other.key

    def __lt__(self, other):
        return self.__key < other.key

    def __hash__(self):
        return hash(self.__key)

    pass


# </editor-fold>

########################################################################################################################

# <editor-fold desc="handler colections">


class HandlerCollectionAbc:
    __metaclass__ = ABCMeta
    pass


def default_handler_collection_repr(self):
    return '{}({}*{})'.format(get_obj_type_name(self), len(self), get_label(self._handler_type))


class HandlerDict (OrderedDict):

    _is_handler_collection = True
    _handler_type = HandlerBase

    def put(self, handler):
        self[handler.key] = handler
        return self

    def pop(self):
        _, obj = self.popitem()
        return obj

    def remove(self, handler, strict=False):
        return remove_item(self, handler.key, strict=strict)

    def update(self, *it):
        for handler in chain.from_iterable(it):
            self.put(handler)
        return self

    def clear(self):
        tmp = list(self)

        for handler in tmp:
            self.remove(handler)

        return self

    def __iter__(self):
        return self.itervalues()

    __repr__ = default_handler_collection_repr

    pass


class HandlerList (list):

    _is_handler_collection = True
    _handler_type = HandlerBase

    def put(self, handler, index=None, empty=None):

        if index is None:
            index = handler.index
        else:
            handler.index = index

        self.allocate(index+1)

        self[index] = handler

        return self

    def allocate(self, n, empty=None):
        if n > len(self):
            self[len(self):n] = repeat(empty, n - len(self))

    def remove(self, handler, strict=False):
        return remove_item(self, handler.index, strict=strict)

    def fill(self, value=None, n=None):
        self[:] = repeat(None, len(self) if n is None else n)
        return self

    __repr__ = default_handler_collection_repr

    pass


HandlerCollectionAbc.register(HandlerDict)
HandlerCollectionAbc.register(HandlerList)


class HandlerSubjects (HandlerDict):
    __slots__ = ()

    def remove(self, handler, strict=False):
        """
        :type handler: HandlerBase
        :type strict: bool
        :rtype: HandlerSubjects
        """
        super(HandlerSubjects, self).remove(handler=handler, strict=strict)
        del handler.owner
        return self


# </editor-fold>

########################################################################################################################
# <editor-fold desc="long repr">


def iter_handler_tree(handler, level=0):
    """
    :type handler: HandlerBase
    :type level: int
    """

    yield handler, level

    for subject in handler.subjects:
        for item in iter_handler_tree(subject, level=level + 1):
            yield item


def tree_format_handler_tree(handler, level=0):
    """
    :type handler: HandlerBase
    :type level: int
    """

    return starmap(tree_format, iter_handler_tree(handler, level=0))


# </editor-fold>
########################################################################################################################
