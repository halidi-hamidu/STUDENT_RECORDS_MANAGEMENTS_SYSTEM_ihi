from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
import datetime
# Create your models here.
class Profile(models.Model):
    GENDER = [
     ("","select gender"),
     ("Male","Male"),
     ("Male","Female"),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=70, null=True, blank=True)
    lasname = models.CharField(max_length=70, null=True, blank=True)
    email = models.EmailField(max_length=70, null=True, blank=True)
    contact = models.PositiveIntegerField(null=True, blank=True)
    gender = models.CharField(max_length=50, null=True, blank=True, choices=GENDER)
    image = models.ImageField(default="c3.jpg", upload_to='media', blank=True, null=True)

    class Meta:
        verbose_name_plural = "UserProfile"

    def __str__(self):
        return self.user.username

# class Module(models.Model):
#     module_name = models.CharField(max_length=100, null=True, blank=True)
#     module_code = models.CharField(max_length=100, null=True, blank=True)
#     module_credit = models.PositiveSmallIntegerField(null=True, blank=True)

#     class Meta:
#         verbose_name_plural = "modules"

#     def __str__(self):
#         return str(self.module_name)

class Course(models.Model):
    course_name = models.CharField(max_length=100, null=True, blank=True)
    course_code = models.CharField(max_length=100, null=True, blank=True)
    # module = models.ManyToManyField(Module, null=True, blank=True)

    class Meta:
        verbose_name_plural = "courses"

    def __str__(self):
        return str(self.course_name)

class College(models.Model):
    college_name = models.CharField(max_length=100, null=True, blank=True)
    college_location = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        verbose_name_plural = "colleges"

    def __str__(self):
        return str(self.college_name)

class Student(models.Model):
    GENDER = [
     ("","select gender"),
     ("Male","Male"),
     ("Female","Female"),
    ]

    STATUS = [
        ("", "Status"),
     ("continuous","continuous"),
     ("postpone","postpone"),
     ("complete","complete"),
     ("final","final"),
    ]

    EDUCATION_LEVEL = [
     ("","select education level"),
     ("PHD","PHD"),
     ("MASTERS","MASTERS"),
    ]

    image = models.ImageField(default='img_avatar.png',blank=True,upload_to='media')
    firstname = models.CharField(max_length=70, null=True, blank=True)
    middle_name = models.CharField(max_length=70, null=True, blank=True)
    surname = models.CharField(max_length=70, null=True, blank=True)
    email = models.EmailField(max_length=70, null=True, blank=True)
    current_date = datetime.datetime.now()
    dob = models.DateField(null=True, blank=True)
    age =  models.PositiveIntegerField(null=True, blank=True)
    gender = models.CharField(max_length=50, null=True, blank=True, choices=GENDER)
    contact = models.PositiveIntegerField(null=True, blank=True)
    nationality = models.CharField(max_length=70, null=True, blank=True)
    registration_number = models.CharField(max_length=70, null=True, blank=True)
    programme_name = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)
    start_date=models.DateField(null=True, blank=True)
    end_date=models.DateField(null=True, blank=True)
    college = models.ForeignKey(College, on_delete=models.SET_NULL, null=True)
    education_level = models.CharField(max_length=50, null=True, blank=True, choices=EDUCATION_LEVEL)
    student_status = models.CharField(max_length=50, null=True, blank=True, choices=STATUS)

    class Meta:
        verbose_name_plural = "students"

    def __str__(self):
        return str(self.surname)
