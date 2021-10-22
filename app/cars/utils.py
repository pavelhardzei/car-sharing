import math
from decimal import Decimal


def count_distances(user_loc, available_cars):
    loc_rad = user_loc[0] * Decimal(math.pi) / 180, user_loc[1] * Decimal(math.pi) / 180
    cars_locs_rad = [(car.car_info.longitude * Decimal(math.pi) / 180,
                      car.car_info.latitude * Decimal(math.pi) / 180) for car in available_cars]

    earth_radius = 6378.8
    distances = [earth_radius * math.acos(math.sin(loc_rad[1]) * math.sin(car_loc[1]) +
                 math.cos(loc_rad[1]) * math.cos(car_loc[1]) * math.cos(car_loc[0] - loc_rad[0]))
                 for car_loc in cars_locs_rad]

    return distances
