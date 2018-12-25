from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
import json
import urllib.parse
# Create your views here.
from app.models import RelCourse, Courses, StuClasstable, Classes, ClassTime, Students, RelStuCtable


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


def searchCourseDeal(request):
    # print(request.get_full_path())
    result = parseURL_simpleSearch(request.get_full_path())
    result = fuzzy_search(result)
    result = parseCourse(result)
    # print(result)
    return HttpResponse(json.dumps(result), content_type='application/json')
    # return HttpResponse(json.dumps(result), content_type='application/json')


# @login_required(login_url='/login')
# url: /searchLable
def seachLableDeal(request):
    # print(request.get_full_path())
    result = parseURL_label(request.get_full_path())
    print(result)
    result = label_search(result)
    # print(result)
    result = parseCourse(result)
    print(result)
    # todo transfer
    return HttpResponse(json.dumps(result), content_type='application/json')


@login_required(login_url='/login')
# url: /checkClass
def checkClassDeal(request):
    sid = request.user.sid
    classid = parseURL_simpleSearch(request.get_full_path())
    print(classid)
    data = [sid, classid]
    bool, strr = check(data)
    result = [bool, strr]
    # todo transfer
    print(result)
    return HttpResponse(json.dumps(result), content_type='application/json')

@login_required(login_url='/login')
# url: /getHistory
def getHistory(request):
    sid = request.user.sid
    result = get_student_all(sid)
    print(result)
    return HttpResponse(json.dumps(result), content_type='application/json')

@login_required(login_url='/login')
# url: /classADD
def addClassDeal(request):
    sid = request.user.sid
    tmp = json.loads(request.body.decode())
    if add_queue(sid, tmp['classnum'], tmp['coin']):
        return HttpResponse(json.dumps('1'), content_type='application/json')
    else:
        return HttpResponse(json.dumps('0'), content_type='application/json')


@login_required(login_url='/login')
# url: /classDELETE
def deleteClassDeal(request):
    sid = request.user.sid
    tmp = json.loads(request.body.decode())
    result = dele_class(sid, tmp['classnum'])
    return HttpResponse(json.dumps(result), content_type='application/json')


def label_search(dic):
    grade_label = dic['Grade']
    grade = RelCourse.objects.none()
    if grade_label:
        for label in grade_label:
            grade = RelCourse.objects.filter(recommandYear=label) | grade
    else:
        grade = RelCourse.objects.all()

    depart = RelCourse.objects.none()
    depart_label = dic['Departments']
    if depart_label:
        for label in depart_label:
            depart = depart | RelCourse.objects.filter(department__name=label)
    else:
        depart = RelCourse.objects.all()
    type = RelCourse.objects.none()
    type_label = dic['CourseType']
    if type_label:
        for label in type_label:
            type = type | RelCourse.objects.filter(courseType__name=label)
    else:
        type = RelCourse.objects.all()
    query_set = grade & depart & type
    temp_result = Classes.objects.none()
    for rel in query_set:
        a = rel.current
        b = Classes.objects.filter(course=rel.current)
        c = Classes.objects.all()
        temp_result = Classes.objects.filter(course=rel.current) | temp_result
    # The previous step find the classes with first three conditions
    time_label = dic['interval']
    time_result = ClassTime.objects.none()
    if time_label:
        for label in time_label:
            time_result = ClassTime.objects.filter(beganInterval__id=label) | ClassTime.objects.filter(
                endInterval__id=label) | time_result
    else:
        time_result = ClassTime.objects.all()

    day_label = dic['day']
    day_result = ClassTime.objects.none()
    if day_label:
        for label in day_label:
            day_result = ClassTime.objects.filter(inweek=label) | day_result
    else:
        day_result = ClassTime.objects.all()
    query_set2 = time_result & day_result
    result1 = set()
    result2 = set()
    for ele in temp_result:
        result1.add(ele.id)
    for ele in query_set2:
        result2.add(ele.classId.id)
    res = set()
    for id in result1.intersection(result2):
        res.add(Classes.objects.get(id=id).course)
    print(res)
    return res


# todo 需要当前学期,
# fuzzy_search 需course_code 模糊查询。
def fuzzy_search(con):
    try:
        result = Courses.objects.filter(
            Q(classes__teacher__name__contains=con) | Q(classes__course__course_name__contains=con) | Q(
                course_code__contains=con))
        return result
    except Exception as e:
        print(e)
        return None


