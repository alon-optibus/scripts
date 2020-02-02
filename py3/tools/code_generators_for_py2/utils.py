from typing import Iterable

TAB_SIZE = 4
TAB = ' ' * TAB_SIZE


########################################################################################################################


def put(level: int, text: str):
    from textwrap import indent

    return print(indent(
        text.expandtabs(TAB_SIZE),
        TAB * level,
    ))


def fjoin(it:Iterable, fmt:str = '{}', sep:str = ''):
    return sep.join(map(fmt.format, it))


########################################################################################################################
