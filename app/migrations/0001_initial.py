# Generated by Django 2.1.2 on 2018-12-21 13:08

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Classes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('capacity', models.IntegerField()),
                ('location', models.CharField(default='none', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='ClassStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=20)),
                ('des', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ClassTime',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('beganWeek', models.IntegerField()),
                ('endWeek', models.IntegerField()),
                ('inweek', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Courses',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_code', models.CharField(max_length=10, unique=True)),
                ('course_name', models.CharField(default='abc', max_length=30)),
                ('des', models.TextField(null=True)),
                ('grade', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='CourseType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True)),
                ('des', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Departments',
            fields=[
                ('name', models.CharField(max_length=20, primary_key=True, serialize=False, unique=True)),
                ('des', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='RelCourse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recommandYear', models.CharField(default='freshman', max_length=20)),
                ('courseType', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='courseType', to='app.CourseType')),
                ('current', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='current', to='app.Courses')),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Departments')),
                ('prerequisites', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prerequisites', to='app.Courses')),
            ],
        ),
        migrations.CreateModel(
            name='RelStuCtable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=20)),
                ('des', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='StuClasstable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coin', models.IntegerField(blank=True)),
                ('classobj', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Classes')),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.RelStuCtable')),
            ],
        ),
        migrations.CreateModel(
            name='Students',
            fields=[
                ('sid', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
                ('password', models.CharField(max_length=30)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Departments')),
            ],
        ),
        migrations.CreateModel(
            name='Teachers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
                ('des', models.TextField(null=True)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Departments')),
            ],
        ),
        migrations.CreateModel(
            name='Terms',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True)),
                ('begin_date', models.DateField()),
                ('end_date', models.DateField()),
                ('status', models.CharField(max_length=10)),
                ('begin_selected', models.DateTimeField(default=datetime.datetime(2018, 12, 21, 13, 8, 47, 584689, tzinfo=utc))),
                ('end_selected', models.DateTimeField(default=datetime.datetime(2018, 12, 21, 13, 8, 47, 584751, tzinfo=utc))),
                ('end_modify', models.DateTimeField(default=datetime.datetime(2018, 12, 21, 13, 8, 47, 584797, tzinfo=utc))),
            ],
        ),
        migrations.CreateModel(
            name='TimeType',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('timeStamp', models.CharField(max_length=20)),
                ('timeInterval', models.IntegerField(default=50)),
            ],
        ),
        migrations.AddField(
            model_name='stuclasstable',
            name='studentobj',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Students'),
        ),
        migrations.AddField(
            model_name='classtime',
            name='beganInterval',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='beganInterval', to='app.TimeType'),
        ),
        migrations.AddField(
            model_name='classtime',
            name='classId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Classes'),
        ),
        migrations.AddField(
            model_name='classtime',
            name='endInterval',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='endInterval', to='app.TimeType'),
        ),
        migrations.AddField(
            model_name='classes',
            name='course',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.Courses'),
        ),
        migrations.AddField(
            model_name='classes',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.ClassStatus'),
        ),
        migrations.AddField(
            model_name='classes',
            name='teacher',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='app.Teachers'),
        ),
        migrations.AddField(
            model_name='classes',
            name='term',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Terms'),
        ),
    ]
