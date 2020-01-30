from __future__ import division, print_function

import unittest
from itertools import *
from inspect import getframeinfo
from contextlib import contextmanager

from my.utils import *


########################################################################################################################
dict_0 = dict(a=11, b=22, c=33, d=44)

dummy_0 = Dummy(**dict_0)

e0 = DummyException(0)
e0_0 = e0('wow-e-0')

yield_validation = DummyException('yield_validation')
yield_validation_0 = yield_validation('yield_validation')


def f():
    return 'wow-f'


def fe():
    raise e0_0


def g():
    yield 'wow-g-0'
    yield 'wow-g-1'
    yield 'wow-g-2'


def ge():
    yield 'wow-ge-0'
    yield 'wow-ge-1'
    yield 'wow-ge-2'
    raise e0('wow-ge')


########################################################################################################################


class MissingYieldException (AssertionError):
    pass


class RedundantYieldException (AssertionError):
    pass


########################################################################################################################


class TestIter (unittest.TestCase):
    # <editor-fold desc="utils">

    def get_event_str(self, event, args=(), back=1):
        return get_fstr(
            fmt=':: test {!r} {!s}: {!r}',
            args=(event,) + tuple(args),
            back=back + 1,
        )

    def print_event(self, event, args, back=1):
        return print(self.get_event_str(
            event=event,
            args=args,
            back=back + 1,
        ))
    
    def print_yield(self, value, index=None, back=1):
        return self.print_event(
            event='yielded' if index is None else 'yielded#{}'.format(index),
            args=(value,),
            back=back + 1,
        )

    def print_raise(self, e, back=1):
        return self.print_event(event='raised', args=(e,), back=back + 1)

    def validate_yield(self, it, lb=None, ub=None, n=None, back=1, catch=()):

        if n is not None:
            lb = ub = n

        it_ = iter(it)
        i = -1
        e = None

        if lb is not None:

            try:
                while i < lb:
                    value = next(it_)
                    i += 1
                    self.print_yield(value, index=i+1, back=back+1)

            except StopIteration:
                pass

            except catch as e_:
                e = e_
                self.print_raise(e, back=back + 1)

            if i < lb-1:
                raise MissingYieldException(get_fstr(
                    fmt=':: test {!r} {!s}',
                    args=('missing yield#{} < {}'.format(i+1, lb),),
                    back=back + 1,
                ))

        if ub is not None:

            try:
                while i < ub:
                    value = next(it)
                    i += 1
                    self.print_yield(value, index=i+1, back=back+1)

            except StopIteration:
                pass

            except catch as e_:
                e = e_
                self.print_raise(e, back=back + 1)

            if i >= ub:
                raise RedundantYieldException(get_fstr(
                    fmt=':: test {!r} {!s}',
                    args=('redundant yield#{} > {}'.format(i+1, ub),),
                    back=back + 1,
                ))

        return e

    # </editor-fold>

    def test__yield_(self):
        self.validate_yield(yield_(dict_0), n=1)
        
    def test__ireturn(self):
        self.validate_yield(ireturn(f), n=1)

    def test__iraise(self):
        self.validate_yield(iraise(e0_0), n=0, catch=e0)

    def test__iempty(self):
        self.validate_yield(iempty, ub=0)

    def test__ipass(self):
        self.validate_yield(ipass(**dict_0), n=0)

    def test__itry(self):
        self.validate_yield(itry(ge), n=3)

    def test__itry__raise(self):
        self.validate_yield(itry(ge, h=iraise), n=3, catch=e0)

    def test__itry1(self):
        self.validate_yield(itry1(f, catch=e0), n=1)

    def test__itry1__raise(self):
        self.validate_yield(itry1(fe, h=iraise, catch=e0), n=0, catch=e0)

    # <editor-fold desc="iget">

    def test__iget(self):
        self.validate_yield(iget_item(dict_0, 'b'), n=1)

    def test__iget__missing(self):
        self.validate_yield(iget_item(dict_0, 'x'), n=0)

    def test__iget__missing__raise(self):
        self.validate_yield(iget_item(dict_0, 'x', h=iraise), n=0, catch=KeyError)

    # </editor-fold>
    # <editor-fold desc="iget_attr">

    def test__iget_attr(self):
        self.validate_yield(iget_attr(dummy_0, 'b'), n=1)

    def test__iget_attr__missing(self):
        self.validate_yield(iget_attr(dummy_0, 'x'), n=0)

    def test__iget_attr__missing__raise(self):
        self.validate_yield(iget_attr(dummy_0, 'x', h=iraise), n=0, catch=AttributeError)

    # </editor-fold>
    pass


class TestRepr (unittest.TestCase):
    
    def test__get_function_name(self):
        self.assertEqual(get_function_name(), 'test__get_function_name')
        pass
    
    def test__fstr(self):

        x = 'wow'

        s = fstr('|{x}|{yield_validation}|{1}|{y}|{0}|', 5, 44, y=42, yield_validation='hello')

        self.assertEqual(s, "|wow|hello|5|42|test__fstr|")

        pass
    
    pass


class TestExperiments (unittest.TestCase):
    
    def test__000(self):

        keys = 'abxcd'

        with self.assertRaises(StopIteration):
            value = get_next(iempty)

        with self.assertRaises(KeyError):
            value = get_item(dict_0, 'x')

        with self.assertRaises(AttributeError):
            value = get_attr(dummy_0, 'x')

        print(get_attr(dummy_0, 'd', 'wow', f=float))
        print(get_attr(dummy_0, 'x', 'wow', f=float))

        print(get_obj_type_name(dummy_0))

        pass

    def test__001(self):
        pass

    pass


########################################################################################################################
