from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
import json


# Create your views here.
from app.models import RelCourse, Courses, StuClasstable, Classes, ClassTime


def login_view(request):
    if request.method == 'GET':
        return render(request,'user_login.html')

    else:
        username = request.POST['username']
        password = request.POST['password']
        print('logininginging')
        # authenticate()
        user = authenticate(request, sid=int(username), password=password)
        print(user)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            return HttpResponseRedirect('/')

            # ...
        else:
            # Return an 'invalid login' error message.
            # ...
            print('abbbbb')


#需要logout表单
def logout_view(request):
    logout(request)
    return render(request,"user_login.html")
    # Redirect to a success page.


@login_required(login_url='/login')
def userMain(request):
    return render(request, "user_main.html")


@login_required(login_url='/login')
#url: /searchCourse
def searchCourseDeal(request):
    data = request.GET['q']
    result = fuzzy_search(data)
    # result = 'adfs'
    #todo transfer
    return HttpResponse(result)
    # return HttpResponse(json.dumps(result), content_type='application/json')

# @login_required(login_url='/login')
#url: /searchLable
def seachLableDeal(request):
    data = json.loads(request.body.decode())
    result = label_search(data)
    # todo transfer
    return HttpResponse(json.dumps(result), content_type='application/json')

@login_required(login_url='/login')
#url: /checkClass
def checkClassDeal(request):
    tmp = json.loads(request.body.decode())
    data = [tmp['sid'], tmp['causeId']]
    result = check(data)
    # todo transfer
    return HttpResponse(json.dumps(result), content_type='application/json')

@login_required(login_url='/login')
#url: /addClass
def addClassDeal(request):
    tmp = json.loads(request.body.decode())
    studentId = tmp['studentId']
    courses = tmp['courses']
    result = add_queue(studentId,courses)
    return HttpResponse(json.dumps(result), content_type='application/json')


# @login_required(login_url='/login')
def label_search(dic):
    grade_label = dic['Grade']
    grade = None
    for label in grade:
        grade = RelCourse.objects.filter(recommandYear=label) | grade
    depart = None
    depart_label = dic['Departments']
    for label in depart_label:
        depart = depart | RelCourse.objects.filter(department__name=label)

    type = None
    type_label = dic['CourseType']
    for label in type_label:
        type = type | RelCourse.objects.filter(courseType__name=label)
    query_set = grade & depart & type
    temp_result = None
    for rel in query_set:
        temp_result = Classes.objects.filter(course=rel.current) | temp_result
    # The previous step find the classes with first three conditions

    time_label = dic['interval']
    time_result = None
    for label in time_label:
        time_result = ClassTime.objects.filter(beganInterval__id=label) | ClassTime.objects.filter(endInterval__id=label) | time_result
    day_label = dic['day']
    day_result = None
    for label in day_label:
        day_result = ClassTime.objects.filter(inweek=label) | day_result
    query_set2 = time_result & day_result
    query_set3= None
    for ele in query_set2:
        t1 = ele.Class_set.all()
    result = temp_result & query_set2.values("classID")
    return result


#todo 需要当前学期,
# fuzzy_search 需course_code 模糊查询。
def fuzzy_search(con):
    result = Classes.objects.filter(
        Q(teacher__name__contains=con) | Q(course__course_name__contains=con) | Q(location__contains=con))
    return result


@login_required(login_url='/login')
def check(student_id,course_code):
    '''
    :param student_id:
    :param course_code:
    :return:
    '''
    studied_classes = StuClasstable.objects.filter(status__status='completed',studentobj__sid=student_id).values('classobj')
    student_course = Courses.objects.filter(course_code)
    needed = RelCourse.objects.filter(current__course_code=course_code)


def add_queue(student_id, course):
    pass













