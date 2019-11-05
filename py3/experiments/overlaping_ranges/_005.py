from random import randint, seed
from my.iter_utils import iter_validate_sorted, iter_overlaps

INF = float('inf')

########################################################################################################################

start_min = 0
start_max = 50
length_min = 1
length_max = 10

number_of_ranges = 30

########################################################################################################################


def iter_overlaps__with_validation(start_end_value, is_sorted=False, lb=-INF, ub=INF):

    prev_b0 = lb

    if is_sorted:
        start_end_value = iter_validate_sorted(start_end_value)

    start_end_value = list(start_end_value)

    ranges = {
        (start, end)
        for start, end, value in start_end_value
    }

    for a0, b0, group in iter_overlaps(
            starts_ends_values=(
                (start, end, (start, end, value))
                for start, end, value in start_end_value
            ),
            is_sorted=is_sorted,
            lb=lb,
            ub=ub,
    ):

        group = list(group)

        group_values = (
            value
            for start, end, value in group
        )

        group_ranges = {
            (start, end)
            for start, end, value in group
        }

        assert lb <= prev_b0 == a0 < b0 <= ub, f'prev_b0={prev_b0}, a0={a0}, b0={b0}, lb={lb}, ub={ub}'

        for a, b in group_ranges:
            assert a <= a0 and b0 <= b

        for a, b in ranges - group_ranges:
            assert a < lb or b > ub or b < b0 or a0 < a

        prev_b0 = b0

        yield a0, b0, group_values

    assert prev_b0 >= ub


########################################################################################################################

if __name__ == '__main__':

    for run_index in range(100):

        seed(run_index)

        ranges = [
            (x0, x0+dx)
            for x0, dx in (
                (randint(start_min, start_max), randint(length_min, length_max))
                for i in range(number_of_ranges)
            )
        ]

        ranges.sort()

        # ranges = ()

        for a0, b0, group in iter_overlaps__with_validation(
            (r + (r,)for r in ranges),
            is_sorted=True,
            lb=10,
            ub=30,
        ):
            if run_index == 0:
                group = sorted(group)
                print(f'{a0:>4} : {b0:>4} | {len(group):>2} | {group}')

########################################################################################################################
