from tools.code_generators_for_py2 import put

attrs = [
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

v = 2

########################################################################################################################

for attr in attrs:
    put(v, f"")
    put(v, f"self.assertEqualAttrs(")
    put(v+1, f"scenario, '{attr}',")
    put(v+1, f"scenario, '{attr[9:]}'")
    put(v, f")")

########################################################################################################################
