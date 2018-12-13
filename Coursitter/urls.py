"""Coursitter URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app import  views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/<str:username>/<str:code>',views.auth_view),
    path('course/',views.get_all_course),
    path('course/query/<int:course_id>',views.get_course_info),
    path('course/del/<int:course_id>',views.del_course),
    path('course/add/<int:course_id>/<str:name>/<str:name>/<int:score>/<str:introduction>/<str:prerequistied>',views.add_course),
    path('course/class/',views.get_all_class),
    path('course/class/query/<int:course_id>',views.get_all_class),
    path('course/class/del/<int:course_id>',views.del_class),
    path('course/class/add/<str:id>/<int:capacity>/<str:status>/<int:term_id>/<int:course_id>',views.add_class),
]
