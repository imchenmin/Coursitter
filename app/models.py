import json
from json import JSONEncoder

from django.db import models
from  django.utils import timezone
from django.contrib.auth.models import AbstractUser


# 原型类<<<-----------------------------------------------------------------


class Departments(models.Model):
    name = models.CharField(max_length=20,unique=True,primary_key=True)
    des = models.TextField(null=True)
    def __str__(self):
        return self.name


class Teachers(models.Model):

    name = models.CharField(max_length=40)
    department = models.ForeignKey(Departments,on_delete=models.CASCADE)
    des = models.TextField(null=True)
    # created_date = models.DateTimeField()

    def __str__(self):
        return '{}  {}  {}'.format(self.name,self.id,self.department)


# 创建学生类
class Students(AbstractUser):
    sid = models.IntegerField(unique=True,primary_key=True)
    username = models.CharField(max_length=20)
    email = models.EmailField()
    # department
    # department = models.ForeignKey(Departments,on_delete=models.CASCADE,default=0)
    # password
    # password  = models.CharField(max_length=30)
    # created_date = models.DateTimeField()

    USERNAME_FIELD = 'sid'
    REQUIRED_FIELDS = ['username','email']
    def __str__(self):
        return '{}  {}'.format(self.sid,self.username)


class Terms(models.Model):
    name = models.CharField(max_length=20,unique=True)
    begin_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=10)
    begin_selected = models.DateTimeField(default=timezone.now())
    end_selected = models.DateTimeField(default=timezone.now())
    end_modify = models.DateTimeField(default=timezone.now())
    # created_date = models.DateTimeField()

    def __str__(self):
        return self.name


# 课程类别，属于培养方案
class CourseType(models.Model):
    name = models.CharField(max_length=20,unique=True)
    des = models.TextField(null=True)    # created_date = models.DateTimeField()

    def __str__(self):
        return self.name


# 具体课程类
class Courses(models.Model):
    course_code = models.CharField(max_length=10,unique=True)
    course_name = models.CharField(max_length=30, default='abc')
    des = models.TextField(null=True)
    grade = models.IntegerField(default=0)
    # created_date = models.DateTimeField()

    def __str__(self):
        return self.course_code + '' + str(self.grade)


class ClassStatus(models.Model):

    status = models.CharField(max_length=20)
    des = models.TextField(null=True)

    def __str__(self):
        return self.status


# 是实际上课时的
class Classes(models.Model):
    term = models.ForeignKey(Terms,on_delete=models.CASCADE)
    course = models.ForeignKey(Courses,on_delete=models.CASCADE,null=True)
    capacity = models.IntegerField()
    status = models.ForeignKey(ClassStatus,on_delete=models.CASCADE)
    # created_date = models.DateTimeField()
    teacher = models.ForeignKey(Teachers, on_delete=models.CASCADE,default=1)
    location = models.CharField(max_length=50, default="none")

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

    def __str__(self):
        return 'course {} class {}'.format(self.course.course_code, self.id)


# 第一节，第二节。。。。。具体在一天的什么时间。方便冬夏换课时。
class TimeType(models.Model):
    id = models.IntegerField(primary_key=True)
    timeStamp = models.CharField(max_length=20)
    timeInterval = models.IntegerField(default=50)    #in minutes

    def __str__(self):
        return "{} {}".format(self.id,self.timeStamp)


class ClassTime(models.Model):
    classId = models.ForeignKey(Classes,on_delete=models.CASCADE)
    beganWeek = models.IntegerField()
    endWeek = models.IntegerField()
    inweek = models.IntegerField()
    beganInterval = models.ForeignKey(TimeType, on_delete=models.CASCADE,related_name='beganInterval')
    endInterval = models.ForeignKey(TimeType, on_delete=models.CASCADE,related_name='endInterval')

    def __str__(self):
        return '{} week:{} - {} from  {} to {}+{}minutes in  {}'.format(self.classId,self.beganWeek,self.endWeek,self.beganInterval,self.endInterval,self.endInterval.timeInterval,self.inweek)


# 学生的选课状态
class RelStuCtable(models.Model):
    status = models.CharField(max_length=20)
    des = models.TextField(null=True)

    def __str__(self):
        return self.status+self.des


# 总的课程表，包括预选课
class StuClasstable(models.Model):
    studentobj = models.ForeignKey(Students,on_delete=models.CASCADE)
    classobj = models.ForeignKey(Classes, on_delete=models.CASCADE)
    coin = models.IntegerField(blank=True)
    status = models.ForeignKey(RelStuCtable,on_delete=models.CASCADE)

    def __str__(self):
        return "{}{}. class {}".format(self.studentobj.name,self.studentobj.sid,self.classobj.course.course_code, self.classobj.course.course_code)


class RelCourse(models.Model):
    current = models.ForeignKey(Courses,on_delete=models.CASCADE,related_name='current')
    prerequisites = models.ForeignKey(Courses, on_delete=models.CASCADE,related_name='prerequisites')
    department = models.ForeignKey(Departments, on_delete=models.CASCADE)
    courseType = models.ForeignKey(CourseType, on_delete=models.CASCADE,related_name='courseType',default=1)
    recommandYear = models.CharField(max_length=20, default="freshman")

    def __str__(self):
        return "{}->{} for {}. Is type:{}".format(self.prerequisites.course_code,self.current.course_code,self.department,self.courseType.name)