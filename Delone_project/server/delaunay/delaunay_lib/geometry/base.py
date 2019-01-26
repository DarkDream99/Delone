import random

from functools import cmp_to_key

from .point import Point


random.seed(120)


def vector_product(point_a, point_b):
    return point_a.x * point_b.y - point_b.x * point_a.y


BASE_POINT = Point(0, 0)


def left_turn(point_a, point_b):
    vec_base_a = point_a - BASE_POINT
    vec_base_b = point_b - BASE_POINT

    vec_prod = vector_product(vec_base_a, vec_base_b)
    if vec_prod > 0:
        return 1
    elif vec_prod < 0:
        return -1
    return 0


def lexicographical_comparator(point_a, point_b):
    if Point.higher(point_a, point_b):
        return 1
    else:
        return -1


def ccw_comparator(point_a, point_b):
    return -1 * left_turn(point_a, point_b)


def cw_comparator(point_a, point_b):
    return left_turn(point_a, point_b)


def sort_point(points, comparator):
    points.sort(key=cmp_to_key(comparator))
    return points


def permutation(points):
    for step in range(100):
        i = random.randint(0, len(points) - 1)
        j = random.randint(0, len(points) - 1)
        points[i], points[j] = points[j], points[i]

    return points
