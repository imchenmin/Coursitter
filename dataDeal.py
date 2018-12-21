import django.http


import json


from django.http import HttpResponse

#url: /searchCourse
def searchCourseDeal(request):
    # = django.http.request()
    data = json.loads(request.body.decode())
    #data = json.loads(request.body.decode())
    #sesult = function:
    return HttpResponse(json.dumps(result), content_type='application/json')

#url: /searchLable
def seachLableDeal(request):
    data = json.loads(request.body.decode())
    #result = function:
    return HttpResponse(json.dumps(result), content_type='application/json')

#url: /checkClass
def checkClassDeal(request):
    tmp = json.loads(request.body.decode())
    data = [tmp['sid'], tmp['causeId']]
    #result = function:
    return HttpResponse(json.dumps(result), content_type='application/json')

#url: /addClass
def addClassDeal(request):
    tmp = json.loads(request.body.decode())
    studentId = tmp['studentId']
    courses = tmp['courses']
    #result = function(studentId,courses)
    return HttpResponse(json.dumps(result), content_type='application/json')

