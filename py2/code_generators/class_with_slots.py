from __future__ import print_function, division
from my.utils import ReprManager
from euclid.utils.attr_utils import partial_data_class

########################################################################################################################

class_name = 'VipSolution'

class_bases = (object,)

attrs = (
        'schedule',
        'data_set',
        'scenario',
        'scheduler',
        'vehicle_info',
        'cols',
        'col_paths',
        'excluded_trips',
    )

# attrs = '''\
# scenario
# schedule
# data_set
# scheduler
# '''.splitlines()

########################################################################################################################


def getattr_repr(obj, attr, default=''):
    try:
        val = getattr(obj, attr)
    except AttributeError:
        return default
    return repr(val)


########################################################################################################################

x = ReprManager()

# <editor-fold desc="head">

x.append('@partial_data_class')
x.format('class {} ({}):', class_name, ', '.join([cls.__name__ for cls in class_bases]))
x += 1

# </editor-fold>

x.new_line()

# <editor-fold desc="slots">

# x.format("__slots__ = _fields = ({})", ' '.join(repr(attr) + ',' for attr in attrs))

x.append("_fields = (")

x += 1

for attr in attrs:
    x.format("'{}',", attr)

x -= 1

x.append(")")

x.new_line()

x.append('_extra = ()')

x.new_line()

x.append('_info_fields = _fields + _extra')
x.append("__slots__ = _info_fields + ('__weakref__',)")


# </editor-fold>

x.new_line()

# <editor-fold desc="__init__">

# x.format('def __init__({}):', ', '.join(['self'] + attrs))

x.append('def __init__(')
x += 2
x.append('self,')

for attr in attrs:
    x.format('{}=None,', attr)

x -= 2
x.append('):')

x += 1

for attr in attrs:
    x.format('self.{attr} = {attr}'.format(attr=attr))


x.append('pass')
x -= 1

# </editor-fold>

# <editor-fold desc="__repr__">

# x.new_line()

# x.append('def __repr__(self):')
# x += 1
#
# x.append("type_name = getattr(type(self), '__name__', '')")
# x.append("return '{}({})'.format(")
# x += 1
# x.append("type_name,")
# x.append("', '.join([")
# x += 1
# x.append("'{}={}'.format(attr, getattr_repr(self, attr))")
# x.append("for attr in type(self)._fields")
# x -= 1
# x.append("])")
# x -= 1
# x.append(")")
#
# x -= 1

# </editor-fold>

# <editor-fold desc="tail">

x.new_line()

x.append('pass')
x -= 1

# </editor-fold>

x.print(file='scratch.txt')

x.code_break('#'*80)

# <editor-fold desc="flatten attrs">

x.append('attrs = """\\')

for attr in attrs:
    x.append(attr)

x.append('""".splitlines()')

x.code_break('#'*80)

# </editor-fold>

x.print()

if True:
    e = x.eval(
        getattr_repr=getattr_repr,
        partial_data_class=partial_data_class,
    )

    y = e.get(class_name)

    print(y)
    print(y.__slots__)
    # print(dir(y))
    for attr in attrs:
        print(attr, ':', getattr_repr(y, attr))

    print('')

    print(object.__new__(y))
    print(y())

    # y1 = y(11, 22, 33)
    #
    # print(y1)
    # print([getattr(y1, attr, None) for attr in attrs])
    #
    # del y1.b
    #
    # print(y1)

    pass


########################################################################################################################
