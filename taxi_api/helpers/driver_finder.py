__author__ = 'luiz'

from taxi_api.helpers.helpers import Helpers
from taxi_api.business.driver import DriverBus
import math
from random import randint


class DriverFinder(object):

    _lat_inc = 3
    _score_cutoff = 10

    def __init__(self):
        self.cfg = Helpers.load_config()
        self.ds_name = self.cfg["api"]["database"]
        self.environ = self.cfg["env"]
        self.driver_bus = DriverBus(self.ds_name, self.environ)
        self.score_cutoff = 10  # ignore drivers with score lower than cutoff

    def run(self, requester_location, desired_drivers, max_depth=5, requester_preferences=None):
        requester_location = Helpers.validate_geo_point(requester_location)
        result = []
        last_bounding_box = (None, None)
        exp_factor = 1
        while len(result) < desired_drivers and exp_factor <= max_depth:
            # TODO check if calculation of bounding_box is correct
            left = requester_location["lat"] + (pow(DriverFinder._lat_inc, exp_factor) / 69.0)
            top = 3960 * 2 * math.pi / 360 * math.cos(left)
            top_left = Helpers.validate_geo_point((left, top))

            right = requester_location["lat"] - (pow(DriverFinder._lat_inc, exp_factor) / 69.0)
            bottom = 3960 * 2 * math.pi / 360 * math.cos(right)
            bottom_right = Helpers.validate_geo_point((right, bottom))

            drivers_in_area = self.driver_bus.list_in_rectangle(
                top_left, bottom_right, True,
                last_bounding_box[0], last_bounding_box[1]  # area to exclude
            )

            # TODO parallel processing of calculate drivers scores
            for driver in drivers_in_area:
                score = self.calculate_driver_score(driver, requester_location, requester_preferences)
                if score > DriverFinder._score_cutoff:
                    result.append((driver, score))

            last_bounding_box = (top_left, bottom_right)
            print last_bounding_box
            exp_factor += 1

        def get_score(item):
            return item[1]
        # return drivers ordered by score
        return [driver[0] for driver in sorted(result, key=get_score, reverse=True)]

    def calculate_driver_score(self, driver, requester_location, requester_preferences):
        # TODO implement real score calculation
        return randint(0, 99)


if __name__ == '__main__':
    finder = DriverFinder()
    print finder.run((0, 0), 10)
