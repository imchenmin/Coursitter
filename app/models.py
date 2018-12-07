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
class CourseType(models.Model):

    uuid = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=20,unique=True)
    # created_date = models.DateTimeField()


# 课程类,不是实际上课时的。是可以复用的，
class Courses(models.Model):

    uuid = models.UUIDField()
    course_code = models.CharField(max_length=10,unique=True)
    coursetype = models.ForeignKey(CourseType,on_delete=models.CASCADE)
    status = models.CharField(max_length=10)
    # created_date = models.DateTimeField()


class Terms(models.Model):
    uuid = models.UUIDField()
    term_string = models.CharField(max_length=20,unique=True)
    begin_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=10)
    # created_date = models.DateTimeField()


class Classes(models.Model):
    uuid = models.UUIDField()
    coupirse = models.ForeignKey(Courses,on_delete=models.CASCADE)
    class_begin = models.DateTimeField()
    class_end = models.DateTimeField()
    term = models.ForeignKey(Terms,on_delete=models.CASCADE)
    capacity = models.IntegerField()
    status = models.CharField(max_length=10)
    # created_date = models.DateTimeField()

    # 课程和老师的关系是一对多
# 原型类>>>-----------------------------------------------------------------

# 关系类<<<-----------------------------------------------------------------
class ClassTeacher_rel(models.Model):
    uuid = models.UUIDField()
    teacher_id = models.ForeignKey(Teachers,on_delete=models.CASCADE)
    classid = models.ForeignKey(Classes,on_delete=models.CASCADE)
    status = models.CharField(max_length=10)
    # created_date = models.DateTimeField()

class ClassStudent_rel(models.Model):
    uuid = models.UUIDField()
    student = models.ForeignKey(Students,on_delete=models.CASCADE)
    classid = models.ForeignKey(Classes,on_delete=models.CASCADE)
    status = models.CharField(max_length=10)
    # created_date = models.DateTimeField()
# 关系类>>>-----------------------------------------------------------------