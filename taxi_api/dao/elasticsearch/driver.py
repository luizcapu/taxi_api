__author__ = 'luiz'

from base import DBBaseDao
from taxi_api.to.driver import DriverTO


class DriverDao(DBBaseDao):
    _default_table = "driver"
    _to_class = DriverTO

    def list_in_rectangle(self, top_left, bottom_right, only_active=True,
                          top_left_exclude=None, bottom_right_exclude=None):
        #{"lat":40.722, "lon":-73.989}
        must = [
            {
                "geo_bounding_box": {
                    "location": {
                        "top_left": top_left,
                        "bottom_right": bottom_right
                    }
                }
            }
        ]

        if only_active:
            must.append({"term":{"available":True}})

        conditions = dict(must=must)

        if top_left_exclude and bottom_right_exclude:
            conditions["must_not"] = [
                {
                    "geo_bounding_box": {
                        "location": {
                            "top_left": top_left_exclude,
                            "bottom_right": bottom_right_exclude
                        }
                    }
                }
            ]

        query = {
            "query": {
                "filtered": {
                    "filter": {
                        "bool": conditions
                    }
                }
            }
        }
        return self._run_query(query)