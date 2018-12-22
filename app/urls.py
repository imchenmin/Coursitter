from django.urls import path,include
from app import views

from django.urls import path

from . import views

urlpatterns = [
    path('searchCourse', views.searchCourseDeal),
    path('seachLableDeal', views.seachLableDeal),
]