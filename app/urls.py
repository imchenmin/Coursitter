from django.urls import path,include
from app import views

from django.urls import path

from . import views

urlpatterns = [
    path('class', views.searchCourseDeal),
    path('label', views.seachLableDeal),
    # path('allClass', )
    # path('mycart',) //get  post
    path('allCourse',views.allCourse)
    # path
]