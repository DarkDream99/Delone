import copy

from geometry.point import Point


class Node(object):

    def __init__(self, triangle):
        self._triangle = triangle
        self._children = []

    @property
    def triangle(self):
        return self._triangle

    @property
    def children(self):
        return self._children

    def append(self, triangle):
        leaf = Node(triangle)
        self._children.append(leaf)
        return leaf

    def is_leaf(self):
        return len(self.children) == 0

    def __contains__(self, item):
        if isinstance(item, Point):
            return item in self._triangle


class LocationTree(object):

    def __init__(self, base_triangle):
        self._root = Node(base_triangle)
        self._leaves = {base_triangle: self._root}

    @property
    def leaves(self):
        return [copy.deepcopy(triangle) for triangle in self._leaves]

    def point_location(self, point):
        start_node = self._root

        while not start_node.is_leaf():
            for child in start_node.children:
                if point in child:
                    start_node = child
                    break
        return copy.deepcopy(start_node.triangle)

    def add_triangle_children(self, triangle, children_triangle):
        leaf = self._find_leaf(triangle.number)
        for child in children_triangle:
            child_node = leaf.append(child)
            self._leaves[child] = child_node

    def clear_leaf(self, triangle):
        leaf = self._find_leaf(triangle.number)
        del self._leaves[leaf.triangle]

    def _find_leaf(self, number):
        for triangle in self._leaves:
            if triangle.number == number:
                return self._leaves[triangle]
