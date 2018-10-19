from django.db import models

# Create your models here.

class Teacher(models.Model):

    tid = models.IntegerField(unique=True)
    name = models.CharField(max_length=30)
    department = models.CharField(max_length=50)

class Department(models.Model):

    name = models.CharField(max_length=20,unique=True)

# 创建学生类
class Student(models.Model):

    sid = models.IntegerField(unique=True)
    name = models.CharField(max_length=20)
    email = models.EmailField()
    # department
    department = models.ForeignKey(Department,on_delete=models.CASCADE,)
    # password
    password  = models.CharField(max_length=30)

# 课程类别
class CourseType(models.Model):

    name = models.CharField(max_length=20,unique=True)


# 课程类,不是实际上课时的。是可以复用的，
class Course(models.Model):

    cid = models.CharField(max_length=10,unique=True)
    coursetype = models.ForeignKey(CourseType,on_delete=models.CASCADE,)