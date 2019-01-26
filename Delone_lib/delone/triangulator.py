import copy
import json

from geometry import base
from . import event
from geometry.base import sort_point
from geometry.base import lexicographical_comparator
from geometry.base import ccw_comparator
from geometry.base import cw_comparator

from geometry.point import Point
from geometry.triangle import Triangle
from geometry.segment import Segment
from geometry.circle import Circle

from .locator import LocationTree
from .event import Event
from .serialize import serialize


class Triangulator(object):

    def __init__(self, points):
        self._points = list(set(points))
        self._base_triangle = None
        self._down_base_point = None
        self._top_base_point = None
        self._higher_point = None
        self._locator = None
        self._events = []

    def make_triangulation(self):
        self._events.append(
            Event(
                ev_type=event.NEW_STAGE,
                description="Создание базового триугольника"
            )
        )
        self._init_base_triangle()

        self._events.append(
            Event(
                ev_type=event.NEW_STAGE,
                description="Иницилизация дерева локализации точки"
            )
        )
        self._locator = LocationTree(self._base_triangle)

        self._events.append(
            Event(
                ev_type=event.NEW_STAGE,
                description="Перестановка точек"
            )
        )
        self._points = base.permutation(self._points)

        for point in self._points:
            if point == self._higher_point:
                continue
            self._events.append(
                Event(
                    ev_type=event.SELECT_POINT,
                    data=point,
                    description=f"Добавляем {point}"
                )
            )
            self._insert_point(point)

        self._events.append(
            Event(ev_type=event.NEW_STAGE, description="Удаление базового триугольника"))
        self._delete_base_triangle()

    def get_events(self):
        return self._events

    def get_events_json(self):
        return json.dumps(self._events, default=serialize)

    def _init_base_triangle(self):
        left_bound = self._points[0].x - 1
        right_bound = self._points[0].x + 1
        top_bound = self._points[0].y + 1
        down_bound = self._points[0].y - 1
        higher_point = self._points[0]

        for point in self._points:
            if point.x >= right_bound:
                right_bound = point.x + 1
            if point.x <= left_bound:
                left_bound = point.x - 1
            if point.y >= top_bound:
                top_bound = point.y + 1
                higher_point = point
            if point.y <= down_bound:
                down_bound = point.y - 1

        self._higher_point = higher_point
        self._events.append(Event(ev_type=event.SELECT_BASE_POINT, data=higher_point))
        down_base_point = self._find_down_base_point(right_bound, down_bound)
        self._down_base_point = down_base_point
        self._events.append(Event(ev_type=event.SELECT_BASE_POINT, data=down_base_point))
        top_base_point = self._find_top_base_point(left_bound, top_bound, down_base_point)
        self._top_base_point = top_base_point
        self._events.append(Event(ev_type=event.SELECT_BASE_POINT, data=top_base_point))
        self._base_triangle = Triangle(down_base_point, top_base_point, higher_point)

        self._events.append(Event(ev_type=event.ADD_BASE_SEGMENT, data=Segment(down_base_point, top_base_point)))
        self._events.append(Event(ev_type=event.ADD_BASE_SEGMENT, data=Segment(down_base_point, higher_point)))
        self._events.append(Event(ev_type=event.ADD_BASE_SEGMENT, data=Segment(higher_point, top_base_point)))

    def _delete_base_triangle(self):
        triangles = self._locator.leaves
        used_segments = set()
        for triangle in triangles:
            if self._down_base_point in triangle:
                for segment in triangle.segments:
                    if segment.contains_point(self._down_base_point) and segment not in used_segments:
                        self._events.append(Event(ev_type=event.DELETE_SEGMENT, data=segment))
                        used_segments.add(segment)
            if self._top_base_point in triangle:
                for segment in triangle.segments:
                    if segment.contains_point(self._top_base_point) and segment not in used_segments:
                        self._events.append(Event(ev_type=event.DELETE_SEGMENT, data=segment))
                        used_segments.add(segment)

    def _find_down_base_point(self, right_bound, down_bound):
        points_a = copy.deepcopy(self._points)
        points_b = copy.deepcopy(self._points)
        left = right_bound
        right = 1e9
        res_point = None
        while right - left >= 0:
            middle = left + (right - left) // 2
            base.BASE_POINT = Point(x=middle, y=down_bound)

            points_a = sort_point(points_a, lexicographical_comparator)
            points_b = sort_point(points_b, cw_comparator)

            equal_point_sets = True
            for i in range(len(points_a)):
                if points_a[i] != points_b[i]:
                    equal_point_sets = False
                if points_a[i] != self._higher_point:
                    if Segment(self._higher_point, base.BASE_POINT).contains_point(points_a[i]):
                        equal_point_sets = False

            if equal_point_sets:
                right = middle - 1
                res_point = base.BASE_POINT
            else:
                left = middle + 1

        return res_point

    def _find_top_base_point(self, left_bound, top_bound, down_base_point):
        points_a = copy.deepcopy(self._points + [down_base_point])
        points_b = copy.deepcopy(self._points + [down_base_point])

        left = -1e9
        right = left_bound
        res_point = None
        while right - left >= 0:
            middle = left + (right - left) // 2
            base.BASE_POINT = Point(x=middle, y=top_bound)

            points_a = sort_point(points_a, lexicographical_comparator)
            points_b = sort_point(points_b, ccw_comparator)

            equal_point_sets = True
            for i in range(len(points_a)):
                if points_a[i] != points_b[i]:
                    equal_point_sets = False
                if points_a[i] != self._down_base_point:
                    if Segment(base.BASE_POINT, self._down_base_point).contains_point(points_a[i]):
                        equal_point_sets = False

            if equal_point_sets:
                left = middle + 1
                res_point = base.BASE_POINT
            else:
                right = middle - 1

        return res_point

    def _insert_point(self, point):
        base_triangle = self._locator.point_location(point)
        res_triangles, changes = base_triangle.split_by_point(point)

        for key in changes:
            self._locator.add_triangle_children(key, changes[key])

        next_changes = []
        used_triangles = []
        for triangle in changes:
            # inside triangle
            if len(changes[triangle]) == 3:
                self._events.append(Event(ev_type=event.ADD_SEGMENT, data=Segment(point, base_triangle.point_a)))
                self._events.append(Event(ev_type=event.ADD_SEGMENT, data=Segment(point, base_triangle.point_b)))
                self._events.append(Event(ev_type=event.ADD_SEGMENT, data=Segment(point, base_triangle.point_c)))

                segment_a = Segment(base_triangle.point_a, base_triangle.point_b)
                temp_changes = self._legalize_by_segment(changes[triangle], segment_a)
                next_changes.extend(temp_changes)

                segment_b = Segment(base_triangle.point_b, base_triangle.point_c)
                temp_changes = self._legalize_by_segment(changes[triangle], segment_b)
                next_changes.extend(temp_changes)

                segment_c = Segment(base_triangle.point_c, base_triangle.point_a)
                temp_changes = self._legalize_by_segment(changes[triangle], segment_c)
                next_changes.extend(temp_changes)
            # on segment
            else:
                triangle_a, triangle_b = changes[triangle]
                common_segment = triangle_a.get_common_segment(triangle_b)
                self._events.append(Event(ev_type=event.ADD_SEGMENT, data=common_segment))
                point_i = triangle_a.last_points([common_segment.start, common_segment.end])[0]
                point_j = triangle_b.last_points([common_segment.start, common_segment.end])[0]
                base_segment = Segment(point_i, point_j)
                if base_segment.contains_point(common_segment.start):
                    start_point = common_segment.end
                else:
                    start_point = common_segment.start

                segment_a = Segment(point_i, start_point)
                next_changes = self._legalize_segment(triangle_a, segment_a)
                segment_b = Segment(point_j, start_point)
                temp_changes = self._legalize_segment(triangle_b, segment_b)
                next_changes.extend(temp_changes)

            for base_triangle, new_triangles in next_changes:
                self._locator.add_triangle_children(base_triangle, new_triangles)
            next_changes.clear()
            used_triangles.append(triangle)

        for triangle in used_triangles:
            self._locator.clear_leaf(triangle)

    def _legalize_by_segment(self, triangles, segment):
        for triangle in triangles:
            if segment in triangle.segments:
                changes = self._legalize_segment(triangle, segment)
                return changes

    def _legalize_segment(self, triangle, segment):
        changes = []
        if self._is_legal_segment(triangle, segment):
            return changes

        point_i = segment.start
        point_j = segment.end
        near_triangle = triangle.get_near_triangle_by_segment(segment)
        point_k = near_triangle.last_points([point_i, point_j])[0]
        self._events.append(Event(ev_type=event.DELETE_SEGMENT, data=segment))

        new_triangle_a, new_triangle_b = Triangle.change_common_segment(triangle, near_triangle)
        new_common_segment = new_triangle_a.get_common_segment(new_triangle_b)
        self._events.append(Event(ev_type=event.ADD_SEGMENT, data=new_common_segment))
        changes.append([triangle, [new_triangle_a, new_triangle_b]])
        changes.append([near_triangle, [new_triangle_a, new_triangle_b]])
        if point_i in new_triangle_a.points:
            next_changes = self._legalize_segment(new_triangle_a, Segment(point_i, point_k))
        else:
            next_changes = self._legalize_segment(new_triangle_b, Segment(point_i, point_k))

        changes.extend(next_changes)

        if point_j in new_triangle_a.points:
            next_changes = self._legalize_segment(new_triangle_a, Segment(point_j, point_k))
        else:
            next_changes = self._legalize_segment(new_triangle_b, Segment(point_j, point_k))

        changes.extend(next_changes)
        return changes

    def _is_legal_segment(self, triangle, segment):
        if segment in self._base_triangle.segments:
            return True

        point_i = segment.start
        point_j = segment.end
        point_l = triangle.last_points([point_i, point_j])[0]
        near_triangle = triangle.get_near_triangle_by_segment(segment)
        point_k = near_triangle.last_points([point_i, point_j])[0]

        ind_i = self._point_index(point_i)
        ind_j = self._point_index(point_j)
        ind_l = self._point_index(point_l)
        ind_k = self._point_index(point_k)

        # circle = Circle(point_a=point_i, point_b=point_j, point_c=point_l)
        # return point_k not in circle

        if ind_i > 0 and ind_j > 0 and ind_k > 0 and ind_l > 0:
            circle = Circle(point_a=point_i, point_b=point_j, point_c=point_l)
            return point_k in circle

        return min(ind_l, ind_k) < min(ind_i, ind_j)

    def _point_index(self, point):
        if point == self._down_base_point:
            return -1
        if point == self._top_base_point:
            return -2
        return 1
