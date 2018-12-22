from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
import json
import urllib.parse
# Create your views here.
from app.models import RelCourse, Courses, StuClasstable, Classes, ClassTime, Students, RelStuCtable


def parseURL(url):
    url = urllib.parse.unquote(url)
    for i in range(len(url)):
        if url[i] == "?":
            url = url[i+1:]
            break
    result = {}
    tmp = url.split("[]")
    #print(tmp)
    origin = ''
    for strr  in tmp:
        origin += strr
    print(origin)
    tmp = origin.split("&")
    for strr in tmp:
        key_value = strr.split("=")
        if key_value[0] not in result.keys():
            result[key_value[0]] = [key_value[1]]
        else:
            result[key_value[0]].append(key_value[1])
    return result


#design for simpleSearch
#input: str/fullURL
#output: str
def parseURL_simpleSearch(url):
    url = urllib.parse.unquote(url)
    for i in range(len(url)):
        if url[i] == "?":
            url = url[i+1:]
            break
    result = url
    return result

def login_view(request):
    if request.method == 'GET':
        return render(request, 'user_login.html')

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
            return HttpResponseRedirect('/')


# 需要logout表单
def logout_view(request):
    logout(request)
    return render(request, "user_login.html")
    # Redirect to a success page.


@login_required(login_url='/login')
def userMain(request):
    return render(request, "user_main.html")


@login_required(login_url='/login')
# url: /searchCourse
def searchCourseDeal(request):
    result = parseURL_simpleSearch(request.get_full_path())
    result = fuzzy_search(result)
    result = parseCourse(result)
    return JsonResponse(result)
    # return HttpResponse(json.dumps(result), content_type='application/json')



# @login_required(login_url='/login')
# url: /searchLable
def seachLableDeal(request):
    print(request.get_full_path())
    result = parseURL(request.get_full_path())
    print(result)
    result = label_search(result)
    print(result)
    result = parseCourse(result)
    print(result)

    # todo transfer
    return JsonResponse(result)


@login_required(login_url='/login')
# url: /checkClass
def checkClassDeal(request):
    tmp = json.loads(request.body.decode())
    data = [tmp['sid'], tmp['causeId']]
    result = check(data)
    # todo transfer
    return HttpResponse(json.dumps(result), content_type='application/json')


@login_required(login_url='/login')
# url: /addClass
def addClassDeal(request):
    # tmp = json.loads(request.body.decode())
    # studentId = tmp['studentId']
    # courses = tmp['courses']
    # result = add_queue(1, 1)
    return HttpResponse(json.dumps(result), content_type='application/json')


def label_search(dic):
    # dic ={}
    grade_label = dic.setdefault('Grade', '')
    # grade_label = "大四"
    grade = RelCourse.objects.none()
    # print(grade)
    for label in grade_label:
        # print(label)
        grade = RelCourse.objects.filter(recommandYear=label) | grade
    depart = RelCourse.objects.none()
    depart_label = dic.setdefault('Departments', '')
    for label in depart_label:
        depart = depart | RelCourse.objects.filter(department__name=label)
    type = RelCourse.objects.none()
    type_label = dic.setdefault('CourseType', '')
    for label in type_label:
        type = type | RelCourse.objects.filter(courseType__name=label)
    query_set = grade & depart & type
    temp_result = Classes.objects.none()
    for rel in query_set:
        temp_result = Classes.objects.filter(course=rel.current) | temp_result
    # The previous step find the classes with first three conditions
    time_label = dic.setdefault('interval', '')
    time_result = ClassTime.objects.none()
    for label in time_label:
        time_result = ClassTime.objects.filter(beganInterval__id=label) | ClassTime.objects.filter(
            endInterval__id=label) | time_result
    day_label = dic.setdefault('day', '')
    day_result = ClassTime.objects.none()
    for label in day_label:
        day_result = ClassTime.objects.filter(inweek=label) | day_result
    query_set2 = time_result & day_result
    result1 = set()
    result2 = set()
    for ele in temp_result:
        result1.add(ele.id)
    for ele in query_set2:
        result2.add(ele.id)

    return result1.intersection(result2)


# todo 需要当前学期,
# fuzzy_search 需course_code 模糊查询。
def fuzzy_search(con):
    result = Courses.objects.filter(
        Q(classes__teacher__name__contains=con) | Q(classes__course__course_name__contains=con) | Q(
            course_code__contains=con))
    return result


def check(data):
    student_id = data[0]
    course_code = data[1]
    studied_classes = StuClasstable.objects.filter(status__status='completed', studentobj__sid=student_id)
    c_id = set()
    for ele in studied_classes:
        c_id.add(ele.classobj_id)
    n_id = set()
    needed_course = RelCourse.objects.filter(current__course_code=course_code)
    for ele in needed_course:
        n_id.add(ele.prerequisites_id)
    re = n_id - c_id
    if not re:
        return True,'Success'
    else:
        s = 'You need to study the following courses: '
        for ele in re:
            c = Courses.objects.get(id=ele)
            s=s+c.course_name+', '
        return False,s



# def add_queue(student_id, c_id, coin):
#     judge = StuClasstable.objects.get(studentobj_id=student_id,classobj_id=c_id)
#     if judge:
#         judge.coin=coin
#         judge.save()
#         return True
#     else:
#         try:
#             sta = RelStuCtable.objects.get(status='waiting')
#             # na = StuClasstable(s
#         return False

def parseCourse(queryset):
    result = {}
    result['msg'] = ""
    courselist = []
    for i in queryset:
        classobjs = Classes.objects.filter(course=i)
        classlist = []
        period = []
        for j in classobjs:
            classinfo = ""
            timeobjs = ClassTime.objects.filter(classId=j)
            for k in timeobjs:
                classinfo = classinfo + "周{} {}-{}".format(k.inweek,k.beganInterval.id,k.endInterval.id)
                period.append(k.inweek)
                period.append(int(k.beganInterval.id/2+1))
            # print(classinfo)
            classlist.append({'classID':j.id,'teacher':j.teacher.name,'classinfo':classinfo,'period':period})
        # print(classlist)
        courselist.append({'Course':i.course_code, 'name':i.course_name,'class':classlist})
    result['result']=courselist
    # print(result)
    return result

def allCourse(request):
    queryset = Courses.objects.filter(classes__term__status="prepare")
    result = parseCourse(queryset)
    return JsonResponse(result)
