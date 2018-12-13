from django.shortcuts import render, HttpResponse, redirect
from django.views.decorators.http import require_http_methods
from django.core import serializers
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
import json
import app.models


def auth_view(request):
    username = request.POST.GET("username")
    password = request.POST.GET("password")

    user = authenticate(username=username, password=password)

    if user:
        login(request, user)
        return redirect('/index/')
    else:
        return HttpResponse('Wrong password or username')


def get_course_info(course_id):
    # todo return all the information of the target course.
    # the key should contain 'code', 'name','score',introduction','prerequistied'
    response = {}
    try:
        response['code'] = 'dddd'
        response['name'] = 'aaa'
        response['score'] = '1'
        response['introduction'] = 'adasfdasf'
        response['prerequistied'] = ['OOAD','DSA']  #先修课
        pass
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    JsonResponse(response)


def get_all_course():
    # todo return all the course id
    response = {}
    try:
        response['result'] = ['1161', '324']
        pass
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    JsonResponse(response)


def add_course(course_code, name, score, introduction, prerequistied):
    # todo 添加课程。如果失d败抛出异常
    response = {}
    try:
        pass
        response['msg'] = 'success'
        response['error_num'] = '0'
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    JsonResponse(response)


def del_course(course_code):
    # todo delete one course record
    response = {}
    try:
        pass
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    JsonResponse(response)


def get_class_info(class_id):
    # todo 查询所给class的信息
    # 返回的信息包字段包括 class_id,capacity,status,term_id,course_code
    response = {}
    try:
        pass
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    JsonResponse(response)


def get_all_class():
    # todo return the  id list of all the class
    response = {}
    try:
        result = []
        pass
        response['result'] = result
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    JsonResponse(response)


def add_class(class_id,capacity, status, term_id, course_code):
    # todo add a class record
    response = {}
    try:
        pass
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    JsonResponse(response)


def del_class(class_id):
    # todo del a clas record
    response = {}
    try:
        pass
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    JsonResponse(response)
