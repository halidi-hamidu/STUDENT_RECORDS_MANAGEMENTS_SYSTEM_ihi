from django.forms import ModelForm
from django import forms
from .models import *
# from wtforms.widgets.core import Select, HTMLString, html_params

class CreateStudentForm(ModelForm):
    class Meta:
        model= Student
        fields='__all__'
        widgets={
            'start_date':forms.widgets.SelectDateWidget(empty_label=('Year', 'Month', 'Day')),
            'end_date':forms.widgets.SelectDateWidget(empty_label=('Year', 'Month', 'Day')),
            'dob':forms.widgets.SelectDateWidget(empty_label=('Year', 'Month', 'Day')),
        }


class CreateCourseForm(ModelForm):
    class Meta:
        model = Course
        fields = "__all__"

# class CreateModuleForm(ModelForm):
#     class Meta:
#         model = Module
#         fields = "__all__"

class AddCollegeForm(ModelForm):
    class Meta:
        model = College
        fields = "__all__"
