__author__ = 'luiz'

from base import DBBaseDao
from ...to.driver import DriverTO


class DriverDao(DBBaseDao):
    _default_table = "driver"
    _to_class = DriverTO

    def list_in_rectangle(self, top_left, bottom_right, only_active=True):
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

        query = {
            "query": {
                "filtered": {
                    "filter": {
                        "bool": {
                            "must": must
                        }
                    }
                }
            }
        }
        return self._run_query(query)