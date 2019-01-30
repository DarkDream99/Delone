import time
import random
import numpy as np

from urllib.request import urlopen

from delaunay.delaunay_lib.geometry.point import Point
from delaunay.delaunay_lib.delone.triangulator import Triangulator


fname = "https://stepic.org/media/attachments/lesson/16462/boston_houses.csv"  # read file name from stdin
f = urlopen(fname)  # open file from URL
data = np.loadtxt(f, delimiter=',', skiprows=1)  # load data to work with

matrix_x = np.ones_like(data)
matrix_x[:, 1:] = np.copy(data)[:, 1:]

matrix_y = np.copy(data)[:, :1]
res_coeff = np.linalg.inv(matrix_x.T @ matrix_x) @ matrix_x.T @ matrix_y
print(" ".join(str(x[0]) for x in res_coeff))

print(data)
print()
print(matrix_x)
print()
print(res_coeff)


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
