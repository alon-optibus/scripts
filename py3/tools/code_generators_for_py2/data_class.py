from tools.code_generators_for_py2 import put

class_name = 'VipScenario'

class_bases = (object,)

attrs = [
    'description',
    'algorithm_data_set',
    'data_set',
    'trips',
    'vehicle_types',
    'depots',
    'trip_parameters',
    'vehicle_type_parameters',
    'depot_parameters',
    'all_vehicle_parameters',
    'scheduler',
    'vehicles',
    'locked_trip_ids',
    'expected_mid_day_depot_parkings',
    'expected_number_of_rows',
    'expected_number_of_cols',
    'expected_number_of_trips',
    'expected_number_of_vehicle_variations',
    'expected_number_of_vehicle_active_bounds',
    'expected_number_of_trips_require_scheduling',
    'expected_number_of_locked_trips',
    'expected_number_of_trip_active_bounds',
    'expected_number_of_trip_groups_with_active_bounds',
    'expected_number_of_vehicle_groups_with_active_bounds',
]

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
