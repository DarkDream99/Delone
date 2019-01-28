import math

from .base import BASE_POINT
from .base import ccw_comparator
from .base import sort_point
from .point import Point
from .segment import Segment


class Circle (object):

    def __init__(self, center=None, radius=None, **kwargs):
        if len(kwargs) == 0:
            self.center = center
            self.radius = radius
        else:
            self._init_by_points(kwargs["point_a"], kwargs["point_b"], kwargs["point_c"])

    def _init_by_points(self, a, b, c):
        d = 2 * (a.x * (b.y - c.y) + b.x * (c.y - a.y) + c.x * (a.y - b.y))
        if d == 0:
            ux, uy = 0, 0
            self.radius = 0
            self.center = Point(ux, uy)
        else:
            ux = ((a.x ** 2 + a.y ** 2)*(b.y - c.y) + (b.x ** 2 + b.y ** 2)*(c.y - a.y)
                  + (c.x ** 2 + c.y ** 2)*(a.y - b.y)) / d
            uy = ((a.x ** 2 + a.y ** 2)*(c.x - b.x) + (b.x ** 2 + b.y ** 2)*(a.x - c.x)
                  + (c.x ** 2 + c.y ** 2)*(b.x - a.x)) / d

            self.center = Point(ux, uy)
            self.radius = Segment(self.center, a).length

        points = [a, b, c]
        sorted_points = sort_point(points, ccw_comparator)
        self.middle = sorted_points[1]

    @property
    def center(self):
        return self._center

    @center.setter
    def center(self, value):
        if not isinstance(value, Point):
            raise ValueError(f"center is instance of class Point, not {type(value)}")

        self._center = value

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, value):
        if not isinstance(value, (int, float)):
            raise ValueError(f"radius is integer or float number, not {type(value)}")

        self._radius = value

    def __contains__(self, item):
        if isinstance(item, Point):
            distance_to_center = Segment(item, self.center).length
            return distance_to_center < self.radius
        raise ValueError(f"item must be instance of Point, not {type(item)}")

    def __str__(self):
        return f"Circle (" \
               f"\n\tcenter: {self.center}" \
               f"\n\tradius: {self.radius})"
