from django.urls import path, include, re_path

from . import views


urlpatterns = [
    re_path(r'^triangulation/', views.create_triangulation)
]
