import time

from delaunay.delaunay_lib.geometry.point import Point
from delaunay.delaunay_lib.delone.triangulator import Triangulator


points = []
with open("input.txt", "r") as file:
    for line in file:
        coords = [float(x) for x in line.split()]
        point = Point(coords[0], coords[1])
        points.append(point)

triangulation = Triangulator(points)
start = time.time()
triangulation.make_triangulation()
end = time.time()
print("Time:", end - start)