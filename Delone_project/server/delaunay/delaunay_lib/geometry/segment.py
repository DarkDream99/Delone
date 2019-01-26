import math

from .point import Point


class Segment(object):

    def __init__(self, start, end):
        self.start = start
        self.end = end

    @property
    def start(self):
        return self._start_point

    @start.setter
    def start(self, value):
        if isinstance(value, Point):
            self._start_point = value
        else:
            raise ValueError(f"start point is instance of class Point not of {type(value)}")

    @property
    def end(self):
        return self._end_point

    @end.setter
    def end(self, value):
        if isinstance(value, Point):
            self._end_point = value
        else:
            raise ValueError(f"end point is instance of class Point not of {type(value)}")

    @property
    def length(self):
        return self.start.distance_to_point(self.end)

    def contains_point(self, point):
        distance_from_start = self.start.distance_to_point(point)
        distance_from_end = self.end.distance_to_point(point)

        return math.fabs(self.length - distance_from_start - distance_from_end) <= 1e-9

    def __eq__(self, other):
        return (self.start == other.start and self.end == other.end) or \
               (self.start == other.end and self.end == other.start)

    def __hash__(self):
        # TODO change hash-function
        return hash(self.start) + hash(self.end)

    def __str__(self):
        return f"{{\"type\": \"Segment\", \"start\": {self.start}, \"end\": {self.end}}}"
