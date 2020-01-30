from typing import Iterable, Tuple, Iterator, TypeVar, Callable
from toolz import identity
from itertools import tee

T1 = TypeVar('T1')
T2 = TypeVar('T2')

########################################################################################################################


def pairwise(iterable: Iterable):
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


def eq(*items):
    return iter_eq(items)


def iter_eq(items):
    for a, b in pairwise(items):
        if not a == b:
            return False
    return True


def map_iter_eq(*iters):
    return map(iter_eq, zip(*iters))


def all_iter_eq(*iters):
    return all(map_iter_eq(*iters))


def iter_validate_sorted(
        iterator: Iterable,
        *,
        key: Callable = identity,
        cmp: Callable = (lambda prev, cur: prev <= cur),
        exception: Exception = AssertionError('Validation faild because the given iterator is not sorted'),
):

    iterator = iter(iterator)

    try:
        item = next(iterator)
    except StopIteration:
        return

    yield item

    prev = key(item)

    for item in iterator:

        cur = key(item)

        if not cmp(prev, cur):
            raise exception

        yield item

        prev = cur

    pass


########################################################################################################################


def iter_overlaps(
        starts_ends_values: Iterable[Tuple[T1, T1, T2]],
        is_sorted: bool = False,
        lb: T1 = -float('inf'),
        ub: T1 = float('inf'),
) -> Iterator[Tuple[T1, T1, Iterator[T2]]]:
    """
    this generator yields triples `l0, u0, group` such that each satisfys the foolowing:

        lb <= l0 < u0 <= ub

        each triple `l, u, _` from `starts_ends_values` satisfys:
            l <= l0 < u0 <= u or u <= l0 or u0 <= l

        `group` is a generator that yields the same values (not necessarily in the same order) as the following:
            (
                value
                for l, u, value in starts_ends_values
                if l <= l0 < u0 <= u
            )

    for more properties of the results of this generator, let:

        A = { (l, u) for l, u, _ in starts_ends_values }

        s(l0, u0) = { (l, u) for l, u in A if l <= l0 < u0 <= u }

        r(x) = { (l, u) for l, u in A if l <= x < u }

        P = [ (l0, u0) for l0, u0, _ in iter_overlaps(starts_ends_values) ]

        S = { s(l0, u0) for l0, u0 in P }

        R = { r(x) for each x that satisfy lb < x < ub }

    then:

        S == R

        for l0, u0 in P:
            for any `x` that satisfy `l0 <= x < ub`:
                r(x) == s(l0, u0)

        the sequnce `P` represents a partition of the range `lb` to `ub`.

        for any `x` that satisfy `lb < x < ub` thre exists exactly one pair `(l0, u0)` in `P` such that `l0 <= x < u0`.

        P[0][0] == lb
        P[-1][1] == ub

        for i in range(len(P)-1):
            P[i][1] == P[i+1][0]

    example:

        iter_overlaps([(0, 5, (0, 5)), (2, 3, (2, 3)), (4, 5, (4, 5)), (7, 10, (7, 10))] -->
            (-inf, 0, [])
            (0, 2, [(0, 5)])
            (2, 3, [(0, 5), (2, 3)])
            (3, 4, [(0, 5)])
            (4, 5, [(0, 5), (4, 5)])
            (5, 7, [])
            (7, 10, [(7, 10)])
            (10, inf, [])

    """

    from heapq import heappush, heappop

    if ub <= lb:
        return

    if not is_sorted:
        starts_ends_values = sorted(starts_ends_values)

    group_start = lb
    heap = []

    for start, end, value in starts_ends_values:

        if end <= group_start:
            continue

        if group_start < start:

            if ub <= start:
                break

            while heap:

                group_end = heap[0][0]

                if start <= group_end:
                    break

                if group_start < group_end:
                    yield group_start, group_end, (x[1] for x in heap)

                    group_start = group_end

                heappop(heap)

            yield group_start, start, (x[1] for x in heap)

            group_start = start

        heappush(heap, (end if end < ub else ub, value))

    while heap:

        group_end = heap[0][0]

        if group_start < group_end:
            yield group_start, group_end, (x[1] for x in heap)

            group_start = group_end

        heappop(heap)

    if group_start < ub:
        yield group_start, ub, ()

    pass


########################################################################################################################
