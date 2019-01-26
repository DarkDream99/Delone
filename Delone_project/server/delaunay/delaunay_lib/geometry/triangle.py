from . import base
from .base import left_turn

from .point import Point
from .segment import Segment
from .circle import Circle


class Triangle(object):

    _count = 0

    def __init__(self, point_a, point_b, point_c):
        self._number = Triangle._count
        Triangle._count += 1

        self._point_a = point_a
        self._point_b = point_b
        self._point_c = point_c

        self._segments = [
            Segment(point_a, point_b),
            Segment(point_b, point_c),
            Segment(point_c, point_a)
        ]

        self._near_triangles = [
            [self._segments[0], None],
            [self._segments[1], None],
            [self._segments[2], None]
        ]

    @property
    def number(self):
        return self._number

    @property
    def point_a(self):
        return self._point_a

    @point_a.setter
    def point_a(self, value):
        if isinstance(value, Point):
            self._point_a = value
        else:
            raise ValueError(f"point A is instance of Point not of {type(value)}")

    @property
    def point_b(self):
        return self._point_b

    @point_b.setter
    def point_b(self, value):
        if isinstance(value, Point):
            self._point_b = value
        else:
            raise ValueError(f"point B is instance of Point not of {type(value)}")

    @property
    def point_c(self):
        return self._point_c

    @point_c.setter
    def point_c(self, value):
        if isinstance(value, Point):
            self._point_c = value
        else:
            raise ValueError(f"point C is instance of Point not of {type(value)}")

    @property
    def points(self):
        return [self.point_a, self.point_b, self.point_c]

    @property
    def segments(self):
        return self._segments

    @property
    def near_triangles(self):
        res_triangles = []
        for segment in self.segments:
            res_triangles.append(self.get_near_triangle_by_segment(segment))
        return res_triangles

    def last_points(self, used_points):
        res = []
        if self.point_a not in used_points:
            res.append(self.point_a)
        if self.point_b not in used_points:
            res.append(self.point_b)
        if self.point_c not in used_points:
            res.append(self.point_c)
        return res

    def get_near_triangle_by_segment(self, segment):
        if segment not in self._segments:
            raise ValueError(f"{segment} is not part of triangle {self}")

        for near in self._near_triangles:
            if near[0] == segment:
                return near[1]

    def set_near_triangle_by_segment(self, segment, new_triangle):
        if segment not in self._segments:
            raise ValueError(f"{segment} is not part of triangle {self}")

        for near in self._near_triangles:
            if near[0] == segment:
                near[1] = new_triangle

    def get_common_segment(self, other_triangle):
        for segment_a in self.segments:
            for segment_b in other_triangle.segments:
                if segment_a == segment_b:
                    return segment_a
        return None

    def split_by_point(self, point):
        lie_on_segment = False
        contaned_segment = None
        for segment in self._segments:
            if segment.contains_point(point):
                lie_on_segment = True
                contaned_segment = segment

        if lie_on_segment:
            res_triangles, changes = self._add_four_triangles(contaned_segment, point)
        else:
            res_triangles, changes = self._add_three_triangles(point)

        return res_triangles, changes

    def _add_four_triangles(self, segment, point):
        common_points = [segment.start, segment.end]
        last_point_a = self.last_points(common_points)[0]
        changes = dict()

        triangle_a = Triangle(common_points[0], last_point_a, point)
        triangle_b = Triangle(common_points[1], last_point_a, point)
        Triangle.join(triangle_a, triangle_b)
        for near_triangle in self.near_triangles:
            Triangle.join(triangle_a, near_triangle)
            Triangle.join(triangle_b, near_triangle)
        res_triangles = [triangle_a, triangle_b]
        changes[self] = [triangle_a, triangle_b]

        near_triangle = self.get_near_triangle_by_segment(segment)
        if near_triangle is not None:
            last_point_b = near_triangle.last_points(common_points)[0]
            triangle_c = Triangle(common_points[0], last_point_b, point)
            triangle_d = Triangle(common_points[1], last_point_b, point)

            Triangle.join(triangle_a, triangle_c)
            Triangle.join(triangle_b, triangle_d)
            Triangle.join(triangle_c, triangle_d)

            for near_triangle in self.near_triangles:
                Triangle.join(triangle_c, near_triangle)
                Triangle.join(triangle_d, near_triangle)
            res_triangles += [triangle_b, triangle_d]
            changes[near_triangle] = [triangle_c, triangle_d]

        return res_triangles, changes

    def _add_three_triangles(self, point):
        triangle_a = Triangle(self.point_a, self.point_b, point)
        triangle_b = Triangle(self.point_b, self.point_c, point)
        triangle_c = Triangle(self.point_c, self.point_a, point)

        Triangle.join(triangle_a, triangle_b)
        Triangle.join(triangle_a, triangle_c)
        Triangle.join(triangle_b, triangle_c)

        for near_triangle in self.near_triangles:
            Triangle.join(near_triangle, triangle_a)
            Triangle.join(near_triangle, triangle_b)
            Triangle.join(near_triangle, triangle_c)
        changes = dict()
        changes[self] = [triangle_a, triangle_b, triangle_c]

        return [triangle_a, triangle_b, triangle_c], changes

    def __contains__(self, item):
        if isinstance(item, Point):
            return self._contains_point(item)

    def _contains_point(self, point):
        base.BASE_POINT = self.point_a
        left_turn_a = left_turn(self.point_b, point)
        base.BASE_POINT = self.point_b
        left_turn_b = left_turn(self.point_c, point)
        base.BASE_POINT = self.point_c
        left_turn_c = left_turn(self.point_a, point)

        comm_value = 0
        if left_turn_a != 0:
            comm_value = left_turn_a

        if comm_value != 0:
            if left_turn_b != 0:
                if left_turn_b != comm_value:
                    return False
        else:
            if left_turn_b != 0:
                comm_value = left_turn_b

        if comm_value != 0:
            if left_turn_c != 0:
                if left_turn_c != comm_value:
                    return False

        return True

    @staticmethod
    def join(triangle_a, triangle_b):
        if triangle_a is None or triangle_b is None:
            return
        common_segment = triangle_a.get_common_segment(triangle_b)
        if common_segment is not None:
            triangle_a.set_near_triangle_by_segment(common_segment, triangle_b)
            triangle_b.set_near_triangle_by_segment(common_segment, triangle_a)

    @staticmethod
    def change_common_segment(triangle_a, triangle_b):
        common_segment = triangle_a.get_common_segment(triangle_b)
        common_points = [common_segment.start, common_segment.end]
        last_point_a = triangle_a.last_points(common_points)[0]
        last_point_b = triangle_b.last_points(common_points)[0]

        new_triangle_a = Triangle(last_point_a, common_points[0], last_point_b)
        new_triangle_b = Triangle(last_point_a, common_points[1], last_point_b)
        Triangle.join(new_triangle_a, new_triangle_b)

        for near_triangle in triangle_a.near_triangles:
            if triangle_b != near_triangle:
                Triangle.join(new_triangle_a, near_triangle)
                Triangle.join(new_triangle_b, near_triangle)

        for near_triangle in triangle_b.near_triangles:
            if triangle_a != near_triangle:
                Triangle.join(new_triangle_a, near_triangle)
                Triangle.join(new_triangle_b, near_triangle)

        return [new_triangle_a, new_triangle_b]

    def vertex_with_max_angle(self):
        cos_a = self.segments[0].length ** 2 + self.segments[1].length ** 2 - self.segments[2].length ** 2 \
                / 2 * self.segments[0].length + self.segments[1].length
        cos_b = self.segments[1].length ** 2 + self.segments[2].length ** 2 - self.segments[0].length ** 2 \
                / 2 * self.segments[1].length + self.segments[2].length
        cos_c = self.segments[2].length ** 2 + self.segments[0].length ** 2 - self.segments[1].length ** 2 \
                / 2 * self.segments[2].length + self.segments[0].length

        if cos_a <= cos_b and cos_a <= cos_c:
            if self.segments[0].start in [self.segments[1].start, self.segments[1].end]:
                return self.segments[0].start
            else:
                return self.segments[0].end

        if cos_b <= cos_a and cos_b <= cos_c:
            if self.segments[1].start in [self.segments[2].start, self.segments[2].end]:
                return self.segments[1].start
            else:
                return self.segments[1].end

        if cos_c <= cos_b and cos_c <= cos_a:
            if self.segments[2].start in [self.segments[0].start, self.segments[0].end]:
                return self.segments[2].start
            else:
                return self.segments[2].end

    def __eq__(self, other):
        if other is None:
            return False
        return self.point_a == other.point_a and self.point_b == other.point_b and self.point_c == other.point_c

    def __hash__(self):
        return hash(self.point_a) + hash(self.point_b) + hash(self.point_c)

    def __repr__(self):
        return f"Triangle (" \
               f"\n\tnumber: {self.number}" \
               f"\n\tpoint_a: {self.point_a}" \
               f"\n\tpoint_b: {self.point_b}" \
               f"\n\tpoint_c: {self.point_c})"

    def __str__(self):
        nears = ['[']
        for near in self.near_triangles:
            if near is None:
                continue
            nears.append(f"[{near.point_a}, {near.point_b}, {near.point_c}]")
            nears.append(',')

        if len(nears) > 1:
            nears.pop()
        nears.append(']')
        nears = "".join(nears)

        circle = Circle(point_a=self.point_a, point_b=self.point_b, point_c=self.point_c)
        str_circle = f"{{\"type\": \"Circle\", \"x\": \"{circle.center.x}\", \"y\": \"{circle.center.y}\", " \
                     f"\"r\": \"{circle.radius}\"}}"
        return f"{{\"number\": \"{self.number}\", \"point_a\": {self.point_a}, \"point_b\": {self.point_b}," \
               f"\"point_c\": {self.point_c}, \"nears\": {nears}, \"circle\": {str_circle}}}"
