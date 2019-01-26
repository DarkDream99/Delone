import random
import time

from geometry.point import Point
from delone.triangulator import Triangulator


points = []
for i in range(100):
    x = random.randint(0, 20)
    y = random.randint(0, 20)
    points.append(Point(x, y))

triangulator = Triangulator(points)
start = time.time()
triangulator.make_triangulation()
end = time.time()
print(end - start)
events = triangulator.get_events_json()
print(events)