def check(data):
    print(data)
    try:
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
        if len(re) == 1 and Courses.objects.get(id=re.pop()).course_name == 'null':
            return 1, 'Success'
        else:
            s = 'You need to study the following courses: '
            for ele in re:
                c = Courses.objects.get(id=ele)
                if c.course_name == 'null':
                    continue
                s = s + c.course_name + ', '
            return 0, s
    except Exception as e:
        return 0, e


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
                classinfo = classinfo + "周{} {}-{}".format(k.inweek, k.beganInterval.id, k.endInterval.id)
                period.append(k.inweek)
                period.append(int(k.beganInterval.id / 2 + 1))
            # print(classinfo)
            classlist.append({'classnum': j.id, 'teachers': j.teacher.name, 'classinfo': classinfo, 'period': period})
        # print(classlist)
        courselist.append({'courseID': i.course_code, 'courseName': i.course_name, 'note': i.des, 'credit': i.grade,
                           'classes': classlist})
    result['result'] = courselist
    # print(result)
    return result


def add_queue(student_id, c_id, coin):
    ju = StuClasstable.objects.filter(studentobj_id=student_id, classobj_id=c_id)
    if ju:
        judge = None
        for ele in ju:
            judge = ele
        deta = coin - judge.coin
        total = used_coin(student_id) + deta
        if total < 100:
            judge.coin = coin
            judge.save()
            return True
        else:
            return False
    else:
        try:
            sta = RelStuCtable.objects.get(status='waiting')
            # na = StuClasstable(studentobj=student, classobj_id=classobj, coin=coin, status=sta)
            StuClasstable.objects.create(studentobj_id=student_id, classobj_id=c_id, coin=coin, status_id=sta.id)
            # na.save()
            # StuClasstable.objects.create()
            return True
        except Exception as e:
            print(e)
            return False


def used_coin(student_id):
    try:
        c = 0
        re = StuClasstable.objects.filter(studentobj_id=student_id)
        for ele in re:
            c += ele.coin
    except Exception as e:
        print(e)
    return c


def dele_class(student_id, class_id):
    try:
        ele = StuClasstable.objects.get(studentobj_id=student_id, classobj_id=class_id)
        ele.status = RelStuCtable.objects.get(status='cancel')
        ele.save()
        return 1
    except Exception as e:
        print(e)
        return 0


def write_result():
    try:
        c = Classes.objects.all()
        for ele in c:
            cap = ele.capacity
            ta = StuClasstable.objects.filter(classobj_id=ele.id).order_by('-coin')
            re_num = ta.count()
            count = 0
            for re in ta:
                if count < cap:
                    re.status = RelStuCtable.objects.get(status='selected')
                else:
                    re.status = RelStuCtable.objects.get(status='unselected')
                re.save()
                count += 1

        return True
    except Exception as e:
        print(e)
        return False


def allCourse(request):
    # queryset = Courses.objects.filter(classes__term__status="prepare")
    queryset = Courses.objects.all()
    result = parseCourse(queryset)
    # print(result)
    return JsonResponse(result)


def get_student_all(student_id):
    try:
        qs = StuClasstable.objects.filter(studentobj_id=student_id,
                                          status__status='waiting') | StuClasstable.objects.filter(
            studentobj_id=student_id, status__status='selected')
        result = []
        for ele in qs:
            result.append((ele.classobj_id, ele.coin))
        return parse_selected_course(result)
    except Exception as e:
        print(e)
        return []


def parse_selected_course(query_set):
    cour = []
    # {courseid: {coin: 123, classnum: 100}, ...}
    for ele in query_set:
        s = str(Classes.objects.get(id=ele[0]).course.course_code) + ' :{coin: ' + str(ele[1]) + ', classsnum:' + str(
            ele[0]) + '}'
        cour.append(s)
    result = ''
    if len(cour) == 1:
        result = '{' + s[0] + '}'
    else:
        for i in range(len(cour)):
            if i == 0:
                result += '{' + cour[i] + ','
            elif i == len(cour) - 1:
                result += cour[i] + '}'
            else:
                result += cour[i] + ','
    return result

def parseURL(url):
    url = urllib.parse.unquote(url)
    for i in range(len(url)):
        if url[i] == "?":
            url = url[i + 1:]
            break
    result = {}
    tmp = url.split("[]")
    # print(tmp)
    origin = ''
    for strr in tmp:
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


def parseURL_label(url):
    for i in range(len(url)):
        if url[i] == "?":
            url = url[i + 1:]
            break
    result = {"Grade": [], "Departments": [], "CourseType": [], "interval": [], "day": []}
    tmp = url.split("%5B%5D")
    origin = ''
    for strr in tmp:
        origin += strr
    tmp = origin.split("&")
    for strr in tmp:
        key_value = strr.split("=")
        result[key_value[0]].append(urllib.parse.unquote(key_value[1]))
    return result


# design for simpleSearch
# input: str/fullURL
# output: str
def parseURL_simpleSearch(url):
    url = urllib.parse.unquote(url)
    for i in range(len(url)):
        if url[i] == "?":
            url = url[i + 1:]
            break
    result = url
    return result
