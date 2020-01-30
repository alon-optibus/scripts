from __future__ import print_function, division

from my.utils.ui_1 import get_ui_input, MissingError
from my.utils.xdotool_1 import xdotool_type

########################################################################################################################

try:
    i: str = get_ui_input()

except MissingError:
    exit()

print(repr(i))

o = i.replace(' ', '_')

print(repr(o))

xdotool_type(o)

########################################################################################################################
