from django.db import models

# Create your models here.
# 原型类<<<-----------------------------------------------------------------

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
    department = models.ForeignKey(Department,on_delete=models.CASCADE)
    # password
    password  = models.CharField(max_length=30)

# 课程类别
class CourseType(models.Model):

    name = models.CharField(max_length=20,unique=True)

# 课程类,不是实际上课时的。是可以复用的，
class Courses(models.Model):

    course_id = models.CharField(max_length=10,unique=True)
    coursetype = models.ForeignKey(CourseType,on_delete=models.CASCADE)

class Terms(models.Model):
    term_id = models.CharField(max_length=15,unique=True)
    begin_date = models.DateField()
    end_date = models.DateField()

class Classes(models.Model):
    class_id = models.IntegerField()
    course = models.ForeignKey(Courses)
    class_begin = models.DateTimeField()
    class_end = models.DateTimeField()
    term = models.ForeignKey(Terms)
    capacity = models.IntegerField()
    # 课程和老师的关系是一对多
# 原型类>>>-----------------------------------------------------------------

# 关系类<<<-----------------------------------------------------------------
# class ClassAndTeacher(models.Model):
# class ClassAndStudent(models.Model):
