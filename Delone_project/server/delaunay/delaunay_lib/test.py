import time
import random
import numpy as np

from urllib.request import urlopen

from delaunay.delaunay_lib.geometry.point import Point
from delaunay.delaunay_lib.delone.triangulator import Triangulator


f = urlopen('https://stepic.org/media/attachments/lesson/16462/boston_houses.csv')
data_table = np.loadtxt(f, skiprows=1, delimiter=',')
means = data_table.mean(axis=0)
print(means)

print(data_table)


# points = []
# with open("input.txt", "r") as file:
#     for line in file:
#         coords = [float(x) for x in line.split()]
#         point = Point(coords[0], coords[1])
#         points.append(point)
#
# triangulation = Triangulator(points)
# start = time.time()
# triangulation.make_triangulation()
# end = time.time()
# print("Time:", end - start)

# with open("out.txt", "w+") as file:
#     for i in range(1100):
#         x = random.randint(-2000, 2000)
#         y = random.randint(-2000, 2000)
#         file.write(f"{x} {y}\n")
