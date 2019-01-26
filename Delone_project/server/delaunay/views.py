import json

from delaunay.delaunay_lib.delone.triangulator import Triangulator
from delaunay.delaunay_lib.geometry.point import Point

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.status import HTTP_200_OK


@api_view(['GET'])
def create_triangulation(request):
    points_json = request.GET.get("points")
    points = json.loads(points_json)

    if len(points) == 0:
        return Response(data={}, status=HTTP_200_OK)

    delaunay_points = []
    for point in points:
        delaunay_points.append(Point(float(point['x']), float(point['y'])))

    triangulator = Triangulator(delaunay_points)
    triangulator.make_triangulation()
    events = triangulator.get_events_json()
    return Response(data=events, status=HTTP_200_OK)
