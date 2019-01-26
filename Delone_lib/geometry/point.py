import math


class Point(object):

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        if isinstance(value, (float, int)):
            self._x = value
        else:
            raise ValueError("coordinate x can be integer or float")

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        if isinstance(value, (float, int)):
            self._y = value
        else:
            raise ValueError("coordinate y can be integer or float")

    def __sub__(self, other):
        res_x = self.x - other.x
        res_y = self.y - other.y
        res_point = Point(res_x, res_y)
        return res_point

    def __add__(self, other):
        res_x = self.x + other.x
        res_y = self.y + other.y
        res_point = Point(res_x, res_y)
        return res_point

    def __truediv__(self, num):
        res_x = self.x / num
        res_y = self.y / num
        res_point = Point(res_x, res_y)
        return res_point

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        # TODO change hash function
        return int(self.x) * 123 + int(self.y) * 127

    def distance_to_point(self, other_point):
        return math.sqrt((self.x - other_point.x) ** 2 + (self.y - other_point.y) ** 2)

    @staticmethod
    def higher(point_a, point_b):
        if point_a.y > point_b.y:
            return True
        elif point_a.y == point_b.y:
            return point_a.x > point_b.x

    def __str__(self):
        return f"{{type=Point, x={self.x}, y={self.y}}}"
