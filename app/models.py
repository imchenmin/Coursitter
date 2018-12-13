from django.db import models

# Create your models here.
# 原型类<<<-----------------------------------------------------------------


class Teachers(models.Model):

    tid = models.IntegerField(unique=True, primary_key=True)
    name = models.CharField(max_length=30)
    department = models.CharField(max_length=50)
    # created_date = models.DateTimeField()


class Departments(models.Model):

    name = models.CharField(max_length=20,unique=True,primary_key=True)
    # created_date = models.DateTimeField()


# 创建学生类
class Students(models.Model):

    sid = models.IntegerField(unique=True,primary_key=True)
    name = models.CharField(max_length=20)
    email = models.EmailField()
    # department
    department = models.ForeignKey(Departments,on_delete=models.CASCADE)
    # password
    password  = models.CharField(max_length=30)
    # created_date = models.DateTimeField()


# 课程类别
class ClassType(models.Model):
    name = models.CharField(max_length=20,unique=True)
    description = models.CharField(max_length=100)
    # created_date = models.DateTimeField()


class CourseStatus(models.Model):

    status = models.CharField(max_length=20)
    description = models.CharField(max_length=100)


# 具体课程类
class Courses(models.Model):

    uuid = models.UUIDField()
    course_code = models.CharField(max_length=10,unique=True)
    courseStatus = models.ForeignKey(CourseStatus, on_delete=models.CASCADE)
    # created_date = models.DateTimeField()


class Terms(models.Model):
    uuid = models.UUIDField()
    term_string = models.CharField(max_length=20,unique=True)
    begin_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=10)
    # created_date = models.DateTimeField()


class TermStatus(models.Model):
    pass


# 课程类,不是实际上课时的。是可以复用的，
class Classes(models.Model):
    class_id = models.CharField(max_length=10,unique=True)
    term = models.ForeignKey(Terms,on_delete=models.CASCADE)
    capacity = models.IntegerField()
    status = models.CharField(max_length=10)
    # created_date = models.DateTimeField()
