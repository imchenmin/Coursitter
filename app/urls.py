from django.urls import path, include
from app import views

from django.urls import path

from . import views

urlpatterns = [
    path('searchCourse/', views.searchCourseDeal),
    path('searchLabel/', views.seachLableDeal),
    path('allCourse/', views.allCourse),
    path('classADD/', views.addClassDeal),
    path('classDELETE/', views.deleteClassDeal),
    path('checkClass/', views.checkClassDeal)
    # path
]
