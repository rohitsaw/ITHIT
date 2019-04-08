from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

#

# Create your models here.
# class Profile(User):
#     user = models.OneToOneField(User, on_delete=models.CASCADE) # username, email , password defined in User model
#     name = models.CharField(max_length=20, null=False, blank=False)
#     isTeacher = models.BooleanField(default=False)
#
#     dept = models.CharField(max_length=20)
#     year = models.CharField(max_length=6)
#     rollno = models.CharField(max_length=20)

class Assignment(models.Model):
    teacher_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="assignments")
    docs = models.FileField(upload_to = 'docs/%Y/%m/%d/')
    header = models.CharField(max_length=64)
    year = models.IntegerField(blank=True,null=True)

    def __str__(self):
        return f"{self.teacher_id}"

class Role(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, primary_key=True)
    isTeacher = models.BooleanField(default=False)

# class Teacher(models.Model):
#     user = models.OneToOneField(User, on_delete = models.CASCADE, primary_key=True)
#     assignments = models.ManyToManyField(Assignment, related_name="teacher")

class Student(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, primary_key=True)
    rollno = models.IntegerField(blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
