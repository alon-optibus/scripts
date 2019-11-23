from tools.code_generators_for_py2 import put

class_name = 'VipScenario'

class_bases = (object,)

attrs = '''\
a
b
c
'''.splitlines()

print(attrs)

########################################################################################################################


class_bases = [
    base.__name__ if isinstance(base, type) else base
    for base in class_bases
]


########################################################################################################################

v = 0

put(v, '')
put(v, f"class {class_name} ({', '.join(class_bases)}):")

v += 1

put(v, '')
put(v, 'def __init__(')

v += 1

put(v, 'self,')

for attr in attrs:
    put(v, f'{attr}=None,')

v -= 1

put(v, '):')

v += 1

# <editor-fold desc="__init__ body">

for attr in attrs:
    put(v, f'self.{attr} = {attr}')

put(v, 'pass')

# </editor-fold>

v -= 1

put(v, 'pass')

v -= 1

put(v, '')

########################################################################################################################
