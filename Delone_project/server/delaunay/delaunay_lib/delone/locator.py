from delaunay.delaunay_lib.geometry.point import Point


class Node(object):

    _count = 0

    def __init__(self, triangle):
        self._number = Node._count
        self._triangle = triangle
        self._children = []
        Node._count += 1

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

    def add_link(self, other_node):
        self._children.append(other_node)

    def is_leaf(self):
        return len(self.children) == 0

    def __contains__(self, item):
        if isinstance(item, Point):
            return item in self._triangle

    def __str__(self):
        return f"{{\"type\": \"Node\", \"number\": \"{self._number}\", \"triangle\": {self._triangle}}}"


class LocationTree(object):

    def __init__(self, base_triangle):
        self._root = Node(base_triangle)
        self._leaves = [
            [base_triangle, self._root]
        ]

    @property
    def root(self):
        return self._root

    @property
    def leaves(self):
        res = []
        for row in self._leaves:
            if len(row[1].children) == 0:
                res.append(row[0])
        return res

    def point_location(self, point):
        start_node = self._root

        while not start_node.is_leaf():
            for child in start_node.children:
                if point in child:
                    start_node = child
                    break
        return start_node.triangle

    def add_triangle_children(self, triangle, children_triangle):
        leaf = self._find_leaf(triangle)
        base_node = leaf
        leaves = []
        for child in children_triangle:
            child_node = self._find_leaf(child)
            if child_node:
                leaf.add_link(child_node)
            else:
                child_node = leaf.append(child)
            leaves.append(child_node)
            self._leaves.append([child, child_node])

        return {"base_node": base_node, "leaves": leaves}

    def clear_leaf(self, triangle):
        leaf = self._find_leaf(triangle.number)
        del self._leaves[leaf.triangle]

    def _find_leaf(self, triangle):
        for row in self._leaves:
            leaf_triangle = row[0]
            if triangle == leaf_triangle and len(row[1].children) == 0:
                return row[1]
