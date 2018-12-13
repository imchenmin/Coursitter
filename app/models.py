from django.db import models

# Create your models here.
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
class Students(models.Model):

    sid = models.IntegerField(unique=True,primary_key=True)
    name = models.CharField(max_length=20)
    email = models.EmailField()
    # department
    department = models.ForeignKey(Departments,on_delete=models.CASCADE)
    # password
    password  = models.CharField(max_length=30)
    # created_date = models.DateTimeField()

    def __str__(self):
        return '{}  {}'.format(self.sid,self.name)


class Terms(models.Model):
    name = models.CharField(max_length=20,unique=True)
    begin_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=10)
    # created_date = models.DateTimeField()

    def __str__(self):
        return self.name


# 课程类别
class CourseType(models.Model):
    name = models.CharField(max_length=20,unique=True)
    des = models.TextField(null=True)    # created_date = models.DateTimeField()

    def __str__(self):
        return self.name


# 具体课程类
class Courses(models.Model):
    course_code = models.CharField(max_length=10,unique=True)
    des = models.TextField(null=True)
    # created_date = models.DateTimeField()

    def __str__(self):
        return self.course_code


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

    def __str__(self):
        return self.course.course_code


class RelStuCtable(models.Model):
    status = models.CharField(max_length=20)
    des = models.TextField(null=True)
    def __str__(self):
        return self.status


# 总的课程表，包括预选课
class StuCtable(models.Model):
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

    def __str__(self):
        return "{}->{} for {}".format(self.prerequisites.course_code,self.current.course_code,self.department)