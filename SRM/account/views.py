from typing import ContextManager
import csv
from django.http import HttpResponse
from django.http.response import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import messages
from django.views.decorators.cache import cache_control
from django.contrib.auth.models import User
import datetime


# from numpy import generic
from .models import *
from . import forms
from .forms import CreateStudentForm
from .utils import get_graph, get_plot,get_graph_cnt, get_graph_cmp, get_graph_fnl,get_graph_pst,get_graph_phd,get_graph_mst
# Create your views here.

def LoginView(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST or None)
        if form.is_valid():
            getUser = form.get_user()
            login(request,getUser)
            return redirect("dashboard")
        else:
            messages.info(request, 'Enter Valid Data!')
            return redirect('auth')
    else:
        form = AuthenticationForm()
        templates = 'account/login.html'
        context = {
           "forms": form,
        }
        return render(request, templates, context)

@cache_control(no_cache=True, must_revalidate=True, privacy=True, no_store=True)
@login_required(login_url='auth')
def RegisterView(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'account created for {username} !')
            return redirect('register')
        else:
            current_user = request.POST.get('username')
            current_user=str(current_user)
            password1=request.POST.get("password1")
            password2=request.POST.get("password2")
            user = User.objects.filter(username=current_user)
            if password1 != password2:
                messages.info(request, f'Password Mismatch!')
                return redirect('register')
            else:
                messages.info(request, f'User {current_user} Already Exist!')
                return redirect('register')
    else:
        form = UserCreationForm()
        templates = 'account/register.html'
        context = {
           "forms": form,
        }
        return render(request, templates, context)
@cache_control(no_cache=True, must_revalidate=True, privacy=True, no_store=False)
@login_required(login_url='auth')
def LogOutView(request):
    logout(request)
    return redirect('auth')

@cache_control(no_cache=True, must_revalidate=True, privacy=True, no_store=False)
@login_required(login_url='auth')
def DashboardView(request):
    get_all_student = Student.objects.all().order_by('-id')
    count_all_student = Student.objects.all().order_by('-id').count()
    get_all_master_std=Student.objects.filter(education_level="MASTERS").count()
    get_all_master_male_std=Student.objects.filter(education_level="MASTERS", gender="Male").count()
    get_all_master_female_std=Student.objects.filter(education_level="MASTERS", gender="Female").count()
    get_all_phd_std=Student.objects.filter(education_level="PHD").count()
    get_all_phd_male_std=Student.objects.filter(education_level="PHD", gender="Male").count()
    get_all_phd_female_std=Student.objects.filter(education_level="PHD", gender="Female").count()
    get_all_cont_student = Student.objects.filter(student_status='continuous').count()
    get_all_cont_student_male = Student.objects.filter(student_status='continuous',gender='Male').count()
    get_all_cont_student_female = Student.objects.filter(student_status='continuous', gender='Female').count()
    get_all_male_student = Student.objects.filter(gender='Male').count()
    get_all_female_student = Student.objects.filter(gender='Female').count()
    get_all_comp_student = Student.objects.filter(student_status='complete').count()
    get_all_comp_student_male = Student.objects.filter(student_status='complete', gender='Male').count()
    get_all_comp_student_female = Student.objects.filter(student_status='complete', gender='Female').count()
    get_all_post_student = Student.objects.filter(student_status='postpone').count()
    get_all_post_student_male = Student.objects.filter(student_status='postpone', gender='Male').count()
    get_all_post_student_female = Student.objects.filter(student_status='postpone', gender='Female').count()
    get_all_final_student = Student.objects.filter(student_status='final').count()
    get_all_final_student_male = Student.objects.filter(student_status='final', gender='Male').count()
    get_all_final_student_female = Student.objects.filter(student_status='final', gender='Female').count()

    total_students = get_all_cont_student + get_all_comp_student + get_all_post_student + get_all_final_student

    time = datetime.datetime.now()
    get_time = time.strftime("%c")
    templates = 'account/dashboard.html'
    context = {
    "get_time":get_time,
    "get_all_student":get_all_student[:10],
    "count_all_student":count_all_student,
    "get_all_male_student":get_all_male_student,
    "get_all_female_student":get_all_female_student,
    # =======================phd ============================
    "get_all_phd_std":get_all_phd_std,
    "get_all_phd_male_std":get_all_phd_male_std,
    "get_all_phd_female_std":get_all_phd_female_std,
    # ======================masters=============
    "get_all_masters_std":get_all_master_std,
    "get_all_masters_male_std":get_all_master_male_std,
    "get_all_masters_female_std":get_all_master_female_std,


    ######## COMPLETED
    "get_all_comp_student":get_all_comp_student,
    "get_all_comp_student_male":get_all_comp_student_male,
    "get_all_comp_student_female":get_all_comp_student_female,

    ###### CONTINUOUS
    "get_all_cont_student":get_all_cont_student,
    "get_all_cont_student_male":get_all_cont_student_male,
    "get_all_cont_student_female":get_all_cont_student_female,

    ###### POSTPONED
    "get_all_post_student":get_all_post_student,
    "get_all_post_student_male":get_all_post_student_male,
    "get_all_post_student_female":get_all_post_student_female,

    ###### FINALIST
    "get_all_final_student":get_all_final_student,
    "get_all_final_student_male":get_all_final_student_male,
    "get_all_final_student_female":get_all_final_student_female,

    }
    return render(request, templates, context)

@cache_control(no_cache=True, must_revalidate=True, privacy=True, no_store=False)
@login_required(login_url='auth')
def PhdView(request):
    form = CreateStudentForm()
    get_college = College.objects.all().order_by('-id')
    get_all_phd_student = Student.objects.filter(education_level='PHD').order_by('-id')
    count_all_phd = Student.objects.filter(education_level='PHD').count()
    count_all_phd_male = Student.objects.filter(education_level='PHD', gender='Male').count()
    count_all_phd_female = Student.objects.filter(education_level='PHD', gender='Female').count()

    ########## COMPLETED STUDENTS
    count_all_phd_comp = Student.objects.filter(education_level='PHD',student_status='complete').count()
    count_all_phd_comp_male = Student.objects.filter(education_level='PHD', gender='Male', student_status='complete').count()
    count_all_phd_comp_female = Student.objects.filter(education_level='PHD', gender='Female', student_status='complete').count()

    ########## CONTINUOUS STUDENTS NOT WORKING
    count_all_phd_cont = Student.objects.filter(education_level='PHD',student_status='continuous').count()
    count_all_phd_cont_male = Student.objects.filter(education_level='PHD',student_status='continuous', gender='Male').count()
    count_all_phd_cont_female = Student.objects.filter(education_level='PHD',student_status='continuous', gender='Female').count()

    ########## POSTPONED STUDENTS
    count_all_phd_post = Student.objects.filter(education_level='PHD',student_status='postpone').count()
    count_all_phd_post_male = Student.objects.filter(education_level='PHD',student_status='postpone', gender='Male').count()
    count_all_phd_post_female = Student.objects.filter(education_level='PHD',student_status='postpone', gender='Female').count()

    ######### FINALIST s
    count_all_phd_final = Student.objects.filter(education_level='PHD',student_status='final').count()
    count_all_phd_final_male = Student.objects.filter(education_level='PHD',student_status='final', gender='Male').count()
    count_all_phd_final_female = Student.objects.filter(education_level='PHD',student_status='final', gender='Female').count()
    if request.method =="POST":
        male="Male"
        female="Female"
        continuous="continuous"
        postpone="postpone"
        complete="complete"
        final="final"
        form=CreateStudentForm()
        try:
            gender=request.POST.get("gender")
            start_date=request.POST.get("start_date")
            end_date=request.POST.get("end_date")
            status=request.POST.get("student_status")
            ######################### empty  selection retrun all phd std #######################
            if gender =='' and start_date == '' and end_date == '' and status =='':
                get_all_phd_student=Student.objects.filter(education_level="PHD")
                time = datetime.datetime.now()
                get_time = time.strftime("%c")
                templates="account/phd.html"
                context={
                        "get_time":get_time,
                        "get_college":get_college,
                        "get_all_phd_student":get_all_phd_student[:10],
                        "count_all_phd":count_all_phd,
                        "count_all_phd_male":count_all_phd_male,
                        "count_all_phd_female":count_all_phd_female,
                        "count_all_phd_comp":count_all_phd_comp,
                        "count_all_phd_comp_male":count_all_phd_comp_male,
                        "count_all_phd_comp_female":count_all_phd_comp_female,
                        "count_all_phd_cont":count_all_phd_cont,
                        "count_all_phd_cont_male":count_all_phd_cont_male,
                        "count_all_phd_cont_female":count_all_phd_cont_female,
                        "count_all_phd_post":count_all_phd_post,
                        "count_all_phd_post_male":count_all_phd_post_male,
                        "count_all_phd_post_female":count_all_phd_post_female,
                        "count_all_phd_final":count_all_phd_final,
                        "count_all_phd_final_male":count_all_phd_final_male,
                        "count_all_phd_final_female":count_all_phd_final_female,
                        "forms":form
                }
                return render(request, templates, context)
            #######################  single selections #######################
            elif gender and start_date == '' and end_date == '' and status =='':
                if gender =="Male":
                    get_all_phd_student_male=Student.objects.filter(education_level="PHD", gender="Male")
                    templates="account/phd.html"
                    context={
                    "get_all_phd_student_male": get_all_phd_student_male,
                    "count_all_phd":count_all_phd,
                    "count_all_phd_male":count_all_phd_male,
                    "count_all_phd_female":count_all_phd_female,
                    "count_all_phd_comp":count_all_phd_comp,
                    "count_all_phd_comp_male":count_all_phd_comp_male,
                    "count_all_phd_comp_female":count_all_phd_comp_female,
                    "count_all_phd_cont":count_all_phd_cont,
                    "count_all_phd_cont_male":count_all_phd_cont_male,
                    "count_all_phd_cont_female":count_all_phd_cont_female,
                    "count_all_phd_post":count_all_phd_post,
                    "count_all_phd_post_male":count_all_phd_post_male,
                    "count_all_phd_post_female":count_all_phd_post_female,
                    "count_all_phd_final":count_all_phd_final,
                    "count_all_phd_final_male":count_all_phd_final_male,
                    "count_all_phd_final_female":count_all_phd_final_female,
                    "forms":form
                    }
                    return render(request, templates, context)
                else:
                    get_all_phd_student_female=Student.objects.filter(education_level="PHD", gender="Female")
                    templates="account/phd.html"
                    context={
                    "get_all_phd_student_female": get_all_phd_student_female,
                    "count_all_phd":count_all_phd,
                    "count_all_phd_male":count_all_phd_male,
                    "count_all_phd_female":count_all_phd_female,
                    "count_all_phd_comp":count_all_phd_comp,
                    "count_all_phd_comp_male":count_all_phd_comp_male,
                    "count_all_phd_comp_female":count_all_phd_comp_female,
                    "count_all_phd_cont":count_all_phd_cont,
                    "count_all_phd_cont_male":count_all_phd_cont_male,
                    "count_all_phd_cont_female":count_all_phd_cont_female,
                    "count_all_phd_post":count_all_phd_post,
                    "count_all_phd_post_male":count_all_phd_post_male,
                    "count_all_phd_post_female":count_all_phd_post_female,
                    "count_all_phd_final":count_all_phd_final,
                    "count_all_phd_final_male":count_all_phd_final_male,
                    "count_all_phd_final_female":count_all_phd_final_female,
                    "forms":form
                    }
                    return render(request, templates, context)
            elif gender == '' and start_date and end_date == '' and status =='':
                get_all_phd_student_by_start_date=Student.objects.filter(education_level="PHD", start_date=str(start_date))
                templates="account/phd.html"
                context={
                "get_all_phd_student_by_start_date": get_all_phd_student_by_start_date,
                "count_all_phd":count_all_phd,
                "count_all_phd_male":count_all_phd_male,
                "count_all_phd_female":count_all_phd_female,
                "count_all_phd_comp":count_all_phd_comp,
                "count_all_phd_comp_male":count_all_phd_comp_male,
                "count_all_phd_comp_female":count_all_phd_comp_female,
                "count_all_phd_cont":count_all_phd_cont,
                "count_all_phd_cont_male":count_all_phd_cont_male,
                "count_all_phd_cont_female":count_all_phd_cont_female,
                "count_all_phd_post":count_all_phd_post,
                "count_all_phd_post_male":count_all_phd_post_male,
                "count_all_phd_post_female":count_all_phd_post_female,
                "count_all_phd_final":count_all_phd_final,
                "count_all_phd_final_male":count_all_phd_final_male,
                "count_all_phd_final_female":count_all_phd_final_female,
                "forms":form,
                "start_date":start_date
                }
                return render(request, templates, context)
            elif gender == '' and start_date ==''  and end_date and status =='':
                get_all_phd_student_by_end_date=Student.objects.filter(education_level="PHD", end_date=str(end_date))
                templates="account/phd.html"
                context={
                "get_all_phd_student_by_end_date": get_all_phd_student_by_end_date,
                "count_all_phd":count_all_phd,
                "count_all_phd_male":count_all_phd_male,
                "count_all_phd_female":count_all_phd_female,
                "count_all_phd_comp":count_all_phd_comp,
                "count_all_phd_comp_male":count_all_phd_comp_male,
                "count_all_phd_comp_female":count_all_phd_comp_female,
                "count_all_phd_cont":count_all_phd_cont,
                "count_all_phd_cont_male":count_all_phd_cont_male,
                "count_all_phd_cont_female":count_all_phd_cont_female,
                "count_all_phd_post":count_all_phd_post,
                "count_all_phd_post_male":count_all_phd_post_male,
                "count_all_phd_post_female":count_all_phd_post_female,
                "count_all_phd_final":count_all_phd_final,
                "count_all_phd_final_male":count_all_phd_final_male,
                "count_all_phd_final_female":count_all_phd_final_female,
                "forms":form,
                "end_date":end_date
                }
                return render(request, templates, context)
            elif gender =='' and start_date =='' and end_date == '' and status:
                if status == continuous:
                    get_all_phd_student_continuous=Student.objects.filter(education_level="PHD", student_status="continuous")
                    templates="account/phd.html"
                    context={
                    "get_all_phd_student_continuous": get_all_phd_student_continuous,
                    "count_all_phd":count_all_phd,
                    "count_all_phd_male":count_all_phd_male,
                    "count_all_phd_female":count_all_phd_female,
                    "count_all_phd_comp":count_all_phd_comp,
                    "count_all_phd_comp_male":count_all_phd_comp_male,
                    "count_all_phd_comp_female":count_all_phd_comp_female,
                    "count_all_phd_cont":count_all_phd_cont,
                    "count_all_phd_cont_male":count_all_phd_cont_male,
                    "count_all_phd_cont_female":count_all_phd_cont_female,
                    "count_all_phd_post":count_all_phd_post,
                    "count_all_phd_post_male":count_all_phd_post_male,
                    "count_all_phd_post_female":count_all_phd_post_female,
                    "count_all_phd_final":count_all_phd_final,
                    "count_all_phd_final_male":count_all_phd_final_male,
                    "count_all_phd_final_female":count_all_phd_final_female,
                    "forms":form,
                    "end_date":end_date
                    }
                    return render(request, templates, context)
                elif status == postpone:
                    get_all_phd_student_postpone=Student.objects.filter(education_level="PHD", student_status="postpone")
                    templates="account/phd.html"
                    context={
                    "get_all_phd_student_postpone": get_all_phd_student_postpone,
                    "count_all_phd":count_all_phd,
                    "count_all_phd_male":count_all_phd_male,
                    "count_all_phd_female":count_all_phd_female,
                    "count_all_phd_comp":count_all_phd_comp,
                    "count_all_phd_comp_male":count_all_phd_comp_male,
                    "count_all_phd_comp_female":count_all_phd_comp_female,
                    "count_all_phd_cont":count_all_phd_cont,
                    "count_all_phd_cont_male":count_all_phd_cont_male,
                    "count_all_phd_cont_female":count_all_phd_cont_female,
                    "count_all_phd_post":count_all_phd_post,
                    "count_all_phd_post_male":count_all_phd_post_male,
                    "count_all_phd_post_female":count_all_phd_post_female,
                    "count_all_phd_final":count_all_phd_final,
                    "count_all_phd_final_male":count_all_phd_final_male,
                    "count_all_phd_final_female":count_all_phd_final_female,
                    "forms":form,
                    "end_date":end_date
                    }
                    return render(request, templates, context)
                elif status == complete:
                    get_all_phd_student_complete=Student.objects.filter(education_level="PHD", student_status=complete)
                    templates="account/phd.html"
                    context={
                    "get_all_phd_student_complete": get_all_phd_student_complete,
                    "count_all_phd":count_all_phd,
                    "count_all_phd_male":count_all_phd_male,
                    "count_all_phd_female":count_all_phd_female,
                    "count_all_phd_comp":count_all_phd_comp,
                    "count_all_phd_comp_male":count_all_phd_comp_male,
                    "count_all_phd_comp_female":count_all_phd_comp_female,
                    "count_all_phd_cont":count_all_phd_cont,
                    "count_all_phd_cont_male":count_all_phd_cont_male,
                    "count_all_phd_cont_female":count_all_phd_cont_female,
                    "count_all_phd_post":count_all_phd_post,
                    "count_all_phd_post_male":count_all_phd_post_male,
                    "count_all_phd_post_female":count_all_phd_post_female,
                    "count_all_phd_final":count_all_phd_final,
                    "count_all_phd_final_male":count_all_phd_final_male,
                    "count_all_phd_final_female":count_all_phd_final_female,
                    "forms":form,
                    "end_date":end_date
                    }
                    return render(request, templates, context)
                else:
                    get_all_phd_student_final=Student.objects.filter(education_level="PHD", student_status=final)
                    templates="account/phd.html"
                    context={
                    "get_all_phd_student_final": get_all_phd_student_final,
                    "count_all_phd":count_all_phd,
                    "count_all_phd_male":count_all_phd_male,
                    "count_all_phd_female":count_all_phd_female,
                    "count_all_phd_comp":count_all_phd_comp,
                    "count_all_phd_comp_male":count_all_phd_comp_male,
                    "count_all_phd_comp_female":count_all_phd_comp_female,
                    "count_all_phd_cont":count_all_phd_cont,
                    "count_all_phd_cont_male":count_all_phd_cont_male,
                    "count_all_phd_cont_female":count_all_phd_cont_female,
                    "count_all_phd_post":count_all_phd_post,
                    "count_all_phd_post_male":count_all_phd_post_male,
                    "count_all_phd_post_female":count_all_phd_post_female,
                    "count_all_phd_final":count_all_phd_final,
                    "count_all_phd_final_male":count_all_phd_final_male,
                    "count_all_phd_final_female":count_all_phd_final_female,
                    "forms":form,
                    "end_date":end_date
                    }
                    return render(request, templates, context)
            ################## two selection #################################
            elif gender and start_date and end_date=='' and status=='':
                if gender == male:
                    get_all_phd_student_male_start_date=Student.objects.filter(education_level="PHD", gender=male, start_date=str(start_date))
                    templates="account/phd.html"
                    context={
                    "get_all_phd_student_male_start_date": get_all_phd_student_male_start_date,
                    "count_all_phd":count_all_phd,
                    "count_all_phd_male":count_all_phd_male,
                    "count_all_phd_female":count_all_phd_female,
                    "count_all_phd_comp":count_all_phd_comp,
                    "count_all_phd_comp_male":count_all_phd_comp_male,
                    "count_all_phd_comp_female":count_all_phd_comp_female,
                    "count_all_phd_cont":count_all_phd_cont,
                    "count_all_phd_cont_male":count_all_phd_cont_male,
                    "count_all_phd_cont_female":count_all_phd_cont_female,
                    "count_all_phd_post":count_all_phd_post,
                    "count_all_phd_post_male":count_all_phd_post_male,
                    "count_all_phd_post_female":count_all_phd_post_female,
                    "count_all_phd_final":count_all_phd_final,
                    "count_all_phd_final_male":count_all_phd_final_male,
                    "count_all_phd_final_female":count_all_phd_final_female,
                    "forms":form,
                    "start_date":start_date
                    }
                    return render(request, templates, context)
                else:
                    get_all_phd_student_female_start_date=Student.objects.filter(education_level="PHD", gender=female, start_date=str(start_date))
                    templates="account/phd.html"
                    context={
                    "get_all_phd_student_female_start_date": get_all_phd_student_female_start_date,
                    "count_all_phd":count_all_phd,
                    "count_all_phd_male":count_all_phd_male,
                    "count_all_phd_female":count_all_phd_female,
                    "count_all_phd_comp":count_all_phd_comp,
                    "count_all_phd_comp_male":count_all_phd_comp_male,
                    "count_all_phd_comp_female":count_all_phd_comp_female,
                    "count_all_phd_cont":count_all_phd_cont,
                    "count_all_phd_cont_male":count_all_phd_cont_male,
                    "count_all_phd_cont_female":count_all_phd_cont_female,
                    "count_all_phd_post":count_all_phd_post,
                    "count_all_phd_post_male":count_all_phd_post_male,
                    "count_all_phd_post_female":count_all_phd_post_female,
                    "count_all_phd_final":count_all_phd_final,
                    "count_all_phd_final_male":count_all_phd_final_male,
                    "count_all_phd_final_female":count_all_phd_final_female,
                    "forms":form,
                    "start_date":start_date
                    }
                    return render(request, templates, context)

            elif gender and start_date == '' and end_date and status =='':
                if gender == male:
                    get_all_phd_student_male_end_date=Student.objects.filter(education_level="PHD", gender=male, end_date=str(end_date))
                    templates="account/phd.html"
                    context={
                    "get_all_phd_student_male_end_date": get_all_phd_student_male_end_date,
                    "count_all_phd":count_all_phd,
                    "count_all_phd_male":count_all_phd_male,
                    "count_all_phd_female":count_all_phd_female,
                    "count_all_phd_comp":count_all_phd_comp,
                    "count_all_phd_comp_male":count_all_phd_comp_male,
                    "count_all_phd_comp_female":count_all_phd_comp_female,
                    "count_all_phd_cont":count_all_phd_cont,
                    "count_all_phd_cont_male":count_all_phd_cont_male,
                    "count_all_phd_cont_female":count_all_phd_cont_female,
                    "count_all_phd_post":count_all_phd_post,
                    "count_all_phd_post_male":count_all_phd_post_male,
                    "count_all_phd_post_female":count_all_phd_post_female,
                    "count_all_phd_final":count_all_phd_final,
                    "count_all_phd_final_male":count_all_phd_final_male,
                    "count_all_phd_final_female":count_all_phd_final_female,
                    "forms":form,
                    "end_date":end_date
                    }
                    return render(request, templates, context)
                else:
                    get_all_phd_student_female_end_date=Student.objects.filter(education_level="PHD", gender=female, end_date=str(end_date))
                    templates="account/phd.html"
                    context={
                    "get_all_phd_student_female_end_date": get_all_phd_student_female_end_date,
                    "count_all_phd":count_all_phd,
                    "count_all_phd_male":count_all_phd_male,
                    "count_all_phd_female":count_all_phd_female,
                    "count_all_phd_comp":count_all_phd_comp,
                    "count_all_phd_comp_male":count_all_phd_comp_male,
                    "count_all_phd_comp_female":count_all_phd_comp_female,
                    "count_all_phd_cont":count_all_phd_cont,
                    "count_all_phd_cont_male":count_all_phd_cont_male,
                    "count_all_phd_cont_female":count_all_phd_cont_female,
                    "count_all_phd_post":count_all_phd_post,
                    "count_all_phd_post_male":count_all_phd_post_male,
                    "count_all_phd_post_female":count_all_phd_post_female,
                    "count_all_phd_final":count_all_phd_final,
                    "count_all_phd_final_male":count_all_phd_final_male,
                    "count_all_phd_final_female":count_all_phd_final_female,
                    "forms":form,
                    "start_date":start_date
                    }
                    return render(request, templates, context)

            elif gender and start_date == '' and end_date =='' and status:

                if gender == male:
                    if status == continuous:
                        get_all_phd_student_continuous_male=Student.objects.filter(education_level="PHD", student_status=continuous, gender=male)
                        templates="account/phd.html"
                        context={
                        "get_all_phd_student_continuous_male": get_all_phd_student_continuous_male,
                        "count_all_phd":count_all_phd,
                        "count_all_phd_male":count_all_phd_male,
                        "count_all_phd_female":count_all_phd_female,
                        "count_all_phd_comp":count_all_phd_comp,
                        "count_all_phd_comp_male":count_all_phd_comp_male,
                        "count_all_phd_comp_female":count_all_phd_comp_female,
                        "count_all_phd_cont":count_all_phd_cont,
                        "count_all_phd_cont_male":count_all_phd_cont_male,
                        "count_all_phd_cont_female":count_all_phd_cont_female,
                        "count_all_phd_post":count_all_phd_post,
                        "count_all_phd_post_male":count_all_phd_post_male,
                        "count_all_phd_post_female":count_all_phd_post_female,
                        "count_all_phd_final":count_all_phd_final,
                        "count_all_phd_final_male":count_all_phd_final_male,
                        "count_all_phd_final_female":count_all_phd_final_female,
                        "forms":form,
                        "end_date":end_date
                        }
                        return render(request, templates, context)
                    elif status == postpone:
                        get_all_phd_student_postpone_male=Student.objects.filter(education_level="PHD", student_status=postpone, gender=male)
                        templates="account/phd.html"
                        context={
                        "get_all_phd_student_postpone_male": get_all_phd_student_postpone_male,
                        "count_all_phd":count_all_phd,
                        "count_all_phd_male":count_all_phd_male,
                        "count_all_phd_female":count_all_phd_female,
                        "count_all_phd_comp":count_all_phd_comp,
                        "count_all_phd_comp_male":count_all_phd_comp_male,
                        "count_all_phd_comp_female":count_all_phd_comp_female,
                        "count_all_phd_cont":count_all_phd_cont,
                        "count_all_phd_cont_male":count_all_phd_cont_male,
                        "count_all_phd_cont_female":count_all_phd_cont_female,
                        "count_all_phd_post":count_all_phd_post,
                        "count_all_phd_post_male":count_all_phd_post_male,
                        "count_all_phd_post_female":count_all_phd_post_female,
                        "count_all_phd_final":count_all_phd_final,
                        "count_all_phd_final_male":count_all_phd_final_male,
                        "count_all_phd_final_female":count_all_phd_final_female,
                        "forms":form,
                        "end_date":end_date
                        }
                        return render(request, templates, context)
                    elif status == complete:
                        get_all_phd_student_complete_male=Student.objects.filter(education_level="PHD", student_status=complete, gender=male)
                        templates="account/phd.html"
                        context={
                        "get_all_phd_student_complete_male": get_all_phd_student_complete_male,
                        "count_all_phd":count_all_phd,
                        "count_all_phd_male":count_all_phd_male,
                        "count_all_phd_female":count_all_phd_female,
                        "count_all_phd_comp":count_all_phd_comp,
                        "count_all_phd_comp_male":count_all_phd_comp_male,
                        "count_all_phd_comp_female":count_all_phd_comp_female,
                        "count_all_phd_cont":count_all_phd_cont,
                        "count_all_phd_cont_male":count_all_phd_cont_male,
                        "count_all_phd_cont_female":count_all_phd_cont_female,
                        "count_all_phd_post":count_all_phd_post,
                        "count_all_phd_post_male":count_all_phd_post_male,
                        "count_all_phd_post_female":count_all_phd_post_female,
                        "count_all_phd_final":count_all_phd_final,
                        "count_all_phd_final_male":count_all_phd_final_male,
                        "count_all_phd_final_female":count_all_phd_final_female,
                        "forms":form,
                        "end_date":end_date
                        }
                        return render(request, templates, context)
                    else:
                        get_all_phd_student_final_male=Student.objects.filter(education_level="PHD", student_status=final, gender=male)
                        templates="account/phd.html"
                        context={
                        "get_all_phd_student_final_male": get_all_phd_student_final_male,
                        "count_all_phd":count_all_phd,
                        "count_all_phd_male":count_all_phd_male,
                        "count_all_phd_female":count_all_phd_female,
                        "count_all_phd_comp":count_all_phd_comp,
                        "count_all_phd_comp_male":count_all_phd_comp_male,
                        "count_all_phd_comp_female":count_all_phd_comp_female,
                        "count_all_phd_cont":count_all_phd_cont,
                        "count_all_phd_cont_male":count_all_phd_cont_male,
                        "count_all_phd_cont_female":count_all_phd_cont_female,
                        "count_all_phd_post":count_all_phd_post,
                        "count_all_phd_post_male":count_all_phd_post_male,
                        "count_all_phd_post_female":count_all_phd_post_female,
                        "count_all_phd_final":count_all_phd_final,
                        "count_all_phd_final_male":count_all_phd_final_male,
                        "count_all_phd_final_female":count_all_phd_final_female,
                        "forms":form,
                        "end_date":end_date
                        }
                        return render(request, templates, context)
                else:
                    if status == continuous:
                        get_all_phd_student_continuous_female=Student.objects.filter(education_level="PHD", student_status=continuous, gender=female)
                        templates="account/phd.html"
                        context={
                        "get_all_phd_student_continuous_female": get_all_phd_student_continuous_female,
                        "count_all_phd":count_all_phd,
                        "count_all_phd_male":count_all_phd_male,
                        "count_all_phd_female":count_all_phd_female,
                        "count_all_phd_comp":count_all_phd_comp,
                        "count_all_phd_comp_male":count_all_phd_comp_male,
                        "count_all_phd_comp_female":count_all_phd_comp_female,
                        "count_all_phd_cont":count_all_phd_cont,
                        "count_all_phd_cont_male":count_all_phd_cont_male,
                        "count_all_phd_cont_female":count_all_phd_cont_female,
                        "count_all_phd_post":count_all_phd_post,
                        "count_all_phd_post_male":count_all_phd_post_male,
                        "count_all_phd_post_female":count_all_phd_post_female,
                        "count_all_phd_final":count_all_phd_final,
                        "count_all_phd_final_male":count_all_phd_final_male,
                        "count_all_phd_final_female":count_all_phd_final_female,
                        "forms":form,
                        "end_date":end_date
                        }
                        return render(request, templates, context)
                    elif status == postpone:
                        get_all_phd_student_postpone_female=Student.objects.filter(education_level="PHD", student_status=postpone, gender=female)
                        templates="account/phd.html"
                        context={
                        "get_all_phd_student_postpone_female": get_all_phd_student_postpone_female,
                        "count_all_phd":count_all_phd,
                        "count_all_phd_male":count_all_phd_male,
                        "count_all_phd_female":count_all_phd_female,
                        "count_all_phd_comp":count_all_phd_comp,
                        "count_all_phd_comp_male":count_all_phd_comp_male,
                        "count_all_phd_comp_female":count_all_phd_comp_female,
                        "count_all_phd_cont":count_all_phd_cont,
                        "count_all_phd_cont_male":count_all_phd_cont_male,
                        "count_all_phd_cont_female":count_all_phd_cont_female,
                        "count_all_phd_post":count_all_phd_post,
                        "count_all_phd_post_male":count_all_phd_post_male,
                        "count_all_phd_post_female":count_all_phd_post_female,
                        "count_all_phd_final":count_all_phd_final,
                        "count_all_phd_final_male":count_all_phd_final_male,
                        "count_all_phd_final_female":count_all_phd_final_female,
                        "forms":form,
                        "end_date":end_date
                        }
                        return render(request, templates, context)
                    elif status == complete:
                        get_all_phd_student_complete_female=Student.objects.filter(education_level="PHD", student_status=complete, gender=female)
                        templates="account/phd.html"
                        context={
                        "get_all_phd_student_complete_female":get_all_phd_student_complete_female ,
                        "count_all_phd":count_all_phd,
                        "count_all_phd_male":count_all_phd_male,
                        "count_all_phd_female":count_all_phd_female,
                        "count_all_phd_comp":count_all_phd_comp,
                        "count_all_phd_comp_male":count_all_phd_comp_male,
                        "count_all_phd_comp_female":count_all_phd_comp_female,
                        "count_all_phd_cont":count_all_phd_cont,
                        "count_all_phd_cont_male":count_all_phd_cont_male,
                        "count_all_phd_cont_female":count_all_phd_cont_female,
                        "count_all_phd_post":count_all_phd_post,
                        "count_all_phd_post_male":count_all_phd_post_male,
                        "count_all_phd_post_female":count_all_phd_post_female,
                        "count_all_phd_final":count_all_phd_final,
                        "count_all_phd_final_male":count_all_phd_final_male,
                        "count_all_phd_final_female":count_all_phd_final_female,
                        "forms":form,
                        "end_date":end_date
                        }
                        return render(request, templates, context)
                    else:
                        get_all_phd_student_final_female=Student.objects.filter(education_level="PHD", student_status=final, gender=female)
                        templates="account/phd.html"
                        context={
                        "get_all_phd_student_final_female":get_all_phd_student_final_female ,
                        "count_all_phd":count_all_phd,
                        "count_all_phd_male":count_all_phd_male,
                        "count_all_phd_female":count_all_phd_female,
                        "count_all_phd_comp":count_all_phd_comp,
                        "count_all_phd_comp_male":count_all_phd_comp_male,
                        "count_all_phd_comp_female":count_all_phd_comp_female,
                        "count_all_phd_cont":count_all_phd_cont,
                        "count_all_phd_cont_male":count_all_phd_cont_male,
                        "count_all_phd_cont_female":count_all_phd_cont_female,
                        "count_all_phd_post":count_all_phd_post,
                        "count_all_phd_post_male":count_all_phd_post_male,
                        "count_all_phd_post_female":count_all_phd_post_female,
                        "count_all_phd_final":count_all_phd_final,
                        "count_all_phd_final_male":count_all_phd_final_male,
                        "count_all_phd_final_female":count_all_phd_final_female,
                        "forms":form,
                        "end_date":end_date
                        }
                        return render(request, templates, context)
            elif gender == '' and start_date and end_date and status =='':
                get_all_phd_student_by_start_date_end_date=Student.objects.filter(education_level="PHD", start_date=start_date, end_date=end_date)
                templates="account/phd.html"
                context={
                "get_all_phd_student_by_start_date_end_date":get_all_phd_student_by_start_date_end_date ,
                "count_all_phd":count_all_phd,
                "count_all_phd_male":count_all_phd_male,
                "count_all_phd_female":count_all_phd_female,
                "count_all_phd_comp":count_all_phd_comp,
                "count_all_phd_comp_male":count_all_phd_comp_male,
                "count_all_phd_comp_female":count_all_phd_comp_female,
                "count_all_phd_cont":count_all_phd_cont,
                "count_all_phd_cont_male":count_all_phd_cont_male,
                "count_all_phd_cont_female":count_all_phd_cont_female,
                "count_all_phd_post":count_all_phd_post,
                "count_all_phd_post_male":count_all_phd_post_male,
                "count_all_phd_post_female":count_all_phd_post_female,
                "count_all_phd_final":count_all_phd_final,
                "count_all_phd_final_male":count_all_phd_final_male,
                "count_all_phd_final_female":count_all_phd_final_female,
                "forms":form,
                "start_date":start_date,
                "end_date":end_date
                }
                return render(request, templates, context)
            elif gender =='' and start_date and end_date =='' and status:
                if status == continuous:
                    get_all_phd_student_by_start_date_cnt=Student.objects.filter(education_level="PHD", start_date=start_date, student_status=continuous)
                    templates="account/phd.html"
                    context={
                    "get_all_phd_student_by_start_date_cnt":get_all_phd_student_by_start_date_cnt,
                    "count_all_phd":count_all_phd,
                    "count_all_phd_male":count_all_phd_male,
                    "count_all_phd_female":count_all_phd_female,
                    "count_all_phd_comp":count_all_phd_comp,
                    "count_all_phd_comp_male":count_all_phd_comp_male,
                    "count_all_phd_comp_female":count_all_phd_comp_female,
                    "count_all_phd_cont":count_all_phd_cont,
                    "count_all_phd_cont_male":count_all_phd_cont_male,
                    "count_all_phd_cont_female":count_all_phd_cont_female,
                    "count_all_phd_post":count_all_phd_post,
                    "count_all_phd_post_male":count_all_phd_post_male,
                    "count_all_phd_post_female":count_all_phd_post_female,
                    "count_all_phd_final":count_all_phd_final,
                    "count_all_phd_final_male":count_all_phd_final_male,
                    "count_all_phd_final_female":count_all_phd_final_female,
                    "forms":form,
                    "start_date":start_date,
                    "end_date":end_date
                    }
                    return render(request, templates, context)
                elif status == postpone:
                    get_all_phd_student_by_start_date_pst=Student.objects.filter(education_level="PHD", start_date=start_date, student_status=postpone)
                    templates="account/phd.html"
                    context={
                    "get_all_phd_student_by_start_date_pst":get_all_phd_student_by_start_date_pst,
                    "count_all_phd":count_all_phd,
                    "count_all_phd_male":count_all_phd_male,
                    "count_all_phd_female":count_all_phd_female,
                    "count_all_phd_comp":count_all_phd_comp,
                    "count_all_phd_comp_male":count_all_phd_comp_male,
                    "count_all_phd_comp_female":count_all_phd_comp_female,
                    "count_all_phd_cont":count_all_phd_cont,
                    "count_all_phd_cont_male":count_all_phd_cont_male,
                    "count_all_phd_cont_female":count_all_phd_cont_female,
                    "count_all_phd_post":count_all_phd_post,
                    "count_all_phd_post_male":count_all_phd_post_male,
                    "count_all_phd_post_female":count_all_phd_post_female,
                    "count_all_phd_final":count_all_phd_final,
                    "count_all_phd_final_male":count_all_phd_final_male,
                    "count_all_phd_final_female":count_all_phd_final_female,
                    "forms":form,
                    "start_date":start_date,
                    "end_date":end_date
                    }
                    return render(request, templates, context)
                elif status == complete:
                    get_all_phd_student_by_start_date_cmp=Student.objects.filter(education_level="PHD", start_date=start_date, student_status=complete)
                    templates="account/phd.html"
                    context={
                    "get_all_phd_student_by_start_date_cmp":get_all_phd_student_by_start_date_cmp,
                    "count_all_phd":count_all_phd,
                    "count_all_phd_male":count_all_phd_male,
                    "count_all_phd_female":count_all_phd_female,
                    "count_all_phd_comp":count_all_phd_comp,
                    "count_all_phd_comp_male":count_all_phd_comp_male,
                    "count_all_phd_comp_female":count_all_phd_comp_female,
                    "count_all_phd_cont":count_all_phd_cont,
                    "count_all_phd_cont_male":count_all_phd_cont_male,
                    "count_all_phd_cont_female":count_all_phd_cont_female,
                    "count_all_phd_post":count_all_phd_post,
                    "count_all_phd_post_male":count_all_phd_post_male,
                    "count_all_phd_post_female":count_all_phd_post_female,
                    "count_all_phd_final":count_all_phd_final,
                    "count_all_phd_final_male":count_all_phd_final_male,
                    "count_all_phd_final_female":count_all_phd_final_female,
                    "forms":form,
                    "start_date":start_date,
                    "end_date":end_date
                    }
                    return render(request, templates, context)
                else:
                    get_all_phd_student_by_start_date_fnl=Student.objects.filter(education_level="PHD", start_date=start_date, student_status=final)
                    templates="account/phd.html"
                    context={
                    "get_all_phd_student_by_start_date_fnl":get_all_phd_student_by_start_date_fnl,
                    "count_all_phd":count_all_phd,
                    "count_all_phd_male":count_all_phd_male,
                    "count_all_phd_female":count_all_phd_female,
                    "count_all_phd_comp":count_all_phd_comp,
                    "count_all_phd_comp_male":count_all_phd_comp_male,
                    "count_all_phd_comp_female":count_all_phd_comp_female,
                    "count_all_phd_cont":count_all_phd_cont,
                    "count_all_phd_cont_male":count_all_phd_cont_male,
                    "count_all_phd_cont_female":count_all_phd_cont_female,
                    "count_all_phd_post":count_all_phd_post,
                    "count_all_phd_post_male":count_all_phd_post_male,
                    "count_all_phd_post_female":count_all_phd_post_female,
                    "count_all_phd_final":count_all_phd_final,
                    "count_all_phd_final_male":count_all_phd_final_male,
                    "count_all_phd_final_female":count_all_phd_final_female,
                    "forms":form,
                    "start_date":start_date,
                    "end_date":end_date
                    }
                    return render(request, templates, context)
                    pass

            elif gender == '' and start_date == '' and end_date and status:
                if status == continuous:
                    get_all_phd_student_by_end_date_cnt=Student.objects.filter(education_level="PHD", end_date=end_date, student_status=continuous)
                    templates="account/phd.html"
                    context={
                    "get_all_phd_student_by_end_date_cnt":get_all_phd_student_by_end_date_cnt,
                    "count_all_phd":count_all_phd,
                    "count_all_phd_male":count_all_phd_male,
                    "count_all_phd_female":count_all_phd_female,
                    "count_all_phd_comp":count_all_phd_comp,
                    "count_all_phd_comp_male":count_all_phd_comp_male,
                    "count_all_phd_comp_female":count_all_phd_comp_female,
                    "count_all_phd_cont":count_all_phd_cont,
                    "count_all_phd_cont_male":count_all_phd_cont_male,
                    "count_all_phd_cont_female":count_all_phd_cont_female,
                    "count_all_phd_post":count_all_phd_post,
                    "count_all_phd_post_male":count_all_phd_post_male,
                    "count_all_phd_post_female":count_all_phd_post_female,
                    "count_all_phd_final":count_all_phd_final,
                    "count_all_phd_final_male":count_all_phd_final_male,
                    "count_all_phd_final_female":count_all_phd_final_female,
                    "forms":form,
                    "start_date":start_date,
                    "end_date":end_date
                    }
                    return render(request, templates, context)
                elif status == postpone:
                    get_all_phd_student_by_end_date_pst=Student.objects.filter(education_level="PHD", end_date=end_date, student_status=postpone)
                    templates="account/phd.html"
                    context={
                    "get_all_phd_student_by_end_date_pst":get_all_phd_student_by_end_date_pst,
                    "count_all_phd":count_all_phd,
                    "count_all_phd_male":count_all_phd_male,
                    "count_all_phd_female":count_all_phd_female,
                    "count_all_phd_comp":count_all_phd_comp,
                    "count_all_phd_comp_male":count_all_phd_comp_male,
                    "count_all_phd_comp_female":count_all_phd_comp_female,
                    "count_all_phd_cont":count_all_phd_cont,
                    "count_all_phd_cont_male":count_all_phd_cont_male,
                    "count_all_phd_cont_female":count_all_phd_cont_female,
                    "count_all_phd_post":count_all_phd_post,
                    "count_all_phd_post_male":count_all_phd_post_male,
                    "count_all_phd_post_female":count_all_phd_post_female,
                    "count_all_phd_final":count_all_phd_final,
                    "count_all_phd_final_male":count_all_phd_final_male,
                    "count_all_phd_final_female":count_all_phd_final_female,
                    "forms":form,
                    "start_date":start_date,
                    "end_date":end_date
                    }
                    return render(request, templates, context)
                elif status == complete:
                    get_all_phd_student_by_end_date_cmp=Student.objects.filter(education_level="PHD", end_date=end_date, student_status=complete)
                    templates="account/phd.html"
                    context={
                    "get_all_phd_student_by_end_date_cmp":get_all_phd_student_by_end_date_cmp,
                    "count_all_phd":count_all_phd,
                    "count_all_phd_male":count_all_phd_male,
                    "count_all_phd_female":count_all_phd_female,
                    "count_all_phd_comp":count_all_phd_comp,
                    "count_all_phd_comp_male":count_all_phd_comp_male,
                    "count_all_phd_comp_female":count_all_phd_comp_female,
                    "count_all_phd_cont":count_all_phd_cont,
                    "count_all_phd_cont_male":count_all_phd_cont_male,
                    "count_all_phd_cont_female":count_all_phd_cont_female,
                    "count_all_phd_post":count_all_phd_post,
                    "count_all_phd_post_male":count_all_phd_post_male,
                    "count_all_phd_post_female":count_all_phd_post_female,
                    "count_all_phd_final":count_all_phd_final,
                    "count_all_phd_final_male":count_all_phd_final_male,
                    "count_all_phd_final_female":count_all_phd_final_female,
                    "forms":form,
                    "start_date":start_date,
                    "end_date":end_date
                    }
                    return render(request, templates, context)
                else:
                    get_all_phd_student_by_end_date_fnl=Student.objects.filter(education_level="PHD", end_date=end_date, student_status=final)
                    templates="account/phd.html"
                    context={
                    "get_all_phd_student_by_end_date_fnl":get_all_phd_student_by_end_date_fnl,
                    "count_all_phd":count_all_phd,
                    "count_all_phd_male":count_all_phd_male,
                    "count_all_phd_female":count_all_phd_female,
                    "count_all_phd_comp":count_all_phd_comp,
                    "count_all_phd_comp_male":count_all_phd_comp_male,
                    "count_all_phd_comp_female":count_all_phd_comp_female,
                    "count_all_phd_cont":count_all_phd_cont,
                    "count_all_phd_cont_male":count_all_phd_cont_male,
                    "count_all_phd_cont_female":count_all_phd_cont_female,
                    "count_all_phd_post":count_all_phd_post,
                    "count_all_phd_post_male":count_all_phd_post_male,
                    "count_all_phd_post_female":count_all_phd_post_female,
                    "count_all_phd_final":count_all_phd_final,
                    "count_all_phd_final_male":count_all_phd_final_male,
                    "count_all_phd_final_female":count_all_phd_final_female,
                    "forms":form,
                    "start_date":start_date,
                    "end_date":end_date
                    }
                    return render(request, templates, context)
                    pass

            ################## triple selection ################################
            elif gender and start_date and end_date and status =='':
                if gender == male:
                    get_all_phd_student_by_start_date_end_date_male=Student.objects.filter(education_level="PHD", start_date=start_date, end_date=end_date, gender=male)
                    templates="account/phd.html"
                    context={
                    "get_all_phd_student_by_start_date_end_date_male":get_all_phd_student_by_start_date_end_date_male ,
                    "count_all_phd":count_all_phd,
                    "count_all_phd_male":count_all_phd_male,
                    "count_all_phd_female":count_all_phd_female,
                    "count_all_phd_comp":count_all_phd_comp,
                    "count_all_phd_comp_male":count_all_phd_comp_male,
                    "count_all_phd_comp_female":count_all_phd_comp_female,
                    "count_all_phd_cont":count_all_phd_cont,
                    "count_all_phd_cont_male":count_all_phd_cont_male,
                    "count_all_phd_cont_female":count_all_phd_cont_female,
                    "count_all_phd_post":count_all_phd_post,
                    "count_all_phd_post_male":count_all_phd_post_male,
                    "count_all_phd_post_female":count_all_phd_post_female,
                    "count_all_phd_final":count_all_phd_final,
                    "count_all_phd_final_male":count_all_phd_final_male,
                    "count_all_phd_final_female":count_all_phd_final_female,
                    "forms":form,
                    "start_date":start_date,
                    "end_date":end_date
                    }
                    return render(request, templates, context)
                else:
                    get_all_phd_student_by_start_date_end_date_female=Student.objects.filter(education_level="PHD", start_date=start_date, end_date=end_date, gender=female)
                    templates="account/phd.html"
                    context={
                    "get_all_phd_student_by_start_date_end_date_female":get_all_phd_student_by_start_date_end_date_female ,
                    "count_all_phd":count_all_phd,
                    "count_all_phd_male":count_all_phd_male,
                    "count_all_phd_female":count_all_phd_female,
                    "count_all_phd_comp":count_all_phd_comp,
                    "count_all_phd_comp_male":count_all_phd_comp_male,
                    "count_all_phd_comp_female":count_all_phd_comp_female,
                    "count_all_phd_cont":count_all_phd_cont,
                    "count_all_phd_cont_male":count_all_phd_cont_male,
                    "count_all_phd_cont_female":count_all_phd_cont_female,
                    "count_all_phd_post":count_all_phd_post,
                    "count_all_phd_post_male":count_all_phd_post_male,
                    "count_all_phd_post_female":count_all_phd_post_female,
                    "count_all_phd_final":count_all_phd_final,
                    "count_all_phd_final_male":count_all_phd_final_male,
                    "count_all_phd_final_female":count_all_phd_final_female,
                    "forms":form,
                    "start_date":start_date,
                    "end_date":end_date
                    }
                    return render(request, templates, context)

            elif gender and start_date and end_date=="" and status:
                if gender == male:
                    if status == continuous:
                        get_all_phd_student_by_start_date_cnt_male=Student.objects.filter(education_level="PHD", start_date=start_date, student_status=continuous, gender=male)
                        templates="account/phd.html"
                        context={
                        "get_all_phd_student_by_start_date_cnt_male":get_all_phd_student_by_start_date_cnt_male,
                        "count_all_phd":count_all_phd,
                        "count_all_phd_male":count_all_phd_male,
                        "count_all_phd_female":count_all_phd_female,
                        "count_all_phd_comp":count_all_phd_comp,
                        "count_all_phd_comp_male":count_all_phd_comp_male,
                        "count_all_phd_comp_female":count_all_phd_comp_female,
                        "count_all_phd_cont":count_all_phd_cont,
                        "count_all_phd_cont_male":count_all_phd_cont_male,
                        "count_all_phd_cont_female":count_all_phd_cont_female,
                        "count_all_phd_post":count_all_phd_post,
                        "count_all_phd_post_male":count_all_phd_post_male,
                        "count_all_phd_post_female":count_all_phd_post_female,
                        "count_all_phd_final":count_all_phd_final,
                        "count_all_phd_final_male":count_all_phd_final_male,
                        "count_all_phd_final_female":count_all_phd_final_female,
                        "forms":form,
                        "start_date":start_date,
                        "end_date":end_date
                        }
                        return render(request, templates, context)
                    elif status == postpone:
                        get_all_phd_student_by_start_date_pst_male=Student.objects.filter(education_level="PHD", start_date=start_date, student_status=postpone, gender=male)
                        templates="account/phd.html"
                        context={
                        "get_all_phd_student_by_start_date_pst_male":get_all_phd_student_by_start_date_pst_male,
                        "count_all_phd":count_all_phd,
                        "count_all_phd_male":count_all_phd_male,
                        "count_all_phd_female":count_all_phd_female,
                        "count_all_phd_comp":count_all_phd_comp,
                        "count_all_phd_comp_male":count_all_phd_comp_male,
                        "count_all_phd_comp_female":count_all_phd_comp_female,
                        "count_all_phd_cont":count_all_phd_cont,
                        "count_all_phd_cont_male":count_all_phd_cont_male,
                        "count_all_phd_cont_female":count_all_phd_cont_female,
                        "count_all_phd_post":count_all_phd_post,
                        "count_all_phd_post_male":count_all_phd_post_male,
                        "count_all_phd_post_female":count_all_phd_post_female,
                        "count_all_phd_final":count_all_phd_final,
                        "count_all_phd_final_male":count_all_phd_final_male,
                        "count_all_phd_final_female":count_all_phd_final_female,
                        "forms":form,
                        "start_date":start_date,
                        "end_date":end_date
                        }
                        return render(request, templates, context)
                    elif status == complete:
                        get_all_phd_student_by_start_date_cmp_male=Student.objects.filter(education_level="PHD", start_date=start_date, student_status=complete, gender= male)
                        templates="account/phd.html"
                        context={
                        "get_all_phd_student_by_start_date_cmp_male":get_all_phd_student_by_start_date_cmp_male,
                        "count_all_phd":count_all_phd,
                        "count_all_phd_male":count_all_phd_male,
                        "count_all_phd_female":count_all_phd_female,
                        "count_all_phd_comp":count_all_phd_comp,
                        "count_all_phd_comp_male":count_all_phd_comp_male,
                        "count_all_phd_comp_female":count_all_phd_comp_female,
                        "count_all_phd_cont":count_all_phd_cont,
                        "count_all_phd_cont_male":count_all_phd_cont_male,
                        "count_all_phd_cont_female":count_all_phd_cont_female,
                        "count_all_phd_post":count_all_phd_post,
                        "count_all_phd_post_male":count_all_phd_post_male,
                        "count_all_phd_post_female":count_all_phd_post_female,
                        "count_all_phd_final":count_all_phd_final,
                        "count_all_phd_final_male":count_all_phd_final_male,
                        "count_all_phd_final_female":count_all_phd_final_female,
                        "forms":form,
                        "start_date":start_date,
                        "end_date":end_date
                        }
                        return render(request, templates, context)
                    else:
                        get_all_phd_student_by_start_date_fnl_male=Student.objects.filter(education_level="PHD", start_date=start_date, student_status=final, gender=male)
                        templates="account/phd.html"
                        context={
                        "get_all_phd_student_by_start_date_fnl_male":get_all_phd_student_by_start_date_fnl_male,
                        "count_all_phd":count_all_phd,
                        "count_all_phd_male":count_all_phd_male,
                        "count_all_phd_female":count_all_phd_female,
                        "count_all_phd_comp":count_all_phd_comp,
                        "count_all_phd_comp_male":count_all_phd_comp_male,
                        "count_all_phd_comp_female":count_all_phd_comp_female,
                        "count_all_phd_cont":count_all_phd_cont,
                        "count_all_phd_cont_male":count_all_phd_cont_male,
                        "count_all_phd_cont_female":count_all_phd_cont_female,
                        "count_all_phd_post":count_all_phd_post,
                        "count_all_phd_post_male":count_all_phd_post_male,
                        "count_all_phd_post_female":count_all_phd_post_female,
                        "count_all_phd_final":count_all_phd_final,
                        "count_all_phd_final_male":count_all_phd_final_male,
                        "count_all_phd_final_female":count_all_phd_final_female,
                        "forms":form,
                        "start_date":start_date,
                        "end_date":end_date
                        }
                        return render(request, templates, context)
                else:
                    if status == continuous:
                        get_all_phd_student_by_start_date_cnt_female=Student.objects.filter(education_level="PHD", start_date=start_date, student_status=continuous, gender=female)
                        templates="account/phd.html"
                        context={
                        "get_all_phd_student_by_start_date_cnt_female":get_all_phd_student_by_start_date_cnt_female,
                        "count_all_phd":count_all_phd,
                        "count_all_phd_male":count_all_phd_male,
                        "count_all_phd_female":count_all_phd_female,
                        "count_all_phd_comp":count_all_phd_comp,
                        "count_all_phd_comp_male":count_all_phd_comp_male,
                        "count_all_phd_comp_female":count_all_phd_comp_female,
                        "count_all_phd_cont":count_all_phd_cont,
                        "count_all_phd_cont_male":count_all_phd_cont_male,
                        "count_all_phd_cont_female":count_all_phd_cont_female,
                        "count_all_phd_post":count_all_phd_post,
                        "count_all_phd_post_male":count_all_phd_post_male,
                        "count_all_phd_post_female":count_all_phd_post_female,
                        "count_all_phd_final":count_all_phd_final,
                        "count_all_phd_final_male":count_all_phd_final_male,
                        "count_all_phd_final_female":count_all_phd_final_female,
                        "forms":form,
                        "start_date":start_date,
                        "end_date":end_date
                        }
                        return render(request, templates, context)
                    elif status == postpone:
                        get_all_phd_student_by_start_date_pst_female=Student.objects.filter(education_level="PHD", start_date=start_date, student_status=postpone, gender=female)
                        templates="account/phd.html"
                        context={
                        "get_all_phd_student_by_start_date_pst_female":get_all_phd_student_by_start_date_pst_female,
                        "count_all_phd":count_all_phd,
                        "count_all_phd_male":count_all_phd_male,
                        "count_all_phd_female":count_all_phd_female,
                        "count_all_phd_comp":count_all_phd_comp,
                        "count_all_phd_comp_male":count_all_phd_comp_male,
                        "count_all_phd_comp_female":count_all_phd_comp_female,
                        "count_all_phd_cont":count_all_phd_cont,
                        "count_all_phd_cont_male":count_all_phd_cont_male,
                        "count_all_phd_cont_female":count_all_phd_cont_female,
                        "count_all_phd_post":count_all_phd_post,
                        "count_all_phd_post_male":count_all_phd_post_male,
                        "count_all_phd_post_female":count_all_phd_post_female,
                        "count_all_phd_final":count_all_phd_final,
                        "count_all_phd_final_male":count_all_phd_final_male,
                        "count_all_phd_final_female":count_all_phd_final_female,
                        "forms":form,
                        "start_date":start_date,
                        "end_date":end_date
                        }
                        return render(request, templates, context)
                    elif status == complete:
                        get_all_phd_student_by_start_date_cmp_female=Student.objects.filter(education_level="PHD", start_date=start_date, student_status=complete, gender= male)
                        templates="account/phd.html"
                        context={
                        "get_all_phd_student_by_start_date_cmp_female":get_all_phd_student_by_start_date_cmp_female,
                        "count_all_phd":count_all_phd,
                        "count_all_phd_male":count_all_phd_male,
                        "count_all_phd_female":count_all_phd_female,
                        "count_all_phd_comp":count_all_phd_comp,
                        "count_all_phd_comp_male":count_all_phd_comp_male,
                        "count_all_phd_comp_female":count_all_phd_comp_female,
                        "count_all_phd_cont":count_all_phd_cont,
                        "count_all_phd_cont_male":count_all_phd_cont_male,
                        "count_all_phd_cont_female":count_all_phd_cont_female,
                        "count_all_phd_post":count_all_phd_post,
                        "count_all_phd_post_male":count_all_phd_post_male,
                        "count_all_phd_post_female":count_all_phd_post_female,
                        "count_all_phd_final":count_all_phd_final,
                        "count_all_phd_final_male":count_all_phd_final_male,
                        "count_all_phd_final_female":count_all_phd_final_female,
                        "forms":form,
                        "start_date":start_date,
                        "end_date":end_date
                        }
                        return render(request, templates, context)
                    else:
                        get_all_phd_student_by_start_date_fnl_female=Student.objects.filter(education_level="PHD", start_date=start_date, student_status=final, gender= female)
                        templates="account/phd.html"
                        context={
                        "get_all_phd_student_by_start_date_fnl_female":get_all_phd_student_by_start_date_fnl_female,
                        "count_all_phd":count_all_phd,
                        "count_all_phd_male":count_all_phd_male,
                        "count_all_phd_female":count_all_phd_female,
                        "count_all_phd_comp":count_all_phd_comp,
                        "count_all_phd_comp_male":count_all_phd_comp_male,
                        "count_all_phd_comp_female":count_all_phd_comp_female,
                        "count_all_phd_cont":count_all_phd_cont,
                        "count_all_phd_cont_male":count_all_phd_cont_male,
                        "count_all_phd_cont_female":count_all_phd_cont_female,
                        "count_all_phd_post":count_all_phd_post,
                        "count_all_phd_post_male":count_all_phd_post_male,
                        "count_all_phd_post_female":count_all_phd_post_female,
                        "count_all_phd_final":count_all_phd_final,
                        "count_all_phd_final_male":count_all_phd_final_male,
                        "count_all_phd_final_female":count_all_phd_final_female,
                        "forms":form,
                        "start_date":start_date,
                        "end_date":end_date
                        }
                        return render(request, templates, context)
            elif gender and start_date =='' and end_date and status:
                if gender == male:
                    if status == continuous:
                        get_all_phd_student_by_end_date_cnt_male=Student.objects.filter(education_level="PHD", end_date=end_date, student_status=continuous, gender=male)
                        templates="account/phd.html"
                        context={
                        "get_all_phd_student_by_end_date_cnt_male":get_all_phd_student_by_end_date_cnt_male,
                        "count_all_phd":count_all_phd,
                        "count_all_phd_male":count_all_phd_male,
                        "count_all_phd_female":count_all_phd_female,
                        "count_all_phd_comp":count_all_phd_comp,
                        "count_all_phd_comp_male":count_all_phd_comp_male,
                        "count_all_phd_comp_female":count_all_phd_comp_female,
                        "count_all_phd_cont":count_all_phd_cont,
                        "count_all_phd_cont_male":count_all_phd_cont_male,
                        "count_all_phd_cont_female":count_all_phd_cont_female,
                        "count_all_phd_post":count_all_phd_post,
                        "count_all_phd_post_male":count_all_phd_post_male,
                        "count_all_phd_post_female":count_all_phd_post_female,
                        "count_all_phd_final":count_all_phd_final,
                        "count_all_phd_final_male":count_all_phd_final_male,
                        "count_all_phd_final_female":count_all_phd_final_female,
                        "forms":form,
                        "start_date":start_date,
                        "end_date":end_date
                        }
                        return render(request, templates, context)
                    elif status == postpone:
                        get_all_phd_student_by_end_date_pst_male=Student.objects.filter(education_level="PHD", end_date=end_date, student_status=postpone, gender=male)
                        templates="account/phd.html"
                        context={
                        "get_all_phd_student_by_end_date_pst_male":get_all_phd_student_by_end_date_pst_male,
                        "count_all_phd":count_all_phd,
                        "count_all_phd_male":count_all_phd_male,
                        "count_all_phd_female":count_all_phd_female,
                        "count_all_phd_comp":count_all_phd_comp,
                        "count_all_phd_comp_male":count_all_phd_comp_male,
                        "count_all_phd_comp_female":count_all_phd_comp_female,
                        "count_all_phd_cont":count_all_phd_cont,
                        "count_all_phd_cont_male":count_all_phd_cont_male,
                        "count_all_phd_cont_female":count_all_phd_cont_female,
                        "count_all_phd_post":count_all_phd_post,
                        "count_all_phd_post_male":count_all_phd_post_male,
                        "count_all_phd_post_female":count_all_phd_post_female,
                        "count_all_phd_final":count_all_phd_final,
                        "count_all_phd_final_male":count_all_phd_final_male,
                        "count_all_phd_final_female":count_all_phd_final_female,
                        "forms":form,
                        "start_date":start_date,
                        "end_date":end_date
                        }
                        return render(request, templates, context)
                    elif status == complete:
                        get_all_phd_student_by_end_date_cmp_male=Student.objects.filter(education_level="PHD", end_date=end_date, student_status=complete, gender= male)
                        templates="account/phd.html"
                        context={
                        "get_all_phd_student_by_end_date_cmp_male":get_all_phd_student_by_end_date_cmp_male,
                        "count_all_phd":count_all_phd,
                        "count_all_phd_male":count_all_phd_male,
                        "count_all_phd_female":count_all_phd_female,
                        "count_all_phd_comp":count_all_phd_comp,
                        "count_all_phd_comp_male":count_all_phd_comp_male,
                        "count_all_phd_comp_female":count_all_phd_comp_female,
                        "count_all_phd_cont":count_all_phd_cont,
                        "count_all_phd_cont_male":count_all_phd_cont_male,
                        "count_all_phd_cont_female":count_all_phd_cont_female,
                        "count_all_phd_post":count_all_phd_post,
                        "count_all_phd_post_male":count_all_phd_post_male,
                        "count_all_phd_post_female":count_all_phd_post_female,
                        "count_all_phd_final":count_all_phd_final,
                        "count_all_phd_final_male":count_all_phd_final_male,
                        "count_all_phd_final_female":count_all_phd_final_female,
                        "forms":form,
                        "start_date":start_date,
                        "end_date":end_date
                        }
                        return render(request, templates, context)
                    else:
                        get_all_phd_student_by_end_date_fnl_male=Student.objects.filter(education_level="PHD", end_date=end_date, student_status=final, gender=male)
                        templates="account/phd.html"
                        context={
                        "get_all_phd_student_by_end_date_fnl_male":get_all_phd_student_by_end_date_fnl_male,
                        "count_all_phd":count_all_phd,
                        "count_all_phd_male":count_all_phd_male,
                        "count_all_phd_female":count_all_phd_female,
                        "count_all_phd_comp":count_all_phd_comp,
                        "count_all_phd_comp_male":count_all_phd_comp_male,
                        "count_all_phd_comp_female":count_all_phd_comp_female,
                        "count_all_phd_cont":count_all_phd_cont,
                        "count_all_phd_cont_male":count_all_phd_cont_male,
                        "count_all_phd_cont_female":count_all_phd_cont_female,
                        "count_all_phd_post":count_all_phd_post,
                        "count_all_phd_post_male":count_all_phd_post_male,
                        "count_all_phd_post_female":count_all_phd_post_female,
                        "count_all_phd_final":count_all_phd_final,
                        "count_all_phd_final_male":count_all_phd_final_male,
                        "count_all_phd_final_female":count_all_phd_final_female,
                        "forms":form,
                        "start_date":start_date,
                        "end_date":end_date
                        }
                        return render(request, templates, context)
                else:
                    if status == continuous:
                        get_all_phd_student_by_end_date_cnt_female=Student.objects.filter(education_level="PHD", end_date=end_date, student_status=continuous, gender=female)
                        templates="account/phd.html"
                        context={
                        "get_all_phd_student_by_end_date_cnt_female":get_all_phd_student_by_end_date_cnt_female,
                        "count_all_phd":count_all_phd,
                        "count_all_phd_male":count_all_phd_male,
                        "count_all_phd_female":count_all_phd_female,
                        "count_all_phd_comp":count_all_phd_comp,
                        "count_all_phd_comp_male":count_all_phd_comp_male,
                        "count_all_phd_comp_female":count_all_phd_comp_female,
                        "count_all_phd_cont":count_all_phd_cont,
                        "count_all_phd_cont_male":count_all_phd_cont_male,
                        "count_all_phd_cont_female":count_all_phd_cont_female,
                        "count_all_phd_post":count_all_phd_post,
                        "count_all_phd_post_male":count_all_phd_post_male,
                        "count_all_phd_post_female":count_all_phd_post_female,
                        "count_all_phd_final":count_all_phd_final,
                        "count_all_phd_final_male":count_all_phd_final_male,
                        "count_all_phd_final_female":count_all_phd_final_female,
                        "forms":form,
                        "start_date":start_date,
                        "end_date":end_date
                        }
                        return render(request, templates, context)
                    elif status == postpone:
                        get_all_phd_student_by_end_date_pst_female=Student.objects.filter(education_level="PHD", end_date=end_date, student_status=postpone, gender=female)
                        templates="account/phd.html"
                        context={
                        "get_all_phd_student_by_end_date_pst_female":get_all_phd_student_by_end_date_pst_female,
                        "count_all_phd":count_all_phd,
                        "count_all_phd_male":count_all_phd_male,
                        "count_all_phd_female":count_all_phd_female,
                        "count_all_phd_comp":count_all_phd_comp,
                        "count_all_phd_comp_male":count_all_phd_comp_male,
                        "count_all_phd_comp_female":count_all_phd_comp_female,
                        "count_all_phd_cont":count_all_phd_cont,
                        "count_all_phd_cont_male":count_all_phd_cont_male,
                        "count_all_phd_cont_female":count_all_phd_cont_female,
                        "count_all_phd_post":count_all_phd_post,
                        "count_all_phd_post_male":count_all_phd_post_male,
                        "count_all_phd_post_female":count_all_phd_post_female,
                        "count_all_phd_final":count_all_phd_final,
                        "count_all_phd_final_male":count_all_phd_final_male,
                        "count_all_phd_final_female":count_all_phd_final_female,
                        "forms":form,
                        "start_date":start_date,
                        "end_date":end_date
                        }
                        return render(request, templates, context)
                    elif status == complete:
                        get_all_phd_student_by_end_date_cmp_female=Student.objects.filter(education_level="PHD", end_date=end_date, student_status=complete, gender= male)
                        templates="account/phd.html"
                        context={
                        "get_all_phd_student_by_end_date_cmp_female":get_all_phd_student_by_end_date_cmp_female,
                        "count_all_phd":count_all_phd,
                        "count_all_phd_male":count_all_phd_male,
                        "count_all_phd_female":count_all_phd_female,
                        "count_all_phd_comp":count_all_phd_comp,
                        "count_all_phd_comp_male":count_all_phd_comp_male,
                        "count_all_phd_comp_female":count_all_phd_comp_female,
                        "count_all_phd_cont":count_all_phd_cont,
                        "count_all_phd_cont_male":count_all_phd_cont_male,
                        "count_all_phd_cont_female":count_all_phd_cont_female,
                        "count_all_phd_post":count_all_phd_post,
                        "count_all_phd_post_male":count_all_phd_post_male,
                        "count_all_phd_post_female":count_all_phd_post_female,
                        "count_all_phd_final":count_all_phd_final,
                        "count_all_phd_final_male":count_all_phd_final_male,
                        "count_all_phd_final_female":count_all_phd_final_female,
                        "forms":form,
                        "start_date":start_date,
                        "end_date":end_date
                        }
                        return render(request, templates, context)
                    else:
                        get_all_phd_student_by_end_date_fnl_female=Student.objects.filter(education_level="PHD", end_date=end_date, student_status=final, gender=female)
                        templates="account/phd.html"
                        context={
                        "get_all_phd_student_by_end_date_fnl_female":get_all_phd_student_by_end_date_fnl_female,
                        "count_all_phd":count_all_phd,
                        "count_all_phd_male":count_all_phd_male,
                        "count_all_phd_female":count_all_phd_female,
                        "count_all_phd_comp":count_all_phd_comp,
                        "count_all_phd_comp_male":count_all_phd_comp_male,
                        "count_all_phd_comp_female":count_all_phd_comp_female,
                        "count_all_phd_cont":count_all_phd_cont,
                        "count_all_phd_cont_male":count_all_phd_cont_male,
                        "count_all_phd_cont_female":count_all_phd_cont_female,
                        "count_all_phd_post":count_all_phd_post,
                        "count_all_phd_post_male":count_all_phd_post_male,
                        "count_all_phd_post_female":count_all_phd_post_female,
                        "count_all_phd_final":count_all_phd_final,
                        "count_all_phd_final_male":count_all_phd_final_male,
                        "count_all_phd_final_female":count_all_phd_final_female,
                        "forms":form,
                        "start_date":start_date,
                        "end_date":end_date
                        }
                        return render(request, templates, context)
            elif gender=='' and start_date and end_date and status:
                if status == continuous:
                    get_all_phd_student_by_start_date_end_date_cnt=Student.objects.filter(education_level="PHD",start_date=start_date, end_date=end_date, student_status=continuous)
                    templates="account/phd.html"
                    context={
                    "get_all_phd_student_by_start_date_end_date_cnt":get_all_phd_student_by_start_date_end_date_cnt,
                    "count_all_phd":count_all_phd,
                    "count_all_phd_male":count_all_phd_male,
                    "count_all_phd_female":count_all_phd_female,
                    "count_all_phd_comp":count_all_phd_comp,
                    "count_all_phd_comp_male":count_all_phd_comp_male,
                    "count_all_phd_comp_female":count_all_phd_comp_female,
                    "count_all_phd_cont":count_all_phd_cont,
                    "count_all_phd_cont_male":count_all_phd_cont_male,
                    "count_all_phd_cont_female":count_all_phd_cont_female,
                    "count_all_phd_post":count_all_phd_post,
                    "count_all_phd_post_male":count_all_phd_post_male,
                    "count_all_phd_post_female":count_all_phd_post_female,
                    "count_all_phd_final":count_all_phd_final,
                    "count_all_phd_final_male":count_all_phd_final_male,
                    "count_all_phd_final_female":count_all_phd_final_female,
                    "forms":form,
                    "start_date":start_date,
                    "end_date":end_date
                    }
                    return render(request, templates, context)
                elif status == postpone:
                    get_all_phd_student_by_start_date_end_date_pst=Student.objects.filter(education_level="PHD", start_date=start_date, end_date=end_date, student_status=postpone)
                    templates="account/phd.html"
                    context={
                    "get_all_phd_student_by_start_date_end_date_pst":get_all_phd_student_by_start_date_end_date_pst,
                    "count_all_phd":count_all_phd,
                    "count_all_phd_male":count_all_phd_male,
                    "count_all_phd_female":count_all_phd_female,
                    "count_all_phd_comp":count_all_phd_comp,
                    "count_all_phd_comp_male":count_all_phd_comp_male,
                    "count_all_phd_comp_female":count_all_phd_comp_female,
                    "count_all_phd_cont":count_all_phd_cont,
                    "count_all_phd_cont_male":count_all_phd_cont_male,
                    "count_all_phd_cont_female":count_all_phd_cont_female,
                    "count_all_phd_post":count_all_phd_post,
                    "count_all_phd_post_male":count_all_phd_post_male,
                    "count_all_phd_post_female":count_all_phd_post_female,
                    "count_all_phd_final":count_all_phd_final,
                    "count_all_phd_final_male":count_all_phd_final_male,
                    "count_all_phd_final_female":count_all_phd_final_female,
                    "forms":form,
                    "start_date":start_date,
                    "end_date":end_date
                    }
                    return render(request, templates, context)
                elif status == complete:
                    get_all_phd_student_by_start_date_end_date_cmp=Student.objects.filter(education_level="PHD",start_date=start_date, end_date=end_date, student_status=complete)
                    templates="account/phd.html"
                    context={
                    "get_all_phd_student_by_start_date_end_date_cmp":get_all_phd_student_by_start_date_end_date_cmp,
                    "count_all_phd":count_all_phd,
                    "count_all_phd_male":count_all_phd_male,
                    "count_all_phd_female":count_all_phd_female,
                    "count_all_phd_comp":count_all_phd_comp,
                    "count_all_phd_comp_male":count_all_phd_comp_male,
                    "count_all_phd_comp_female":count_all_phd_comp_female,
                    "count_all_phd_cont":count_all_phd_cont,
                    "count_all_phd_cont_male":count_all_phd_cont_male,
                    "count_all_phd_cont_female":count_all_phd_cont_female,
                    "count_all_phd_post":count_all_phd_post,
                    "count_all_phd_post_male":count_all_phd_post_male,
                    "count_all_phd_post_female":count_all_phd_post_female,
                    "count_all_phd_final":count_all_phd_final,
                    "count_all_phd_final_male":count_all_phd_final_male,
                    "count_all_phd_final_female":count_all_phd_final_female,
                    "forms":form,
                    "start_date":start_date,
                    "end_date":end_date
                    }
                    return render(request, templates, context)
                else:
                    get_all_phd_student_by_start_date_end_date_fnl=Student.objects.filter(education_level="PHD",start_date=start_date, end_date=end_date, student_status=final)
                    templates="account/phd.html"
                    context={
                    "get_all_phd_student_by_start_date_end_date_fnl":get_all_phd_student_by_start_date_end_date_fnl,
                    "count_all_phd":count_all_phd,
                    "count_all_phd_male":count_all_phd_male,
                    "count_all_phd_female":count_all_phd_female,
                    "count_all_phd_comp":count_all_phd_comp,
                    "count_all_phd_comp_male":count_all_phd_comp_male,
                    "count_all_phd_comp_female":count_all_phd_comp_female,
                    "count_all_phd_cont":count_all_phd_cont,
                    "count_all_phd_cont_male":count_all_phd_cont_male,
                    "count_all_phd_cont_female":count_all_phd_cont_female,
                    "count_all_phd_post":count_all_phd_post,
                    "count_all_phd_post_male":count_all_phd_post_male,
                    "count_all_phd_post_female":count_all_phd_post_female,
                    "count_all_phd_final":count_all_phd_final,
                    "count_all_phd_final_male":count_all_phd_final_male,
                    "count_all_phd_final_female":count_all_phd_final_female,
                    "forms":form,
                    "start_date":start_date,
                    "end_date":end_date
                    }
                    return render(request, templates, context)
            ################### quoter selections #########################
            elif gender and start_date and end_date and status:
                if gender == male:
                    if status == continuous:
                        get_all_phd_student_by_start_date_end_date_cnt_male=Student.objects.filter(education_level="PHD",start_date=start_date, end_date=end_date, student_status=continuous, gender=male)
                        templates="account/phd.html"
                        context={
                        "get_all_phd_student_by_start_date_end_date_cnt_male":get_all_phd_student_by_start_date_end_date_cnt_male,
                        "count_all_phd":count_all_phd,
                        "count_all_phd_male":count_all_phd_male,
                        "count_all_phd_female":count_all_phd_female,
                        "count_all_phd_comp":count_all_phd_comp,
                        "count_all_phd_comp_male":count_all_phd_comp_male,
                        "count_all_phd_comp_female":count_all_phd_comp_female,
                        "count_all_phd_cont":count_all_phd_cont,
                        "count_all_phd_cont_male":count_all_phd_cont_male,
                        "count_all_phd_cont_female":count_all_phd_cont_female,
                        "count_all_phd_post":count_all_phd_post,
                        "count_all_phd_post_male":count_all_phd_post_male,
                        "count_all_phd_post_female":count_all_phd_post_female,
                        "count_all_phd_final":count_all_phd_final,
                        "count_all_phd_final_male":count_all_phd_final_male,
                        "count_all_phd_final_female":count_all_phd_final_female,
                        "forms":form,
                        "start_date":start_date,
                        "end_date":end_date
                        }
                        return render(request, templates, context)
                    elif status == postpone:
                        get_all_phd_student_by_start_date_end_date_pst_male=Student.objects.filter(education_level="PHD",start_date=start_date, end_date=end_date, student_status=postpone, gender=male)
                        templates="account/phd.html"
                        context={
                        "get_all_phd_student_by_start_date_end_date_pst_male":get_all_phd_student_by_start_date_end_date_pst_male,
                        "count_all_phd":count_all_phd,
                        "count_all_phd_male":count_all_phd_male,
                        "count_all_phd_female":count_all_phd_female,
                        "count_all_phd_comp":count_all_phd_comp,
                        "count_all_phd_comp_male":count_all_phd_comp_male,
                        "count_all_phd_comp_female":count_all_phd_comp_female,
                        "count_all_phd_cont":count_all_phd_cont,
                        "count_all_phd_cont_male":count_all_phd_cont_male,
                        "count_all_phd_cont_female":count_all_phd_cont_female,
                        "count_all_phd_post":count_all_phd_post,
                        "count_all_phd_post_male":count_all_phd_post_male,
                        "count_all_phd_post_female":count_all_phd_post_female,
                        "count_all_phd_final":count_all_phd_final,
                        "count_all_phd_final_male":count_all_phd_final_male,
                        "count_all_phd_final_female":count_all_phd_final_female,
                        "forms":form,
                        "start_date":start_date,
                        "end_date":end_date
                        }
                        return render(request, templates, context)
                    elif status == complete:
                        get_all_phd_student_by_start_date_end_date_cmp_male=Student.objects.filter(education_level="PHD",start_date=start_date, end_date=end_date, student_status=complete, gender=male)
                        templates="account/phd.html"
                        context={
                        "get_all_phd_student_by_start_date_end_date_cmp_male":get_all_phd_student_by_start_date_end_date_cmp_male,
                        "count_all_phd":count_all_phd,
                        "count_all_phd_male":count_all_phd_male,
                        "count_all_phd_female":count_all_phd_female,
                        "count_all_phd_comp":count_all_phd_comp,
                        "count_all_phd_comp_male":count_all_phd_comp_male,
                        "count_all_phd_comp_female":count_all_phd_comp_female,
                        "count_all_phd_cont":count_all_phd_cont,
                        "count_all_phd_cont_male":count_all_phd_cont_male,
                        "count_all_phd_cont_female":count_all_phd_cont_female,
                        "count_all_phd_post":count_all_phd_post,
                        "count_all_phd_post_male":count_all_phd_post_male,
                        "count_all_phd_post_female":count_all_phd_post_female,
                        "count_all_phd_final":count_all_phd_final,
                        "count_all_phd_final_male":count_all_phd_final_male,
                        "count_all_phd_final_female":count_all_phd_final_female,
                        "forms":form,
                        "start_date":start_date,
                        "end_date":end_date
                        }
                        return render(request, templates, context)
                    else:
                        get_all_phd_student_by_start_date_end_date_fnl_male=Student.objects.filter(education_level="PHD",start_date=start_date, end_date=end_date, student_status=final, gender=male)
                        templates="account/phd.html"
                        context={
                        "get_all_phd_student_by_start_date_end_date_fnl_male":get_all_phd_student_by_start_date_end_date_fnl_male,
                        "count_all_phd":count_all_phd,
                        "count_all_phd_male":count_all_phd_male,
                        "count_all_phd_female":count_all_phd_female,
                        "count_all_phd_comp":count_all_phd_comp,
                        "count_all_phd_comp_male":count_all_phd_comp_male,
                        "count_all_phd_comp_female":count_all_phd_comp_female,
                        "count_all_phd_cont":count_all_phd_cont,
                        "count_all_phd_cont_male":count_all_phd_cont_male,
                        "count_all_phd_cont_female":count_all_phd_cont_female,
                        "count_all_phd_post":count_all_phd_post,
                        "count_all_phd_post_male":count_all_phd_post_male,
                        "count_all_phd_post_female":count_all_phd_post_female,
                        "count_all_phd_final":count_all_phd_final,
                        "count_all_phd_final_male":count_all_phd_final_male,
                        "count_all_phd_final_female":count_all_phd_final_female,
                        "forms":form,
                        "start_date":start_date,
                        "end_date":end_date
                        }
                        return render(request, templates, context)
                else:
                     if status == continuous:
                        get_all_phd_student_by_start_date_end_date_cnt_female=Student.objects.filter(education_level="PHD",start_date=start_date, end_date=end_date, student_status=continuous, gender=female)
                        templates="account/phd.html"
                        context={
                        "get_all_phd_student_by_start_date_end_date_cnt_female":get_all_phd_student_by_start_date_end_date_cnt_female,
                        "count_all_phd":count_all_phd,
                        "count_all_phd_male":count_all_phd_male,
                        "count_all_phd_female":count_all_phd_female,
                        "count_all_phd_comp":count_all_phd_comp,
                        "count_all_phd_comp_male":count_all_phd_comp_male,
                        "count_all_phd_comp_female":count_all_phd_comp_female,
                        "count_all_phd_cont":count_all_phd_cont,
                        "count_all_phd_cont_male":count_all_phd_cont_male,
                        "count_all_phd_cont_female":count_all_phd_cont_female,
                        "count_all_phd_post":count_all_phd_post,
                        "count_all_phd_post_male":count_all_phd_post_male,
                        "count_all_phd_post_female":count_all_phd_post_female,
                        "count_all_phd_final":count_all_phd_final,
                        "count_all_phd_final_male":count_all_phd_final_male,
                        "count_all_phd_final_female":count_all_phd_final_female,
                        "forms":form,
                        "start_date":start_date,
                        "end_date":end_date
                        }
                        return render(request, templates, context)
                     elif status == postpone:
                        get_all_phd_student_by_start_date_end_date_pst_female=Student.objects.filter(education_level="PHD",start_date=start_date, end_date=end_date, student_status=postpone, gender=female)
                        templates="account/phd.html"
                        context={
                        "get_all_phd_student_by_start_date_end_date_pst_female":get_all_phd_student_by_start_date_end_date_pst_female,
                        "count_all_phd":count_all_phd,
                        "count_all_phd_male":count_all_phd_male,
                        "count_all_phd_female":count_all_phd_female,
                        "count_all_phd_comp":count_all_phd_comp,
                        "count_all_phd_comp_male":count_all_phd_comp_male,
                        "count_all_phd_comp_female":count_all_phd_comp_female,
                        "count_all_phd_cont":count_all_phd_cont,
                        "count_all_phd_cont_male":count_all_phd_cont_male,
                        "count_all_phd_cont_female":count_all_phd_cont_female,
                        "count_all_phd_post":count_all_phd_post,
                        "count_all_phd_post_male":count_all_phd_post_male,
                        "count_all_phd_post_female":count_all_phd_post_female,
                        "count_all_phd_final":count_all_phd_final,
                        "count_all_phd_final_male":count_all_phd_final_male,
                        "count_all_phd_final_female":count_all_phd_final_female,
                        "forms":form,
                        "start_date":start_date,
                        "end_date":end_date
                        }
                        return render(request, templates, context)
                     elif status == complete:
                        get_all_phd_student_by_start_date_end_date_cmp_female=Student.objects.filter(education_level="PHD",start_date=start_date, end_date=end_date, student_status=complete, gender=female)
                        templates="account/phd.html"
                        context={
                        "get_all_phd_student_by_start_date_end_date_cmp_female":get_all_phd_student_by_start_date_end_date_cmp_female,
                        "count_all_phd":count_all_phd,
                        "count_all_phd_male":count_all_phd_male,
                        "count_all_phd_female":count_all_phd_female,
                        "count_all_phd_comp":count_all_phd_comp,
                        "count_all_phd_comp_male":count_all_phd_comp_male,
                        "count_all_phd_comp_female":count_all_phd_comp_female,
                        "count_all_phd_cont":count_all_phd_cont,
                        "count_all_phd_cont_male":count_all_phd_cont_male,
                        "count_all_phd_cont_female":count_all_phd_cont_female,
                        "count_all_phd_post":count_all_phd_post,
                        "count_all_phd_post_male":count_all_phd_post_male,
                        "count_all_phd_post_female":count_all_phd_post_female,
                        "count_all_phd_final":count_all_phd_final,
                        "count_all_phd_final_male":count_all_phd_final_male,
                        "count_all_phd_final_female":count_all_phd_final_female,
                        "forms":form,
                        "start_date":start_date,
                        "end_date":end_date
                        }
                        return render(request, templates, context)
                     else:
                            get_all_phd_student_by_start_date_end_date_fnl_female=Student.objects.filter(education_level="PHD",start_date=start_date, end_date=end_date, student_status=final, gender=female)
                            templates="account/phd.html"
                            context={
                            "get_all_phd_student_by_start_date_end_date_fnl_female":get_all_phd_student_by_start_date_end_date_fnl_female,
                            "count_all_phd":count_all_phd,
                            "count_all_phd_male":count_all_phd_male,
                            "count_all_phd_female":count_all_phd_female,
                            "count_all_phd_comp":count_all_phd_comp,
                            "count_all_phd_comp_male":count_all_phd_comp_male,
                            "count_all_phd_comp_female":count_all_phd_comp_female,
                            "count_all_phd_cont":count_all_phd_cont,
                            "count_all_phd_cont_male":count_all_phd_cont_male,
                            "count_all_phd_cont_female":count_all_phd_cont_female,
                            "count_all_phd_post":count_all_phd_post,
                            "count_all_phd_post_male":count_all_phd_post_male,
                            "count_all_phd_post_female":count_all_phd_post_female,
                            "count_all_phd_final":count_all_phd_final,
                            "count_all_phd_final_male":count_all_phd_final_male,
                            "count_all_phd_final_female":count_all_phd_final_female,
                            "forms":form,
                            "start_date":start_date,
                            "end_date":end_date
                            }
                            return render(request, templates, context)
        except:
            return HttpResponse("Please Enter valid data")
    else:
        time = datetime.datetime.now()
        get_time = time.strftime("%c")
        templates = 'account/phd.html'
        context = {
        "get_time":get_time,
        "get_college":get_college,
        "get_all_phd_student":get_all_phd_student[:10],
        "count_all_phd":count_all_phd,
        "count_all_phd_male":count_all_phd_male,
        "count_all_phd_female":count_all_phd_female,
        "count_all_phd_comp":count_all_phd_comp,
        "count_all_phd_comp_male":count_all_phd_comp_male,
        "count_all_phd_comp_female":count_all_phd_comp_female,
        "count_all_phd_cont":count_all_phd_cont,
        "count_all_phd_cont_male":count_all_phd_cont_male,
        "count_all_phd_cont_female":count_all_phd_cont_female,
        "count_all_phd_post":count_all_phd_post,
        "count_all_phd_post_male":count_all_phd_post_male,
        "count_all_phd_post_female":count_all_phd_post_female,
        "count_all_phd_final":count_all_phd_final,
        "count_all_phd_final_male":count_all_phd_final_male,
        "count_all_phd_final_female":count_all_phd_final_female,
        "forms":form
        }
        return render(request, templates, context)


@cache_control(no_cache=True, must_revalidate=True, privacy=True, no_store=False)
@login_required(login_url='auth')
def MastersView(request):
    form = CreateStudentForm()
    get_college = College.objects.all().order_by('-id')
    get_all_master_student = Student.objects.filter(education_level='MASTERS').order_by('-id')
    count_all_master = Student.objects.filter(education_level='MASTERS').count()
    count_all_master_male = Student.objects.filter(education_level='MASTERS', gender='Male').count()
    count_all_master_female = Student.objects.filter(education_level='MASTERS', gender='Female').count()

    ########## COMPLETED STUDENTS
    count_all_master_comp = Student.objects.filter(education_level='MASTERS',student_status='complete').count()
    count_all_master_comp_male = Student.objects.filter(education_level='MASTERS', gender='Male', student_status='complete').count()
    count_all_master_comp_female = Student.objects.filter(education_level='MASTERS', gender='Female', student_status='complete').count()

    ########## CONTINUOUS STUDENTS NOT WORKING
    count_all_master_cont = Student.objects.filter(education_level='MASTERS',student_status='continuous').count()
    count_all_master_cont_male = Student.objects.filter(education_level='MASTERS',student_status='continuous', gender='Male').count()
    count_all_master_cont_female = Student.objects.filter(education_level='MASTERS',student_status='continuous', gender='Female').count()

    ########## POSTPONED STUDENTS
    count_all_master_post = Student.objects.filter(education_level='MASTERS',student_status='postpone').count()
    count_all_master_post_male = Student.objects.filter(education_level='MASTERS',student_status='postpone', gender='Male').count()
    count_all_master_post_female = Student.objects.filter(education_level='MASTERS',student_status='postpone', gender='Female').count()

    ######### FINALIST s
    count_all_master_final = Student.objects.filter(education_level='MASTERS',student_status='final').count()
    count_all_master_final_male = Student.objects.filter(education_level='MASTERS',student_status='final', gender='Male').count()
    count_all_master_final_female = Student.objects.filter(education_level='MASTERS',student_status='final', gender='Female').count()
    if request.method =="POST":
        male="Male"
        female="Female"
        continuous="continuous"
        postpone="postpone"
        complete="complete"
        final="final"
        form=CreateStudentForm()
        try:
            gender=request.POST.get("gender")
            start_date=request.POST.get("start_date")
            end_date=request.POST.get("end_date")
            status=request.POST.get("student_status")
            ######################### empty  selection retrun all phd std #######################
            if gender =='' and start_date == '' and end_date == '' and status =='':
                get_all_master_student=Student.objects.filter(education_level="MASTERS")
                time = datetime.datetime.now()
                get_time = time.strftime("%c")
                templates = 'account/masters.html'
                context = {
                "get_time":get_time,
                "get_college":get_college,
                "get_student":get_all_master_student[:10],
                "count_all_masters":count_all_master,
                "count_all_masters_male":count_all_master_male,
                "count_all_masters_female":count_all_master_female,
                "count_all_masters_comp":count_all_master_comp,
                "count_all_masters_comp_male":count_all_master_comp_male,
                "count_all_masters_comp_female":count_all_master_comp_female,
                "count_all_masters_cont":count_all_master_cont,
                "count_all_masters_cont_male":count_all_master_cont_male,
                "count_all_masters_cont_female":count_all_master_cont_female,
                "count_all_masters_post":count_all_master_post,
                "count_all_masters_post_male":count_all_master_post_male,
                "count_all_masters_post_female":count_all_master_post_female,
                "count_all_masters_final":count_all_master_final,
                "count_all_masters_final_male":count_all_master_final_male,
                "count_all_masters_final_female":count_all_master_final_female,
                "forms":form
                }
                return render(request, templates, context)
            #######################  single selections #######################
            elif gender and start_date == '' and end_date == '' and status =='':
                if gender =="Male":
                    get_all_masters_student_male=Student.objects.filter(education_level="MASTERS", gender="Male")
                    time = datetime.datetime.now()
                    get_time = time.strftime("%c")
                    templates = 'account/masters.html'
                    context = {
                    "get_time":get_time,
                    "get_college":get_college,
                    "get_all_masters_student_male":get_all_masters_student_male[:10],
                    "count_all_masters":count_all_master,
                    "count_all_masters_male":count_all_master_male,
                    "count_all_masters_female":count_all_master_female,
                    "count_all_masters_comp":count_all_master_comp,
                    "count_all_masters_comp_male":count_all_master_comp_male,
                    "count_all_masters_comp_female":count_all_master_comp_female,
                    "count_all_masters_cont":count_all_master_cont,
                    "count_all_masters_cont_male":count_all_master_cont_male,
                    "count_all_masters_cont_female":count_all_master_cont_female,
                    "count_all_masters_post":count_all_master_post,
                    "count_all_masters_post_male":count_all_master_post_male,
                    "count_all_masters_post_female":count_all_master_post_female,
                    "count_all_masters_final":count_all_master_final,
                    "count_all_masters_final_male":count_all_master_final_male,
                    "count_all_masters_final_female":count_all_master_final_female,
                    "forms":form
                    }
                    return render(request, templates, context)
                else:
                    get_all_masters_student_female=Student.objects.filter(education_level="MASTERS", gender="Female")
                    time = datetime.datetime.now()
                    get_time = time.strftime("%c")
                    templates = 'account/masters.html'
                    context = {
                    "get_time":get_time,
                    "get_college":get_college,
                    "get_all_masters_student_female":get_all_masters_student_female,
                    "count_all_masters":count_all_master,
                    "count_all_masters_male":count_all_master_male,
                    "count_all_masters_female":count_all_master_female,
                    "count_all_masters_comp":count_all_master_comp,
                    "count_all_masters_comp_male":count_all_master_comp_male,
                    "count_all_masters_comp_female":count_all_master_comp_female,
                    "count_all_masters_cont":count_all_master_cont,
                    "count_all_masters_cont_male":count_all_master_cont_male,
                    "count_all_masters_cont_female":count_all_master_cont_female,
                    "count_all_masters_post":count_all_master_post,
                    "count_all_masters_post_male":count_all_master_post_male,
                    "count_all_masters_post_female":count_all_master_post_female,
                    "count_all_masters_final":count_all_master_final,
                    "count_all_masters_final_male":count_all_master_final_male,
                    "count_all_masters_final_female":count_all_master_final_female,
                    "forms":form
                    }
                    return render(request, templates, context)

            elif gender == '' and start_date and end_date == '' and status =='':
                get_all_masters_student_by_start_date=Student.objects.filter(education_level="MASTERS", start_date=str(start_date))
                time = datetime.datetime.now()
                get_time = time.strftime("%c")
                templates = 'account/masters.html'
                context = {
                "get_time":get_time,
                "get_college":get_college,
                "get_all_masters_student_by_start_date":get_all_masters_student_by_start_date,
                "count_all_masters":count_all_master,
                "count_all_masters_male":count_all_master_male,
                "count_all_masters_female":count_all_master_female,
                "count_all_masters_comp":count_all_master_comp,
                "count_all_masters_comp_male":count_all_master_comp_male,
                "count_all_masters_comp_female":count_all_master_comp_female,
                "count_all_masters_cont":count_all_master_cont,
                "count_all_masters_cont_male":count_all_master_cont_male,
                "count_all_masters_cont_female":count_all_master_cont_female,
                "count_all_masters_post":count_all_master_post,
                "count_all_masters_post_male":count_all_master_post_male,
                "count_all_masters_post_female":count_all_master_post_female,
                "count_all_masters_final":count_all_master_final,
                "count_all_masters_final_male":count_all_master_final_male,
                "count_all_masters_final_female":count_all_master_final_female,
                "forms":form,
                "start_date":start_date
                }
                return render(request, templates, context)
            elif gender == '' and start_date ==''  and end_date and status =='':
                get_all_masters_student_by_end_date=Student.objects.filter(education_level="MASTERS", end_date=str(end_date))
                time = datetime.datetime.now()
                get_time = time.strftime("%c")
                templates = 'account/masters.html'
                context = {
                "get_time":get_time,
                "get_college":get_college,
                "get_all_masters_student_by_end_date":get_all_masters_student_by_end_date,
                "count_all_masters":count_all_master,
                "count_all_masters_male":count_all_master_male,
                "count_all_masters_female":count_all_master_female,
                "count_all_masters_comp":count_all_master_comp,
                "count_all_masters_comp_male":count_all_master_comp_male,
                "count_all_masters_comp_female":count_all_master_comp_female,
                "count_all_masters_cont":count_all_master_cont,
                "count_all_masters_cont_male":count_all_master_cont_male,
                "count_all_masters_cont_female":count_all_master_cont_female,
                "count_all_masters_post":count_all_master_post,
                "count_all_masters_post_male":count_all_master_post_male,
                "count_all_masters_post_female":count_all_master_post_female,
                "count_all_masters_final":count_all_master_final,
                "count_all_masters_final_male":count_all_master_final_male,
                "count_all_masters_final_female":count_all_master_final_female,
                "forms":form,
                "end_date": end_date,
                "end_date": end_date
                }
                return render(request, templates, context)
            elif gender =='' and start_date =='' and end_date == '' and status:
                if status == continuous:
                    get_all_masters_student_continuous=Student.objects.filter(education_level="MASTERS", student_status="continuous")
                    time = datetime.datetime.now()
                    get_time = time.strftime("%c")
                    templates = 'account/masters.html'
                    context = {
                    "get_time":get_time,
                    "get_college":get_college,
                    "get_all_masters_student_continuous":get_all_masters_student_continuous,
                    "count_all_masters":count_all_master,
                    "count_all_masters_male":count_all_master_male,
                    "count_all_masters_female":count_all_master_female,
                    "count_all_masters_comp":count_all_master_comp,
                    "count_all_masters_comp_male":count_all_master_comp_male,
                    "count_all_masters_comp_female":count_all_master_comp_female,
                    "count_all_masters_cont":count_all_master_cont,
                    "count_all_masters_cont_male":count_all_master_cont_male,
                    "count_all_masters_cont_female":count_all_master_cont_female,
                    "count_all_masters_post":count_all_master_post,
                    "count_all_masters_post_male":count_all_master_post_male,
                    "count_all_masters_post_female":count_all_master_post_female,
                    "count_all_masters_final":count_all_master_final,
                    "count_all_masters_final_male":count_all_master_final_male,
                    "count_all_masters_final_female":count_all_master_final_female,
                    "forms":form,
                    "start_date": start_date,
                    "end_date": end_date
                    }
                    return render(request, templates, context)
                elif status == postpone:
                    get_all_masters_student_postpone=Student.objects.filter(education_level="MASTERS", student_status="postpone")
                    time = datetime.datetime.now()
                    get_time = time.strftime("%c")
                    templates = 'account/masters.html'
                    context = {
                    "get_time":get_time,
                    "get_college":get_college,
                    "get_all_masters_student_postpone":get_all_masters_student_postpone,
                    "count_all_masters":count_all_master,
                    "count_all_masters_male":count_all_master_male,
                    "count_all_masters_female":count_all_master_female,
                    "count_all_masters_comp":count_all_master_comp,
                    "count_all_masters_comp_male":count_all_master_comp_male,
                    "count_all_masters_comp_female":count_all_master_comp_female,
                    "count_all_masters_cont":count_all_master_cont,
                    "count_all_masters_cont_male":count_all_master_cont_male,
                    "count_all_masters_cont_female":count_all_master_cont_female,
                    "count_all_masters_post":count_all_master_post,
                    "count_all_masters_post_male":count_all_master_post_male,
                    "count_all_masters_post_female":count_all_master_post_female,
                    "count_all_masters_final":count_all_master_final,
                    "count_all_masters_final_male":count_all_master_final_male,
                    "count_all_masters_final_female":count_all_master_final_female,
                    "forms":form,
                    "start_date": start_date,
                    "end_date": end_date
                    }
                    return render(request, templates, context)
                elif status == complete:
                    get_all_masters_student_complete=Student.objects.filter(education_level="MASTERS", student_status=complete)
                    time = datetime.datetime.now()
                    get_time = time.strftime("%c")
                    templates = 'account/masters.html'
                    context = {
                    "get_time":get_time,
                    "get_college":get_college,
                    "get_all_masters_student_complete":get_all_masters_student_complete,
                    "count_all_masters":count_all_master,
                    "count_all_masters_male":count_all_master_male,
                    "count_all_masters_female":count_all_master_female,
                    "count_all_masters_comp":count_all_master_comp,
                    "count_all_masters_comp_male":count_all_master_comp_male,
                    "count_all_masters_comp_female":count_all_master_comp_female,
                    "count_all_masters_cont":count_all_master_cont,
                    "count_all_masters_cont_male":count_all_master_cont_male,
                    "count_all_masters_cont_female":count_all_master_cont_female,
                    "count_all_masters_post":count_all_master_post,
                    "count_all_masters_post_male":count_all_master_post_male,
                    "count_all_masters_post_female":count_all_master_post_female,
                    "count_all_masters_final":count_all_master_final,
                    "count_all_masters_final_male":count_all_master_final_male,
                    "count_all_masters_final_female":count_all_master_final_female,
                    "forms":form,
                    "start_date": start_date,
                    "end_date": end_date
                    }
                    return render(request, templates, context)
                else:
                    get_all_masters_student_final=Student.objects.filter(education_level="MASTERS", student_status=final)
                    time = datetime.datetime.now()
                    get_time = time.strftime("%c")
                    templates = 'account/masters.html'
                    context = {
                    "get_time":get_time,
                    "get_college":get_college,
                    "get_all_masters_student_final":get_all_masters_student_final,
                    "count_all_masters":count_all_master,
                    "count_all_masters_male":count_all_master_male,
                    "count_all_masters_female":count_all_master_female,
                    "count_all_masters_comp":count_all_master_comp,
                    "count_all_masters_comp_male":count_all_master_comp_male,
                    "count_all_masters_comp_female":count_all_master_comp_female,
                    "count_all_masters_cont":count_all_master_cont,
                    "count_all_masters_cont_male":count_all_master_cont_male,
                    "count_all_masters_cont_female":count_all_master_cont_female,
                    "count_all_masters_post":count_all_master_post,
                    "count_all_masters_post_male":count_all_master_post_male,
                    "count_all_masters_post_female":count_all_master_post_female,
                    "count_all_masters_final":count_all_master_final,
                    "count_all_masters_final_male":count_all_master_final_male,
                    "count_all_masters_final_female":count_all_master_final_female,
                    "forms":form,
                    "start_date": start_date,
                    "end_date": end_date
                    }
                    return render(request, templates, context)
            ################## two selection #################################
            elif gender and start_date and end_date=='' and status=='':
                if gender == male:
                    get_all_masters_student_male_start_date=Student.objects.filter(education_level="MASTERS", gender=male, start_date=str(start_date))
                    time = datetime.datetime.now()
                    get_time = time.strftime("%c")
                    templates = 'account/masters.html'
                    context = {
                    "get_time":get_time,
                    "get_college":get_college,
                    "get_all_masters_student_male_start_date":get_all_masters_student_male_start_date,
                    "count_all_masters":count_all_master,
                    "count_all_masters_male":count_all_master_male,
                    "count_all_masters_female":count_all_master_female,
                    "count_all_masters_comp":count_all_master_comp,
                    "count_all_masters_comp_male":count_all_master_comp_male,
                    "count_all_masters_comp_female":count_all_master_comp_female,
                    "count_all_masters_cont":count_all_master_cont,
                    "count_all_masters_cont_male":count_all_master_cont_male,
                    "count_all_masters_cont_female":count_all_master_cont_female,
                    "count_all_masters_post":count_all_master_post,
                    "count_all_masters_post_male":count_all_master_post_male,
                    "count_all_masters_post_female":count_all_master_post_female,
                    "count_all_masters_final":count_all_master_final,
                    "count_all_masters_final_male":count_all_master_final_male,
                    "count_all_masters_final_female":count_all_master_final_female,
                    "forms":form,
                    "start_date": start_date,
                    "end_date": end_date
                    }
                    return render(request, templates, context)
                else:
                    get_all_masters_student_female_start_date=Student.objects.filter(education_level="MASTERS", gender=female, start_date=str(start_date))
                    time = datetime.datetime.now()
                    get_time = time.strftime("%c")
                    templates = 'account/masters.html'
                    context = {
                    "get_time":get_time,
                    "get_college":get_college,
                    "get_all_masters_student_female_start_date":get_all_masters_student_female_start_date,
                    "count_all_masters":count_all_master,
                    "count_all_masters_male":count_all_master_male,
                    "count_all_masters_female":count_all_master_female,
                    "count_all_masters_comp":count_all_master_comp,
                    "count_all_masters_comp_male":count_all_master_comp_male,
                    "count_all_masters_comp_female":count_all_master_comp_female,
                    "count_all_masters_cont":count_all_master_cont,
                    "count_all_masters_cont_male":count_all_master_cont_male,
                    "count_all_masters_cont_female":count_all_master_cont_female,
                    "count_all_masters_post":count_all_master_post,
                    "count_all_masters_post_male":count_all_master_post_male,
                    "count_all_masters_post_female":count_all_master_post_female,
                    "count_all_masters_final":count_all_master_final,
                    "count_all_masters_final_male":count_all_master_final_male,
                    "count_all_masters_final_female":count_all_master_final_female,
                    "forms":form,
                    "start_date": start_date,
                    "end_date": end_date
                    }
                    return render(request, templates, context)

            elif gender and start_date == '' and end_date and status =='':
                if gender == male:
                    get_all_masters_student_male_end_date=Student.objects.filter(education_level="MASTERS", gender=male, end_date=str(end_date))
                    time = datetime.datetime.now()
                    get_time = time.strftime("%c")
                    templates = 'account/masters.html'
                    context = {
                    "get_time":get_time,
                    "get_college":get_college,
                    "get_all_masters_student_male_end_date":get_all_masters_student_male_end_date,
                    "count_all_masters":count_all_master,
                    "count_all_masters_male":count_all_master_male,
                    "count_all_masters_female":count_all_master_female,
                    "count_all_masters_comp":count_all_master_comp,
                    "count_all_masters_comp_male":count_all_master_comp_male,
                    "count_all_masters_comp_female":count_all_master_comp_female,
                    "count_all_masters_cont":count_all_master_cont,
                    "count_all_masters_cont_male":count_all_master_cont_male,
                    "count_all_masters_cont_female":count_all_master_cont_female,
                    "count_all_masters_post":count_all_master_post,
                    "count_all_masters_post_male":count_all_master_post_male,
                    "count_all_masters_post_female":count_all_master_post_female,
                    "count_all_masters_final":count_all_master_final,
                    "count_all_masters_final_male":count_all_master_final_male,
                    "count_all_masters_final_female":count_all_master_final_female,
                    "forms":form,
                    "start_date": start_date,
                    "end_date": end_date
                    }
                    return render(request, templates, context)
                else:
                    get_all_masters_student_female_end_date=Student.objects.filter(education_level="MASTERS", gender=female, end_date=str(end_date))
                    time = datetime.datetime.now()
                    get_time = time.strftime("%c")
                    templates = 'account/masters.html'
                    context = {
                    "get_time":get_time,
                    "get_college":get_college,
                    "get_all_masters_student_female_end_date":get_all_masters_student_female_end_date,
                    "count_all_masters":count_all_master,
                    "count_all_masters_male":count_all_master_male,
                    "count_all_masters_female":count_all_master_female,
                    "count_all_masters_comp":count_all_master_comp,
                    "count_all_masters_comp_male":count_all_master_comp_male,
                    "count_all_masters_comp_female":count_all_master_comp_female,
                    "count_all_masters_cont":count_all_master_cont,
                    "count_all_masters_cont_male":count_all_master_cont_male,
                    "count_all_masters_cont_female":count_all_master_cont_female,
                    "count_all_masters_post":count_all_master_post,
                    "count_all_masters_post_male":count_all_master_post_male,
                    "count_all_masters_post_female":count_all_master_post_female,
                    "count_all_masters_final":count_all_master_final,
                    "count_all_masters_final_male":count_all_master_final_male,
                    "count_all_masters_final_female":count_all_master_final_female,
                    "forms":form,
                    "start_date": start_date,
                    "end_date": end_date
                    }
                    return render(request, templates, context)
 # ======================== anza hapa hapa =======================
            elif gender and start_date == '' and end_date =='' and status:
                if gender == male:
                    if status == continuous:
                        get_all_masters_student_continuous_male=Student.objects.filter(education_level="MASTERS", student_status=continuous, gender=male)
                        time = datetime.datetime.now()
                        get_time = time.strftime("%c")
                        templates = 'account/masters.html'
                        context = {
                        "get_time":get_time,
                        "get_college":get_college,
                        "get_all_masters_student_continuous_male":get_all_masters_student_continuous_male,
                        "count_all_masters":count_all_master,
                        "count_all_masters_male":count_all_master_male,
                        "count_all_masters_female":count_all_master_female,
                        "count_all_masters_comp":count_all_master_comp,
                        "count_all_masters_comp_male":count_all_master_comp_male,
                        "count_all_masters_comp_female":count_all_master_comp_female,
                        "count_all_masters_cont":count_all_master_cont,
                        "count_all_masters_cont_male":count_all_master_cont_male,
                        "count_all_masters_cont_female":count_all_master_cont_female,
                        "count_all_masters_post":count_all_master_post,
                        "count_all_masters_post_male":count_all_master_post_male,
                        "count_all_masters_post_female":count_all_master_post_female,
                        "count_all_masters_final":count_all_master_final,
                        "count_all_masters_final_male":count_all_master_final_male,
                        "count_all_masters_final_female":count_all_master_final_female,
                        "forms":form,
                        "start_date": start_date,
                        "end_date": end_date
                        }
                        return render(request, templates, context)
    # ===================  ENDELEAA NA HAP ======================
                    elif status == postpone:
                        get_all_masters_student_postpone_male=Student.objects.filter(education_level="MASTERS", student_status=postpone, gender=male)
                        time = datetime.datetime.now()
                        get_time = time.strftime("%c")
                        templates = 'account/masters.html'
                        context = {
                        "get_time":get_time,
                        "get_college":get_college,
                        "get_all_masters_student_postpone_male":get_all_masters_student_postpone_male,
                        "count_all_masters":count_all_master,
                        "count_all_masters_male":count_all_master_male,
                        "count_all_masters_female":count_all_master_female,
                        "count_all_masters_comp":count_all_master_comp,
                        "count_all_masters_comp_male":count_all_master_comp_male,
                        "count_all_masters_comp_female":count_all_master_comp_female,
                        "count_all_masters_cont":count_all_master_cont,
                        "count_all_masters_cont_male":count_all_master_cont_male,
                        "count_all_masters_cont_female":count_all_master_cont_female,
                        "count_all_masters_post":count_all_master_post,
                        "count_all_masters_post_male":count_all_master_post_male,
                        "count_all_masters_post_female":count_all_master_post_female,
                        "count_all_masters_final":count_all_master_final,
                        "count_all_masters_final_male":count_all_master_final_male,
                        "count_all_masters_final_female":count_all_master_final_female,
                        "forms":form,
                        "start_date": start_date,
                        "end_date": end_date
                        }
                        return render(request, templates, context)
                    elif status == complete:
                        get_all_masters_student_complete_male=Student.objects.filter(education_level="MASTERS", student_status=complete, gender=male)
                        time = datetime.datetime.now()
                        get_time = time.strftime("%c")
                        templates = 'account/masters.html'
                        context = {
                        "get_time":get_time,
                        "get_college":get_college,
                        "get_all_masters_student_complete_male":get_all_masters_student_complete_male,
                        "count_all_masters":count_all_master,
                        "count_all_masters_male":count_all_master_male,
                        "count_all_masters_female":count_all_master_female,
                        "count_all_masters_comp":count_all_master_comp,
                        "count_all_masters_comp_male":count_all_master_comp_male,
                        "count_all_masters_comp_female":count_all_master_comp_female,
                        "count_all_masters_cont":count_all_master_cont,
                        "count_all_masters_cont_male":count_all_master_cont_male,
                        "count_all_masters_cont_female":count_all_master_cont_female,
                        "count_all_masters_post":count_all_master_post,
                        "count_all_masters_post_male":count_all_master_post_male,
                        "count_all_masters_post_female":count_all_master_post_female,
                        "count_all_masters_final":count_all_master_final,
                        "count_all_masters_final_male":count_all_master_final_male,
                        "count_all_masters_final_female":count_all_master_final_female,
                        "forms":form,
                        "start_date": start_date,
                        "end_date": end_date
                        }
                        return render(request, templates, context)
                    else:
                        get_all_msters_student_final_male=Student.objects.filter(education_level="MASTERS", student_status=final, gender=male)
                        time = datetime.datetime.now()
                        get_time = time.strftime("%c")
                        templates = 'account/masters.html'
                        context = {
                        "get_time":get_time,
                        "get_college":get_college,
                        "get_all_msters_student_final_male":get_all_msters_student_final_male,
                        "count_all_masters":count_all_master,
                        "count_all_masters_male":count_all_master_male,
                        "count_all_masters_female":count_all_master_female,
                        "count_all_masters_comp":count_all_master_comp,
                        "count_all_masters_comp_male":count_all_master_comp_male,
                        "count_all_masters_comp_female":count_all_master_comp_female,
                        "count_all_masters_cont":count_all_master_cont,
                        "count_all_masters_cont_male":count_all_master_cont_male,
                        "count_all_masters_cont_female":count_all_master_cont_female,
                        "count_all_masters_post":count_all_master_post,
                        "count_all_masters_post_male":count_all_master_post_male,
                        "count_all_masters_post_female":count_all_master_post_female,
                        "count_all_masters_final":count_all_master_final,
                        "count_all_masters_final_male":count_all_master_final_male,
                        "count_all_masters_final_female":count_all_master_final_female,
                        "forms":form,
                        "start_date": start_date,
                        "end_date": end_date
                        }
                        return render(request, templates, context)
                else:
                    if status == continuous:
                        get_all_masters_student_continuous_female=Student.objects.filter(education_level="MASTERS", student_status=continuous, gender=female)
                        time = datetime.datetime.now()
                        get_time = time.strftime("%c")
                        templates = 'account/masters.html'
                        context = {
                        "get_time":get_time,
                        "get_college":get_college,
                        "get_all_masters_student_continuous_female":get_all_masters_student_continuous_female,
                        "count_all_masters":count_all_master,
                        "count_all_masters_male":count_all_master_male,
                        "count_all_masters_female":count_all_master_female,
                        "count_all_masters_comp":count_all_master_comp,
                        "count_all_masters_comp_male":count_all_master_comp_male,
                        "count_all_masters_comp_female":count_all_master_comp_female,
                        "count_all_masters_cont":count_all_master_cont,
                        "count_all_masters_cont_male":count_all_master_cont_male,
                        "count_all_masters_cont_female":count_all_master_cont_female,
                        "count_all_masters_post":count_all_master_post,
                        "count_all_masters_post_male":count_all_master_post_male,
                        "count_all_masters_post_female":count_all_master_post_female,
                        "count_all_masters_final":count_all_master_final,
                        "count_all_masters_final_male":count_all_master_final_male,
                        "count_all_masters_final_female":count_all_master_final_female,
                        "forms":form,
                        "start_date": start_date,
                        "end_date": end_date
                        }
                        return render(request, templates, context)
                    elif status == postpone:
                        get_all_masters_student_postpone_female=Student.objects.filter(education_level="MASTERS", student_status=postpone, gender=female)
                        time = datetime.datetime.now()
                        get_time = time.strftime("%c")
                        templates = 'account/masters.html'
                        context = {
                        "get_time":get_time,
                        "get_college":get_college,
                        "get_all_masters_student_postpone_female":get_all_masters_student_postpone_female,
                        "count_all_masters":count_all_master,
                        "count_all_masters_male":count_all_master_male,
                        "count_all_masters_female":count_all_master_female,
                        "count_all_masters_comp":count_all_master_comp,
                        "count_all_masters_comp_male":count_all_master_comp_male,
                        "count_all_masters_comp_female":count_all_master_comp_female,
                        "count_all_masters_cont":count_all_master_cont,
                        "count_all_masters_cont_male":count_all_master_cont_male,
                        "count_all_masters_cont_female":count_all_master_cont_female,
                        "count_all_masters_post":count_all_master_post,
                        "count_all_masters_post_male":count_all_master_post_male,
                        "count_all_masters_post_female":count_all_master_post_female,
                        "count_all_masters_final":count_all_master_final,
                        "count_all_masters_final_male":count_all_master_final_male,
                        "count_all_masters_final_female":count_all_master_final_female,
                        "forms":form,
                        "start_date": start_date,
                        "end_date": end_date
                        }
                        return render(request, templates, context)
                    elif status == complete:
                        get_all_masters_student_complete_female=Student.objects.filter(education_level="MASTERS", student_status=complete, gender=female)
                        time = datetime.datetime.now()
                        get_time = time.strftime("%c")
                        templates = 'account/masters.html'
                        context = {
                        "get_time":get_time,
                        "get_college":get_college,
                        "get_all_masters_student_complete_female":get_all_masters_student_complete_female,
                        "count_all_masters":count_all_master,
                        "count_all_masters_male":count_all_master_male,
                        "count_all_masters_female":count_all_master_female,
                        "count_all_masters_comp":count_all_master_comp,
                        "count_all_masters_comp_male":count_all_master_comp_male,
                        "count_all_masters_comp_female":count_all_master_comp_female,
                        "count_all_masters_cont":count_all_master_cont,
                        "count_all_masters_cont_male":count_all_master_cont_male,
                        "count_all_masters_cont_female":count_all_master_cont_female,
                        "count_all_masters_post":count_all_master_post,
                        "count_all_masters_post_male":count_all_master_post_male,
                        "count_all_masters_post_female":count_all_master_post_female,
                        "count_all_masters_final":count_all_master_final,
                        "count_all_masters_final_male":count_all_master_final_male,
                        "count_all_masters_final_female":count_all_master_final_female,
                        "forms":form,
                        "start_date": start_date,
                        "end_date": end_date
                        }
                        return render(request, templates, context)
                    else:
                        get_all_masters_student_final_female=Student.objects.filter(education_level="MASTERS", student_status=final, gender=female)
                        time = datetime.datetime.now()
                        get_time = time.strftime("%c")
                        templates = 'account/masters.html'
                        context = {
                        "get_time":get_time,
                        "get_college":get_college,
                        "get_all_masters_student_final_female":get_all_masters_student_final_female,
                        "count_all_masters":count_all_master,
                        "count_all_masters_male":count_all_master_male,
                        "count_all_masters_female":count_all_master_female,
                        "count_all_masters_comp":count_all_master_comp,
                        "count_all_masters_comp_male":count_all_master_comp_male,
                        "count_all_masters_comp_female":count_all_master_comp_female,
                        "count_all_masters_cont":count_all_master_cont,
                        "count_all_masters_cont_male":count_all_master_cont_male,
                        "count_all_masters_cont_female":count_all_master_cont_female,
                        "count_all_masters_post":count_all_master_post,
                        "count_all_masters_post_male":count_all_master_post_male,
                        "count_all_masters_post_female":count_all_master_post_female,
                        "count_all_masters_final":count_all_master_final,
                        "count_all_masters_final_male":count_all_master_final_male,
                        "count_all_masters_final_female":count_all_master_final_female,
                        "forms":form,
                        "start_date": start_date,
                        "end_date": end_date
                        }
                        return render(request, templates, context)
            elif gender == '' and start_date and end_date and status =='':
                get_all_masters_student_by_start_date_end_date=Student.objects.filter(education_level="MASTERS", start_date=start_date, end_date=end_date)
                time = datetime.datetime.now()
                get_time = time.strftime("%c")
                templates = 'account/masters.html'
                context = {
                "get_time":get_time,
                "get_college":get_college,
                "get_all_masters_student_by_start_date_end_date":get_all_masters_student_by_start_date_end_date,
                "count_all_masters":count_all_master,
                "count_all_masters_male":count_all_master_male,
                "count_all_masters_female":count_all_master_female,
                "count_all_masters_comp":count_all_master_comp,
                "count_all_masters_comp_male":count_all_master_comp_male,
                "count_all_masters_comp_female":count_all_master_comp_female,
                "count_all_masters_cont":count_all_master_cont,
                "count_all_masters_cont_male":count_all_master_cont_male,
                "count_all_masters_cont_female":count_all_master_cont_female,
                "count_all_masters_post":count_all_master_post,
                "count_all_masters_post_male":count_all_master_post_male,
                "count_all_masters_post_female":count_all_master_post_female,
                "count_all_masters_final":count_all_master_final,
                "count_all_masters_final_male":count_all_master_final_male,
                "count_all_masters_final_female":count_all_master_final_female,
                "forms":form,
                "start_date": start_date,
                "end_date": end_date
                }
                return render(request, templates, context)
            elif gender =='' and start_date and end_date =='' and status:
                if status == continuous:
                    get_all_masters_student_by_start_date_cnt=Student.objects.filter(education_level="MASTERS", start_date=start_date, student_status=continuous)
                    time = datetime.datetime.now()
                    get_time = time.strftime("%c")
                    templates = 'account/masters.html'
                    context = {
                    "get_time":get_time,
                    "get_college":get_college,
                    "get_all_masters_student_by_start_date_cnt":get_all_masters_student_by_start_date_cnt,
                    "count_all_masters":count_all_master,
                    "count_all_masters_male":count_all_master_male,
                    "count_all_masters_female":count_all_master_female,
                    "count_all_masters_comp":count_all_master_comp,
                    "count_all_masters_comp_male":count_all_master_comp_male,
                    "count_all_masters_comp_female":count_all_master_comp_female,
                    "count_all_masters_cont":count_all_master_cont,
                    "count_all_masters_cont_male":count_all_master_cont_male,
                    "count_all_masters_cont_female":count_all_master_cont_female,
                    "count_all_masters_post":count_all_master_post,
                    "count_all_masters_post_male":count_all_master_post_male,
                    "count_all_masters_post_female":count_all_master_post_female,
                    "count_all_masters_final":count_all_master_final,
                    "count_all_masters_final_male":count_all_master_final_male,
                    "count_all_masters_final_female":count_all_master_final_female,
                    "forms":form,
                    "start_date": start_date,
                    "end_date": end_date
                    }
                    return render(request, templates, context)
                elif status == postpone:
                    get_all_masters_student_by_start_date_pst=Student.objects.filter(education_level="MASTERS", start_date=start_date, student_status=postpone)
                    time = datetime.datetime.now()
                    get_time = time.strftime("%c")
                    templates = 'account/masters.html'
                    context = {
                    "get_time":get_time,
                    "get_college":get_college,
                    "get_all_masters_student_by_start_date_pst":get_all_masters_student_by_start_date_pst,
                    "count_all_masters":count_all_master,
                    "count_all_masters_male":count_all_master_male,
                    "count_all_masters_female":count_all_master_female,
                    "count_all_masters_comp":count_all_master_comp,
                    "count_all_masters_comp_male":count_all_master_comp_male,
                    "count_all_masters_comp_female":count_all_master_comp_female,
                    "count_all_masters_cont":count_all_master_cont,
                    "count_all_masters_cont_male":count_all_master_cont_male,
                    "count_all_masters_cont_female":count_all_master_cont_female,
                    "count_all_masters_post":count_all_master_post,
                    "count_all_masters_post_male":count_all_master_post_male,
                    "count_all_masters_post_female":count_all_master_post_female,
                    "count_all_masters_final":count_all_master_final,
                    "count_all_masters_final_male":count_all_master_final_male,
                    "count_all_masters_final_female":count_all_master_final_female,
                    "forms":form,
                    "start_date": start_date,
                    "end_date": end_date
                    }
                    return render(request, templates, context)
                elif status == complete:
                    get_all_masters_student_by_start_date_cmp=Student.objects.filter(education_level="MASTERS", start_date=start_date, student_status=complete)
                    time = datetime.datetime.now()
                    get_time = time.strftime("%c")
                    templates = 'account/masters.html'
                    context = {
                    "get_time":get_time,
                    "get_college":get_college,
                    "get_all_masters_student_by_start_date_cmp":get_all_masters_student_by_start_date_cmp,
                    "count_all_masters":count_all_master,
                    "count_all_masters_male":count_all_master_male,
                    "count_all_masters_female":count_all_master_female,
                    "count_all_masters_comp":count_all_master_comp,
                    "count_all_masters_comp_male":count_all_master_comp_male,
                    "count_all_masters_comp_female":count_all_master_comp_female,
                    "count_all_masters_cont":count_all_master_cont,
                    "count_all_masters_cont_male":count_all_master_cont_male,
                    "count_all_masters_cont_female":count_all_master_cont_female,
                    "count_all_masters_post":count_all_master_post,
                    "count_all_masters_post_male":count_all_master_post_male,
                    "count_all_masters_post_female":count_all_master_post_female,
                    "count_all_masters_final":count_all_master_final,
                    "count_all_masters_final_male":count_all_master_final_male,
                    "count_all_masters_final_female":count_all_master_final_female,
                    "forms":form,
                    "start_date": start_date,
                    "end_date": end_date
                    }
                    return render(request, templates, context)
                else:
                    get_all_masters_student_by_start_date_fnl=Student.objects.filter(education_level="MASTERS", start_date=start_date, student_status=final)
                    time = datetime.datetime.now()
                    get_time = time.strftime("%c")
                    templates = 'account/masters.html'
                    context = {
                    "get_time":get_time,
                    "get_college":get_college,
                    "get_all_masters_student_by_start_date_fnl":get_all_masters_student_by_start_date_fnl,
                    "count_all_masters":count_all_master,
                    "count_all_masters_male":count_all_master_male,
                    "count_all_masters_female":count_all_master_female,
                    "count_all_masters_comp":count_all_master_comp,
                    "count_all_masters_comp_male":count_all_master_comp_male,
                    "count_all_masters_comp_female":count_all_master_comp_female,
                    "count_all_masters_cont":count_all_master_cont,
                    "count_all_masters_cont_male":count_all_master_cont_male,
                    "count_all_masters_cont_female":count_all_master_cont_female,
                    "count_all_masters_post":count_all_master_post,
                    "count_all_masters_post_male":count_all_master_post_male,
                    "count_all_masters_post_female":count_all_master_post_female,
                    "count_all_masters_final":count_all_master_final,
                    "count_all_masters_final_male":count_all_master_final_male,
                    "count_all_masters_final_female":count_all_master_final_female,
                    "forms":form,
                    "start_date": start_date,
                    "end_date": end_date
                    }
                    return render(request, templates, context)

            elif gender == '' and start_date == '' and end_date and status:
                if status == continuous:
                    get_all_masters_student_by_end_date_cnt=Student.objects.filter(education_level="MASTERS", end_date=end_date, student_status=continuous)
                    time = datetime.datetime.now()
                    get_time = time.strftime("%c")
                    templates = 'account/masters.html'
                    context = {
                    "get_time":get_time,
                    "get_college":get_college,
                    "get_all_masters_student_by_end_date_cnt":get_all_masters_student_by_end_date_cnt,
                    "count_all_masters":count_all_master,
                    "count_all_masters_male":count_all_master_male,
                    "count_all_masters_female":count_all_master_female,
                    "count_all_masters_comp":count_all_master_comp,
                    "count_all_masters_comp_male":count_all_master_comp_male,
                    "count_all_masters_comp_female":count_all_master_comp_female,
                    "count_all_masters_cont":count_all_master_cont,
                    "count_all_masters_cont_male":count_all_master_cont_male,
                    "count_all_masters_cont_female":count_all_master_cont_female,
                    "count_all_masters_post":count_all_master_post,
                    "count_all_masters_post_male":count_all_master_post_male,
                    "count_all_masters_post_female":count_all_master_post_female,
                    "count_all_masters_final":count_all_master_final,
                    "count_all_masters_final_male":count_all_master_final_male,
                    "count_all_masters_final_female":count_all_master_final_female,
                    "forms":form,
                    "start_date": start_date,
                    "end_date": end_date
                    }
                    return render(request, templates, context)
                elif status == postpone:
                    get_all_masters_student_by_end_date_pst=Student.objects.filter(education_level="MASTERS", end_date=end_date, student_status=postpone)
                    time = datetime.datetime.now()
                    get_time = time.strftime("%c")
                    templates = 'account/masters.html'
                    context = {
                    "get_time":get_time,
                    "get_college":get_college,
                    "get_all_masters_student_by_end_date_pst":get_all_masters_student_by_end_date_pst,
                    "count_all_masters":count_all_master,
                    "count_all_masters_male":count_all_master_male,
                    "count_all_masters_female":count_all_master_female,
                    "count_all_masters_comp":count_all_master_comp,
                    "count_all_masters_comp_male":count_all_master_comp_male,
                    "count_all_masters_comp_female":count_all_master_comp_female,
                    "count_all_masters_cont":count_all_master_cont,
                    "count_all_masters_cont_male":count_all_master_cont_male,
                    "count_all_masters_cont_female":count_all_master_cont_female,
                    "count_all_masters_post":count_all_master_post,
                    "count_all_masters_post_male":count_all_master_post_male,
                    "count_all_masters_post_female":count_all_master_post_female,
                    "count_all_masters_final":count_all_master_final,
                    "count_all_masters_final_male":count_all_master_final_male,
                    "count_all_masters_final_female":count_all_master_final_female,
                    "forms":form,
                    "start_date": start_date,
                    "end_date": end_date
                    }
                    return render(request, templates, context)
                elif status == complete:
                    get_all_masters_student_by_end_date_cmp=Student.objects.filter(education_level="MASTERS", end_date=end_date, student_status=complete)
                    time = datetime.datetime.now()
                    get_time = time.strftime("%c")
                    templates = 'account/masters.html'
                    context = {
                    "get_time":get_time,
                    "get_college":get_college,
                    "get_all_masters_student_by_end_date_cmp":get_all_masters_student_by_end_date_cmp,
                    "count_all_masters":count_all_master,
                    "count_all_masters_male":count_all_master_male,
                    "count_all_masters_female":count_all_master_female,
                    "count_all_masters_comp":count_all_master_comp,
                    "count_all_masters_comp_male":count_all_master_comp_male,
                    "count_all_masters_comp_female":count_all_master_comp_female,
                    "count_all_masters_cont":count_all_master_cont,
                    "count_all_masters_cont_male":count_all_master_cont_male,
                    "count_all_masters_cont_female":count_all_master_cont_female,
                    "count_all_masters_post":count_all_master_post,
                    "count_all_masters_post_male":count_all_master_post_male,
                    "count_all_masters_post_female":count_all_master_post_female,
                    "count_all_masters_final":count_all_master_final,
                    "count_all_masters_final_male":count_all_master_final_male,
                    "count_all_masters_final_female":count_all_master_final_female,
                    "forms":form,
                    "start_date": start_date,
                    "end_date": end_date
                    }
                    return render(request, templates, context)
                else:
                    get_all_masters_student_by_end_date_fnl=Student.objects.filter(education_level="MASTERS", end_date=end_date, student_status=final)
                    time = datetime.datetime.now()
                    get_time = time.strftime("%c")
                    templates = 'account/masters.html'
                    context = {
                    "get_time":get_time,
                    "get_college":get_college,
                    "get_all_masters_student_by_end_date_fnl":get_all_masters_student_by_end_date_fnl,
                    "count_all_masters":count_all_master,
                    "count_all_masters_male":count_all_master_male,
                    "count_all_masters_female":count_all_master_female,
                    "count_all_masters_comp":count_all_master_comp,
                    "count_all_masters_comp_male":count_all_master_comp_male,
                    "count_all_masters_comp_female":count_all_master_comp_female,
                    "count_all_masters_cont":count_all_master_cont,
                    "count_all_masters_cont_male":count_all_master_cont_male,
                    "count_all_masters_cont_female":count_all_master_cont_female,
                    "count_all_masters_post":count_all_master_post,
                    "count_all_masters_post_male":count_all_master_post_male,
                    "count_all_masters_post_female":count_all_master_post_female,
                    "count_all_masters_final":count_all_master_final,
                    "count_all_masters_final_male":count_all_master_final_male,
                    "count_all_masters_final_female":count_all_master_final_female,
                    "forms":form,
                    "start_date": start_date,
                    "end_date": end_date
                    }
                    return render(request, templates, context)

            ################## triple selection ################################
            elif gender and start_date and end_date and status =='':
                if gender == male:
                    get_all_masters_student_by_start_date_end_date_male=Student.objects.filter(education_level="MASTERS", start_date=start_date, end_date=end_date, gender=male)
                    time = datetime.datetime.now()
                    get_time = time.strftime("%c")
                    templates = 'account/masters.html'
                    context = {
                    "get_time":get_time,
                    "get_college":get_college,
                    "get_all_masters_student_by_start_date_end_date_male":get_all_masters_student_by_start_date_end_date_male,
                    "count_all_masters":count_all_master,
                    "count_all_masters_male":count_all_master_male,
                    "count_all_masters_female":count_all_master_female,
                    "count_all_masters_comp":count_all_master_comp,
                    "count_all_masters_comp_male":count_all_master_comp_male,
                    "count_all_masters_comp_female":count_all_master_comp_female,
                    "count_all_masters_cont":count_all_master_cont,
                    "count_all_masters_cont_male":count_all_master_cont_male,
                    "count_all_masters_cont_female":count_all_master_cont_female,
                    "count_all_masters_post":count_all_master_post,
                    "count_all_masters_post_male":count_all_master_post_male,
                    "count_all_masters_post_female":count_all_master_post_female,
                    "count_all_masters_final":count_all_master_final,
                    "count_all_masters_final_male":count_all_master_final_male,
                    "count_all_masters_final_female":count_all_master_final_female,
                    "forms":form,
                    "start_date": start_date,
                    "end_date": end_date
                    }
                    return render(request, templates, context)

                else:
                    get_all_masters_student_by_start_date_end_date_female=Student.objects.filter(education_level="MASTERS", start_date=start_date, end_date=end_date, gender=female)
                    time = datetime.datetime.now()
                    get_time = time.strftime("%c")
                    templates = 'account/masters.html'
                    context = {
                    "get_time":get_time,
                    "get_college":get_college,
                    "get_all_masters_student_by_start_date_end_date_female":get_all_masters_student_by_start_date_end_date_female,
                    "count_all_masters":count_all_master,
                    "count_all_masters_male":count_all_master_male,
                    "count_all_masters_female":count_all_master_female,
                    "count_all_masters_comp":count_all_master_comp,
                    "count_all_masters_comp_male":count_all_master_comp_male,
                    "count_all_masters_comp_female":count_all_master_comp_female,
                    "count_all_masters_cont":count_all_master_cont,
                    "count_all_masters_cont_male":count_all_master_cont_male,
                    "count_all_masters_cont_female":count_all_master_cont_female,
                    "count_all_masters_post":count_all_master_post,
                    "count_all_masters_post_male":count_all_master_post_male,
                    "count_all_masters_post_female":count_all_master_post_female,
                    "count_all_masters_final":count_all_master_final,
                    "count_all_masters_final_male":count_all_master_final_male,
                    "count_all_masters_final_female":count_all_master_final_female,
                    "forms":form,
                    "start_date": start_date,
                    "end_date": end_date
                    }
                    return render(request, templates, context)
            elif gender and start_date and end_date=="" and status:
                if gender == male:
                    if status == continuous:
                        get_all_masters_student_by_start_date_cnt_male=Student.objects.filter(education_level="MASTERS", start_date=start_date, student_status=continuous, gender=male)
                        time = datetime.datetime.now()
                        get_time = time.strftime("%c")
                        templates = 'account/masters.html'
                        context = {
                        "get_time":get_time,
                        "get_college":get_college,
                        "get_all_masters_student_by_start_date_cnt_male":get_all_masters_student_by_start_date_cnt_male,
                        "count_all_masters":count_all_master,
                        "count_all_masters_male":count_all_master_male,
                        "count_all_masters_female":count_all_master_female,
                        "count_all_masters_comp":count_all_master_comp,
                        "count_all_masters_comp_male":count_all_master_comp_male,
                        "count_all_masters_comp_female":count_all_master_comp_female,
                        "count_all_masters_cont":count_all_master_cont,
                        "count_all_masters_cont_male":count_all_master_cont_male,
                        "count_all_masters_cont_female":count_all_master_cont_female,
                        "count_all_masters_post":count_all_master_post,
                        "count_all_masters_post_male":count_all_master_post_male,
                        "count_all_masters_post_female":count_all_master_post_female,
                        "count_all_masters_final":count_all_master_final,
                        "count_all_masters_final_male":count_all_master_final_male,
                        "count_all_masters_final_female":count_all_master_final_female,
                        "forms":form,
                        "start_date": start_date,
                        "end_date": end_date
                        }
                        return render(request, templates, context)
                    elif status == postpone:
                        get_all_masters_student_by_start_date_pst_male=Student.objects.filter(education_level="MASTERS", start_date=start_date, student_status=postpone, gender=male)
                        time = datetime.datetime.now()
                        get_time = time.strftime("%c")
                        templates = 'account/masters.html'
                        context = {
                        "get_time":get_time,
                        "get_college":get_college,
                        "get_all_masters_student_by_start_date_pst_male":get_all_masters_student_by_start_date_pst_male,
                        "count_all_masters":count_all_master,
                        "count_all_masters_male":count_all_master_male,
                        "count_all_masters_female":count_all_master_female,
                        "count_all_masters_comp":count_all_master_comp,
                        "count_all_masters_comp_male":count_all_master_comp_male,
                        "count_all_masters_comp_female":count_all_master_comp_female,
                        "count_all_masters_cont":count_all_master_cont,
                        "count_all_masters_cont_male":count_all_master_cont_male,
                        "count_all_masters_cont_female":count_all_master_cont_female,
                        "count_all_masters_post":count_all_master_post,
                        "count_all_masters_post_male":count_all_master_post_male,
                        "count_all_masters_post_female":count_all_master_post_female,
                        "count_all_masters_final":count_all_master_final,
                        "count_all_masters_final_male":count_all_master_final_male,
                        "count_all_masters_final_female":count_all_master_final_female,
                        "forms":form,
                        "start_date": start_date,
                        "end_date": end_date
                        }
                        return render(request, templates, context)
                    elif status == complete:
                        get_all_masters_student_by_start_date_cmp_male=Student.objects.filter(education_level="MASTERS", start_date=start_date, student_status=complete, gender= male)
                        time = datetime.datetime.now()
                        get_time = time.strftime("%c")
                        templates = 'account/masters.html'
                        context = {
                        "get_time":get_time,
                        "get_college":get_college,
                        "get_all_masters_student_by_start_date_cmp_male":get_all_masters_student_by_start_date_cmp_male,
                        "count_all_masters":count_all_master,
                        "count_all_masters_male":count_all_master_male,
                        "count_all_masters_female":count_all_master_female,
                        "count_all_masters_comp":count_all_master_comp,
                        "count_all_masters_comp_male":count_all_master_comp_male,
                        "count_all_masters_comp_female":count_all_master_comp_female,
                        "count_all_masters_cont":count_all_master_cont,
                        "count_all_masters_cont_male":count_all_master_cont_male,
                        "count_all_masters_cont_female":count_all_master_cont_female,
                        "count_all_masters_post":count_all_master_post,
                        "count_all_masters_post_male":count_all_master_post_male,
                        "count_all_masters_post_female":count_all_master_post_female,
                        "count_all_masters_final":count_all_master_final,
                        "count_all_masters_final_male":count_all_master_final_male,
                        "count_all_masters_final_female":count_all_master_final_female,
                        "forms":form,
                        "start_date": start_date,
                        "end_date": end_date
                        }
                        return render(request, templates, context)
                    else:
                        get_all_msters_student_by_start_date_fnl_male=Student.objects.filter(education_level="MASTERS", start_date=start_date, student_status=final, gender=male)
                        time = datetime.datetime.now()
                        get_time = time.strftime("%c")
                        templates = 'account/masters.html'
                        context = {
                        "get_time":get_time,
                        "get_college":get_college,
                        "get_all_msters_student_by_start_date_fnl_male":get_all_msters_student_by_start_date_fnl_male,
                        "count_all_masters":count_all_master,
                        "count_all_masters_male":count_all_master_male,
                        "count_all_masters_female":count_all_master_female,
                        "count_all_masters_comp":count_all_master_comp,
                        "count_all_masters_comp_male":count_all_master_comp_male,
                        "count_all_masters_comp_female":count_all_master_comp_female,
                        "count_all_masters_cont":count_all_master_cont,
                        "count_all_masters_cont_male":count_all_master_cont_male,
                        "count_all_masters_cont_female":count_all_master_cont_female,
                        "count_all_masters_post":count_all_master_post,
                        "count_all_masters_post_male":count_all_master_post_male,
                        "count_all_masters_post_female":count_all_master_post_female,
                        "count_all_masters_final":count_all_master_final,
                        "count_all_masters_final_male":count_all_master_final_male,
                        "count_all_masters_final_female":count_all_master_final_female,
                        "forms":form,
                        "start_date": start_date,
                        "end_date": end_date
                        }
                        return render(request, templates, context)
                else:
                    if status == continuous:
                        get_all_masters_student_by_start_date_cnt_female=Student.objects.filter(education_level="MASTERS", start_date=start_date, student_status=continuous, gender=female)
                        time = datetime.datetime.now()
                        get_time = time.strftime("%c")
                        templates = 'account/masters.html'
                        context = {
                        "get_time":get_time,
                        "get_college":get_college,
                        "get_all_masters_student_by_start_date_cnt_female":get_all_masters_student_by_start_date_cnt_female,
                        "count_all_masters":count_all_master,
                        "count_all_masters_male":count_all_master_male,
                        "count_all_masters_female":count_all_master_female,
                        "count_all_masters_comp":count_all_master_comp,
                        "count_all_masters_comp_male":count_all_master_comp_male,
                        "count_all_masters_comp_female":count_all_master_comp_female,
                        "count_all_masters_cont":count_all_master_cont,
                        "count_all_masters_cont_male":count_all_master_cont_male,
                        "count_all_masters_cont_female":count_all_master_cont_female,
                        "count_all_masters_post":count_all_master_post,
                        "count_all_masters_post_male":count_all_master_post_male,
                        "count_all_masters_post_female":count_all_master_post_female,
                        "count_all_masters_final":count_all_master_final,
                        "count_all_masters_final_male":count_all_master_final_male,
                        "count_all_masters_final_female":count_all_master_final_female,
                        "forms":form,
                        "start_date": start_date,
                        "end_date": end_date
                        }
                        return render(request, templates, context)
                    elif status == postpone:
                        get_all_masters_student_by_start_date_pst_female=Student.objects.filter(education_level="MASTERS", start_date=start_date, student_status=postpone, gender=female)
                        time = datetime.datetime.now()
                        get_time = time.strftime("%c")
                        templates = 'account/masters.html'
                        context = {
                        "get_time":get_time,
                        "get_college":get_college,
                        "get_all_masters_student_by_start_date_pst_female":get_all_masters_student_by_start_date_pst_female,
                        "count_all_masters":count_all_master,
                        "count_all_masters_male":count_all_master_male,
                        "count_all_masters_female":count_all_master_female,
                        "count_all_masters_comp":count_all_master_comp,
                        "count_all_masters_comp_male":count_all_master_comp_male,
                        "count_all_masters_comp_female":count_all_master_comp_female,
                        "count_all_masters_cont":count_all_master_cont,
                        "count_all_masters_cont_male":count_all_master_cont_male,
                        "count_all_masters_cont_female":count_all_master_cont_female,
                        "count_all_masters_post":count_all_master_post,
                        "count_all_masters_post_male":count_all_master_post_male,
                        "count_all_masters_post_female":count_all_master_post_female,
                        "count_all_masters_final":count_all_master_final,
                        "count_all_masters_final_male":count_all_master_final_male,
                        "count_all_masters_final_female":count_all_master_final_female,
                        "forms":form,
                        "start_date": start_date,
                        "end_date": end_date
                        }
                        return render(request, templates, context)
                    elif status == complete:
                        get_all_masters_student_by_start_date_cmp_female=Student.objects.filter(education_level="MASTERS", start_date=start_date, student_status=complete, gender= male)
                        time = datetime.datetime.now()
                        get_time = time.strftime("%c")
                        templates = 'account/masters.html'
                        context = {
                        "get_time":get_time,
                        "get_college":get_college,
                        "get_all_masters_student_by_start_date_cmp_female":get_all_masters_student_by_start_date_cmp_female,
                        "count_all_masters":count_all_master,
                        "count_all_masters_male":count_all_master_male,
                        "count_all_masters_female":count_all_master_female,
                        "count_all_masters_comp":count_all_master_comp,
                        "count_all_masters_comp_male":count_all_master_comp_male,
                        "count_all_masters_comp_female":count_all_master_comp_female,
                        "count_all_masters_cont":count_all_master_cont,
                        "count_all_masters_cont_male":count_all_master_cont_male,
                        "count_all_masters_cont_female":count_all_master_cont_female,
                        "count_all_masters_post":count_all_master_post,
                        "count_all_masters_post_male":count_all_master_post_male,
                        "count_all_masters_post_female":count_all_master_post_female,
                        "count_all_masters_final":count_all_master_final,
                        "count_all_masters_final_male":count_all_master_final_male,
                        "count_all_masters_final_female":count_all_master_final_female,
                        "forms":form,
                        "start_date": start_date,
                        "end_date": end_date
                        }
                        return render(request, templates, context)
                    else:
                        get_all_masters_student_by_start_date_fnl_female=Student.objects.filter(education_level="MASTERS", start_date=start_date, student_status=final, gender= female)
                        time = datetime.datetime.now()
                        get_time = time.strftime("%c")
                        templates = 'account/masters.html'
                        context = {
                        "get_time":get_time,
                        "get_college":get_college,
                        "get_all_masters_student_by_start_date_fnl_female":get_all_masters_student_by_start_date_fnl_female,
                        "count_all_masters":count_all_master,
                        "count_all_masters_male":count_all_master_male,
                        "count_all_masters_female":count_all_master_female,
                        "count_all_masters_comp":count_all_master_comp,
                        "count_all_masters_comp_male":count_all_master_comp_male,
                        "count_all_masters_comp_female":count_all_master_comp_female,
                        "count_all_masters_cont":count_all_master_cont,
                        "count_all_masters_cont_male":count_all_master_cont_male,
                        "count_all_masters_cont_female":count_all_master_cont_female,
                        "count_all_masters_post":count_all_master_post,
                        "count_all_masters_post_male":count_all_master_post_male,
                        "count_all_masters_post_female":count_all_master_post_female,
                        "count_all_masters_final":count_all_master_final,
                        "count_all_masters_final_male":count_all_master_final_male,
                        "count_all_masters_final_female":count_all_master_final_female,
                        "forms":form,
                        "start_date": start_date,
                        "end_date": end_date
                        }
                        return render(request, templates, context)
            elif gender and start_date =='' and end_date and status:
                if gender == male:
                    if status == continuous:
                        get_all_masters_student_by_end_date_cnt_male=Student.objects.filter(education_level="MASTERS", end_date=end_date, student_status=continuous, gender=male)
                        time = datetime.datetime.now()
                        get_time = time.strftime("%c")
                        templates = 'account/masters.html'
                        context = {
                        "get_time":get_time,
                        "get_college":get_college,
                        "get_all_masters_student_by_end_date_cnt_male":get_all_masters_student_by_end_date_cnt_male,
                        "count_all_masters":count_all_master,
                        "count_all_masters_male":count_all_master_male,
                        "count_all_masters_female":count_all_master_female,
                        "count_all_masters_comp":count_all_master_comp,
                        "count_all_masters_comp_male":count_all_master_comp_male,
                        "count_all_masters_comp_female":count_all_master_comp_female,
                        "count_all_masters_cont":count_all_master_cont,
                        "count_all_masters_cont_male":count_all_master_cont_male,
                        "count_all_masters_cont_female":count_all_master_cont_female,
                        "count_all_masters_post":count_all_master_post,
                        "count_all_masters_post_male":count_all_master_post_male,
                        "count_all_masters_post_female":count_all_master_post_female,
                        "count_all_masters_final":count_all_master_final,
                        "count_all_masters_final_male":count_all_master_final_male,
                        "count_all_masters_final_female":count_all_master_final_female,
                        "forms":form,
                        "start_date": start_date,
                        "end_date": end_date
                        }
                        return render(request, templates, context)
                    elif status == postpone:
                        get_all_masters_student_by_end_date_pst_male=Student.objects.filter(education_level="MASTERS", end_date=end_date, student_status=postpone, gender=male)
                        time = datetime.datetime.now()
                        get_time = time.strftime("%c")
                        templates = 'account/masters.html'
                        context = {
                        "get_time":get_time,
                        "get_college":get_college,
                        "get_all_masters_student_by_end_date_pst_male":get_all_masters_student_by_end_date_pst_male,
                        "count_all_masters":count_all_master,
                        "count_all_masters_male":count_all_master_male,
                        "count_all_masters_female":count_all_master_female,
                        "count_all_masters_comp":count_all_master_comp,
                        "count_all_masters_comp_male":count_all_master_comp_male,
                        "count_all_masters_comp_female":count_all_master_comp_female,
                        "count_all_masters_cont":count_all_master_cont,
                        "count_all_masters_cont_male":count_all_master_cont_male,
                        "count_all_masters_cont_female":count_all_master_cont_female,
                        "count_all_masters_post":count_all_master_post,
                        "count_all_masters_post_male":count_all_master_post_male,
                        "count_all_masters_post_female":count_all_master_post_female,
                        "count_all_masters_final":count_all_master_final,
                        "count_all_masters_final_male":count_all_master_final_male,
                        "count_all_masters_final_female":count_all_master_final_female,
                        "forms":form,
                        "start_date": start_date,
                        "end_date": end_date
                        }
                        return render(request, templates, context)
                    elif status == complete:
                        get_all_masters_student_by_end_date_cmp_male=Student.objects.filter(education_level="MASTERS", end_date=end_date, student_status=complete, gender= male)
                        time = datetime.datetime.now()
                        get_time = time.strftime("%c")
                        templates = 'account/masters.html'
                        context = {
                        "get_time":get_time,
                        "get_college":get_college,
                        "get_all_masters_student_by_end_date_cmp_male":get_all_masters_student_by_end_date_cmp_male,
                        "count_all_masters":count_all_master,
                        "count_all_masters_male":count_all_master_male,
                        "count_all_masters_female":count_all_master_female,
                        "count_all_masters_comp":count_all_master_comp,
                        "count_all_masters_comp_male":count_all_master_comp_male,
                        "count_all_masters_comp_female":count_all_master_comp_female,
                        "count_all_masters_cont":count_all_master_cont,
                        "count_all_masters_cont_male":count_all_master_cont_male,
                        "count_all_masters_cont_female":count_all_master_cont_female,
                        "count_all_masters_post":count_all_master_post,
                        "count_all_masters_post_male":count_all_master_post_male,
                        "count_all_masters_post_female":count_all_master_post_female,
                        "count_all_masters_final":count_all_master_final,
                        "count_all_masters_final_male":count_all_master_final_male,
                        "count_all_masters_final_female":count_all_master_final_female,
                        "forms":form,
                        "start_date": start_date,
                        "end_date": end_date
                        }
                        return render(request, templates, context)
                    else:
                        get_all_masters_student_by_end_date_fnl_male=Student.objects.filter(education_level="MASTERS", end_date=end_date, student_status=final, gender=male)
                        time = datetime.datetime.now()
                        get_time = time.strftime("%c")
                        templates = 'account/masters.html'
                        context = {
                        "get_time":get_time,
                        "get_college":get_college,
                        "get_all_masters_student_by_end_date_fnl_male":get_all_masters_student_by_end_date_fnl_male,
                        "count_all_masters":count_all_master,
                        "count_all_masters_male":count_all_master_male,
                        "count_all_masters_female":count_all_master_female,
                        "count_all_masters_comp":count_all_master_comp,
                        "count_all_masters_comp_male":count_all_master_comp_male,
                        "count_all_masters_comp_female":count_all_master_comp_female,
                        "count_all_masters_cont":count_all_master_cont,
                        "count_all_masters_cont_male":count_all_master_cont_male,
                        "count_all_masters_cont_female":count_all_master_cont_female,
                        "count_all_masters_post":count_all_master_post,
                        "count_all_masters_post_male":count_all_master_post_male,
                        "count_all_masters_post_female":count_all_master_post_female,
                        "count_all_masters_final":count_all_master_final,
                        "count_all_masters_final_male":count_all_master_final_male,
                        "count_all_masters_final_female":count_all_master_final_female,
                        "forms":form,
                        "start_date": start_date,
                        "end_date": end_date
                        }
                        return render(request, templates, context)
                else:
                    if status == continuous:
                        get_all_masters_student_by_end_date_cnt_female=Student.objects.filter(education_level="MASTERS", end_date=end_date, student_status=continuous, gender=female)
                        time = datetime.datetime.now()
                        get_time = time.strftime("%c")
                        templates = 'account/masters.html'
                        context = {
                        "get_time":get_time,
                        "get_college":get_college,
                        "get_all_masters_student_by_end_date_cnt_female":get_all_masters_student_by_end_date_cnt_female,
                        "count_all_masters":count_all_master,
                        "count_all_masters_male":count_all_master_male,
                        "count_all_masters_female":count_all_master_female,
                        "count_all_masters_comp":count_all_master_comp,
                        "count_all_masters_comp_male":count_all_master_comp_male,
                        "count_all_masters_comp_female":count_all_master_comp_female,
                        "count_all_masters_cont":count_all_master_cont,
                        "count_all_masters_cont_male":count_all_master_cont_male,
                        "count_all_masters_cont_female":count_all_master_cont_female,
                        "count_all_masters_post":count_all_master_post,
                        "count_all_masters_post_male":count_all_master_post_male,
                        "count_all_masters_post_female":count_all_master_post_female,
                        "count_all_masters_final":count_all_master_final,
                        "count_all_masters_final_male":count_all_master_final_male,
                        "count_all_masters_final_female":count_all_master_final_female,
                        "forms":form,
                        "start_date": start_date,
                        "end_date": end_date
                        }
                        return render(request, templates, context)
                    elif status == postpone:
                        get_all_masters_student_by_end_date_pst_female=Student.objects.filter(education_level="MASTERS", end_date=end_date, student_status=postpone, gender=female)
                        time = datetime.datetime.now()
                        get_time = time.strftime("%c")
                        templates = 'account/masters.html'
                        context = {
                        "get_time":get_time,
                        "get_college":get_college,
                        "get_all_masters_student_by_end_date_pst_female":get_all_masters_student_by_end_date_pst_female,
                        "count_all_masters":count_all_master,
                        "count_all_masters_male":count_all_master_male,
                        "count_all_masters_female":count_all_master_female,
                        "count_all_masters_comp":count_all_master_comp,
                        "count_all_masters_comp_male":count_all_master_comp_male,
                        "count_all_masters_comp_female":count_all_master_comp_female,
                        "count_all_masters_cont":count_all_master_cont,
                        "count_all_masters_cont_male":count_all_master_cont_male,
                        "count_all_masters_cont_female":count_all_master_cont_female,
                        "count_all_masters_post":count_all_master_post,
                        "count_all_masters_post_male":count_all_master_post_male,
                        "count_all_masters_post_female":count_all_master_post_female,
                        "count_all_masters_final":count_all_master_final,
                        "count_all_masters_final_male":count_all_master_final_male,
                        "count_all_masters_final_female":count_all_master_final_female,
                        "forms":form,
                        "start_date": start_date,
                        "end_date": end_date
                        }
                        return render(request, templates, context)
                    elif status == complete:
                        get_all_masters_student_by_end_date_cmp_female=Student.objects.filter(education_level="MASTERS", end_date=end_date, student_status=complete, gender= male)
                        time = datetime.datetime.now()
                        get_time = time.strftime("%c")
                        templates = 'account/masters.html'
                        context = {
                        "get_time":get_time,
                        "get_college":get_college,
                        "get_all_masters_student_by_end_date_cmp_female":get_all_masters_student_by_end_date_cmp_female,
                        "count_all_masters":count_all_master,
                        "count_all_masters_male":count_all_master_male,
                        "count_all_masters_female":count_all_master_female,
                        "count_all_masters_comp":count_all_master_comp,
                        "count_all_masters_comp_male":count_all_master_comp_male,
                        "count_all_masters_comp_female":count_all_master_comp_female,
                        "count_all_masters_cont":count_all_master_cont,
                        "count_all_masters_cont_male":count_all_master_cont_male,
                        "count_all_masters_cont_female":count_all_master_cont_female,
                        "count_all_masters_post":count_all_master_post,
                        "count_all_masters_post_male":count_all_master_post_male,
                        "count_all_masters_post_female":count_all_master_post_female,
                        "count_all_masters_final":count_all_master_final,
                        "count_all_masters_final_male":count_all_master_final_male,
                        "count_all_masters_final_female":count_all_master_final_female,
                        "forms":form,
                        "start_date": start_date,
                        "end_date": end_date
                        }
                        return render(request, templates, context)
                    else:
                        get_all_masters_student_by_end_date_fnl_female=Student.objects.filter(education_level="MASTERS", end_date=end_date, student_status=final, gender=female)
                        time = datetime.datetime.now()
                        get_time = time.strftime("%c")
                        templates = 'account/masters.html'
                        context = {
                        "get_time":get_time,
                        "get_college":get_college,
                        "get_all_masters_student_by_end_date_fnl_female":get_all_masters_student_by_end_date_fnl_female,
                        "count_all_masters":count_all_master,
                        "count_all_masters_male":count_all_master_male,
                        "count_all_masters_female":count_all_master_female,
                        "count_all_masters_comp":count_all_master_comp,
                        "count_all_masters_comp_male":count_all_master_comp_male,
                        "count_all_masters_comp_female":count_all_master_comp_female,
                        "count_all_masters_cont":count_all_master_cont,
                        "count_all_masters_cont_male":count_all_master_cont_male,
                        "count_all_masters_cont_female":count_all_master_cont_female,
                        "count_all_masters_post":count_all_master_post,
                        "count_all_masters_post_male":count_all_master_post_male,
                        "count_all_masters_post_female":count_all_master_post_female,
                        "count_all_masters_final":count_all_master_final,
                        "count_all_masters_final_male":count_all_master_final_male,
                        "count_all_masters_final_female":count_all_master_final_female,
                        "forms":form,
                        "start_date": start_date,
                        "end_date": end_date
                        }
                        return render(request, templates, context)
            elif gender=='' and start_date and end_date and status:
                if status == continuous:
                    get_all_masters_student_by_start_date_end_date_cnt=Student.objects.filter(education_level="MASTERS",start_date=start_date, end_date=end_date, student_status=continuous)
                    time = datetime.datetime.now()
                    get_time = time.strftime("%c")
                    templates = 'account/masters.html'
                    context = {
                    "get_time":get_time,
                    "get_college":get_college,
                    "get_all_masters_student_by_start_date_end_date_cnt":get_all_masters_student_by_start_date_end_date_cnt,
                    "count_all_masters":count_all_master,
                    "count_all_masters_male":count_all_master_male,
                    "count_all_masters_female":count_all_master_female,
                    "count_all_masters_comp":count_all_master_comp,
                    "count_all_masters_comp_male":count_all_master_comp_male,
                    "count_all_masters_comp_female":count_all_master_comp_female,
                    "count_all_masters_cont":count_all_master_cont,
                    "count_all_masters_cont_male":count_all_master_cont_male,
                    "count_all_masters_cont_female":count_all_master_cont_female,
                    "count_all_masters_post":count_all_master_post,
                    "count_all_masters_post_male":count_all_master_post_male,
                    "count_all_masters_post_female":count_all_master_post_female,
                    "count_all_masters_final":count_all_master_final,
                    "count_all_masters_final_male":count_all_master_final_male,
                    "count_all_masters_final_female":count_all_master_final_female,
                    "forms":form,
                    "start_date": start_date,
                    "end_date": end_date
                    }
                    return render(request, templates, context)
                elif status == postpone:
                    get_all_masters_student_by_start_date_end_date_pst=Student.objects.filter(education_level="MASTERS", start_date=start_date, end_date=end_date, student_status=postpone)
                    time = datetime.datetime.now()
                    get_time = time.strftime("%c")
                    templates = 'account/masters.html'
                    context = {
                    "get_time":get_time,
                    "get_college":get_college,
                    "get_all_masters_student_by_start_date_end_date_pst":get_all_masters_student_by_start_date_end_date_pst,
                    "count_all_masters":count_all_master,
                    "count_all_masters_male":count_all_master_male,
                    "count_all_masters_female":count_all_master_female,
                    "count_all_masters_comp":count_all_master_comp,
                    "count_all_masters_comp_male":count_all_master_comp_male,
                    "count_all_masters_comp_female":count_all_master_comp_female,
                    "count_all_masters_cont":count_all_master_cont,
                    "count_all_masters_cont_male":count_all_master_cont_male,
                    "count_all_masters_cont_female":count_all_master_cont_female,
                    "count_all_masters_post":count_all_master_post,
                    "count_all_masters_post_male":count_all_master_post_male,
                    "count_all_masters_post_female":count_all_master_post_female,
                    "count_all_masters_final":count_all_master_final,
                    "count_all_masters_final_male":count_all_master_final_male,
                    "count_all_masters_final_female":count_all_master_final_female,
                    "forms":form,
                    "start_date": start_date,
                    "end_date": end_date
                    }
                    return render(request, templates, context)
                elif status == complete:
                    get_all_masters_student_by_start_date_end_date_cmp=Student.objects.filter(education_level="MASTERS",start_date=start_date, end_date=end_date, student_status=complete)
                    time = datetime.datetime.now()
                    get_time = time.strftime("%c")
                    templates = 'account/masters.html'
                    context = {
                    "get_time":get_time,
                    "get_college":get_college,
                    "get_all_masters_student_by_start_date_end_date_cmp":get_all_masters_student_by_start_date_end_date_cmp,
                    "count_all_masters":count_all_master,
                    "count_all_masters_male":count_all_master_male,
                    "count_all_masters_female":count_all_master_female,
                    "count_all_masters_comp":count_all_master_comp,
                    "count_all_masters_comp_male":count_all_master_comp_male,
                    "count_all_masters_comp_female":count_all_master_comp_female,
                    "count_all_masters_cont":count_all_master_cont,
                    "count_all_masters_cont_male":count_all_master_cont_male,
                    "count_all_masters_cont_female":count_all_master_cont_female,
                    "count_all_masters_post":count_all_master_post,
                    "count_all_masters_post_male":count_all_master_post_male,
                    "count_all_masters_post_female":count_all_master_post_female,
                    "count_all_masters_final":count_all_master_final,
                    "count_all_masters_final_male":count_all_master_final_male,
                    "count_all_masters_final_female":count_all_master_final_female,
                    "forms":form,
                    "start_date": start_date,
                    "end_date": end_date
                    }
                    return render(request, templates, context)
                else:
                    get_all_masters_student_by_start_date_end_date_fnl=Student.objects.filter(education_level="MASTERS",start_date=start_date, end_date=end_date, student_status=final)
                    time = datetime.datetime.now()
                    get_time = time.strftime("%c")
                    templates = 'account/masters.html'
                    context = {
                    "get_time":get_time,
                    "get_college":get_college,
                    "get_all_masters_student_by_start_date_end_date_fnl":get_all_masters_student_by_start_date_end_date_fnl,
                    "count_all_masters":count_all_master,
                    "count_all_masters_male":count_all_master_male,
                    "count_all_masters_female":count_all_master_female,
                    "count_all_masters_comp":count_all_master_comp,
                    "count_all_masters_comp_male":count_all_master_comp_male,
                    "count_all_masters_comp_female":count_all_master_comp_female,
                    "count_all_masters_cont":count_all_master_cont,
                    "count_all_masters_cont_male":count_all_master_cont_male,
                    "count_all_masters_cont_female":count_all_master_cont_female,
                    "count_all_masters_post":count_all_master_post,
                    "count_all_masters_post_male":count_all_master_post_male,
                    "count_all_masters_post_female":count_all_master_post_female,
                    "count_all_masters_final":count_all_master_final,
                    "count_all_masters_final_male":count_all_master_final_male,
                    "count_all_masters_final_female":count_all_master_final_female,
                    "forms":form,
                    "start_date": start_date,
                    "end_date": end_date
                    }
                    return render(request, templates, context)
            ################### quoter selections #########################
            elif gender and start_date and end_date and status:
                if gender == male:
                    if status == continuous:
                        get_all_masters_student_by_start_date_end_date_cnt_male=Student.objects.filter(education_level="MASTERS",start_date=start_date, end_date=end_date, student_status=continuous, gender=male)
                        time = datetime.datetime.now()
                        get_time = time.strftime("%c")
                        templates = 'account/masters.html'
                        context = {
                        "get_time":get_time,
                        "get_college":get_college,
                        "get_all_masters_student_by_start_date_end_date_cnt_male":get_all_masters_student_by_start_date_end_date_cnt_male,
                        "count_all_masters":count_all_master,
                        "count_all_masters_male":count_all_master_male,
                        "count_all_masters_female":count_all_master_female,
                        "count_all_masters_comp":count_all_master_comp,
                        "count_all_masters_comp_male":count_all_master_comp_male,
                        "count_all_masters_comp_female":count_all_master_comp_female,
                        "count_all_masters_cont":count_all_master_cont,
                        "count_all_masters_cont_male":count_all_master_cont_male,
                        "count_all_masters_cont_female":count_all_master_cont_female,
                        "count_all_masters_post":count_all_master_post,
                        "count_all_masters_post_male":count_all_master_post_male,
                        "count_all_masters_post_female":count_all_master_post_female,
                        "count_all_masters_final":count_all_master_final,
                        "count_all_masters_final_male":count_all_master_final_male,
                        "count_all_masters_final_female":count_all_master_final_female,
                        "forms":form,
                        "start_date": start_date,
                        "end_date": end_date
                        }
                        return render(request, templates, context)
                    elif status == postpone:
                        get_all_masters_student_by_start_date_end_date_pst_male=Student.objects.filter(education_level="MASTERS",start_date=start_date, end_date=end_date, student_status=postpone, gender=male)
                        time = datetime.datetime.now()
                        get_time = time.strftime("%c")
                        templates = 'account/masters.html'
                        context = {
                        "get_time":get_time,
                        "get_college":get_college,
                        "get_all_masters_student_by_start_date_end_date_pst_male":get_all_masters_student_by_start_date_end_date_pst_male,
                        "count_all_masters":count_all_master,
                        "count_all_masters_male":count_all_master_male,
                        "count_all_masters_female":count_all_master_female,
                        "count_all_masters_comp":count_all_master_comp,
                        "count_all_masters_comp_male":count_all_master_comp_male,
                        "count_all_masters_comp_female":count_all_master_comp_female,
                        "count_all_masters_cont":count_all_master_cont,
                        "count_all_masters_cont_male":count_all_master_cont_male,
                        "count_all_masters_cont_female":count_all_master_cont_female,
                        "count_all_masters_post":count_all_master_post,
                        "count_all_masters_post_male":count_all_master_post_male,
                        "count_all_masters_post_female":count_all_master_post_female,
                        "count_all_masters_final":count_all_master_final,
                        "count_all_masters_final_male":count_all_master_final_male,
                        "count_all_masters_final_female":count_all_master_final_female,
                        "forms":form,
                        "start_date": start_date,
                        "end_date": end_date
                        }
                        return render(request, templates, context)
                    elif status == complete:
                        get_all_masters_student_by_start_date_end_date_cmp_male=Student.objects.filter(education_level="MASTERS",start_date=start_date, end_date=end_date, student_status=complete, gender=male)
                        time = datetime.datetime.now()
                        get_time = time.strftime("%c")
                        templates = 'account/masters.html'
                        context = {
                        "get_time":get_time,
                        "get_college":get_college,
                        "get_all_masters_student_by_start_date_end_date_cmp_male":get_all_masters_student_by_start_date_end_date_cmp_male,
                        "count_all_masters":count_all_master,
                        "count_all_masters_male":count_all_master_male,
                        "count_all_masters_female":count_all_master_female,
                        "count_all_masters_comp":count_all_master_comp,
                        "count_all_masters_comp_male":count_all_master_comp_male,
                        "count_all_masters_comp_female":count_all_master_comp_female,
                        "count_all_masters_cont":count_all_master_cont,
                        "count_all_masters_cont_male":count_all_master_cont_male,
                        "count_all_masters_cont_female":count_all_master_cont_female,
                        "count_all_masters_post":count_all_master_post,
                        "count_all_masters_post_male":count_all_master_post_male,
                        "count_all_masters_post_female":count_all_master_post_female,
                        "count_all_masters_final":count_all_master_final,
                        "count_all_masters_final_male":count_all_master_final_male,
                        "count_all_masters_final_female":count_all_master_final_female,
                        "forms":form,
                        "start_date": start_date,
                        "end_date": end_date
                        }
                        return render(request, templates, context)
                    else:
                        get_all_masters_student_by_start_date_end_date_fnl_male=Student.objects.filter(education_level="MASTERS",start_date=start_date, end_date=end_date, student_status=final, gender=male)
                        time = datetime.datetime.now()
                        get_time = time.strftime("%c")
                        templates = 'account/masters.html'
                        context = {
                        "get_time":get_time,
                        "get_college":get_college,
                        "get_all_masters_student_by_start_date_end_date_fnl_male":get_all_masters_student_by_start_date_end_date_fnl_male,
                        "count_all_masters":count_all_master,
                        "count_all_masters_male":count_all_master_male,
                        "count_all_masters_female":count_all_master_female,
                        "count_all_masters_comp":count_all_master_comp,
                        "count_all_masters_comp_male":count_all_master_comp_male,
                        "count_all_masters_comp_female":count_all_master_comp_female,
                        "count_all_masters_cont":count_all_master_cont,
                        "count_all_masters_cont_male":count_all_master_cont_male,
                        "count_all_masters_cont_female":count_all_master_cont_female,
                        "count_all_masters_post":count_all_master_post,
                        "count_all_masters_post_male":count_all_master_post_male,
                        "count_all_masters_post_female":count_all_master_post_female,
                        "count_all_masters_final":count_all_master_final,
                        "count_all_masters_final_male":count_all_master_final_male,
                        "count_all_masters_final_female":count_all_master_final_female,
                        "forms":form,
                        "start_date": start_date,
                        "end_date": end_date
                        }
                        return render(request, templates, context)
                else:
                     if status == continuous:
                        get_all_masters_student_by_start_date_end_date_cnt_female=Student.objects.filter(education_level="MASTERS",start_date=start_date, end_date=end_date, student_status=continuous, gender=female)
                        time = datetime.datetime.now()
                        get_time = time.strftime("%c")
                        templates = 'account/masters.html'
                        context = {
                        "get_time":get_time,
                        "get_college":get_college,
                        "get_all_masters_student_by_start_date_end_date_cnt_female":get_all_masters_student_by_start_date_end_date_cnt_female,
                        "count_all_masters":count_all_master,
                        "count_all_masters_male":count_all_master_male,
                        "count_all_masters_female":count_all_master_female,
                        "count_all_masters_comp":count_all_master_comp,
                        "count_all_masters_comp_male":count_all_master_comp_male,
                        "count_all_masters_comp_female":count_all_master_comp_female,
                        "count_all_masters_cont":count_all_master_cont,
                        "count_all_masters_cont_male":count_all_master_cont_male,
                        "count_all_masters_cont_female":count_all_master_cont_female,
                        "count_all_masters_post":count_all_master_post,
                        "count_all_masters_post_male":count_all_master_post_male,
                        "count_all_masters_post_female":count_all_master_post_female,
                        "count_all_masters_final":count_all_master_final,
                        "count_all_masters_final_male":count_all_master_final_male,
                        "count_all_masters_final_female":count_all_master_final_female,
                        "forms":form,
                        "start_date": start_date,
                        "end_date": end_date
                        }
                        return render(request, templates, context)
                     elif status == postpone:
                        get_all_masters_student_by_start_date_end_date_pst_female=Student.objects.filter(education_level="MASTERS",start_date=start_date, end_date=end_date, student_status=postpone, gender=female)
                        time = datetime.datetime.now()
                        get_time = time.strftime("%c")
                        templates = 'account/masters.html'
                        context = {
                        "get_time":get_time,
                        "get_college":get_college,
                        "get_all_masters_student_by_start_date_end_date_pst_female":get_all_masters_student_by_start_date_end_date_pst_female,
                        "count_all_masters":count_all_master,
                        "count_all_masters_male":count_all_master_male,
                        "count_all_masters_female":count_all_master_female,
                        "count_all_masters_comp":count_all_master_comp,
                        "count_all_masters_comp_male":count_all_master_comp_male,
                        "count_all_masters_comp_female":count_all_master_comp_female,
                        "count_all_masters_cont":count_all_master_cont,
                        "count_all_masters_cont_male":count_all_master_cont_male,
                        "count_all_masters_cont_female":count_all_master_cont_female,
                        "count_all_masters_post":count_all_master_post,
                        "count_all_masters_post_male":count_all_master_post_male,
                        "count_all_masters_post_female":count_all_master_post_female,
                        "count_all_masters_final":count_all_master_final,
                        "count_all_masters_final_male":count_all_master_final_male,
                        "count_all_masters_final_female":count_all_master_final_female,
                        "forms":form,
                        "start_date": start_date,
                        "end_date": end_date
                        }
                        return render(request, templates, context)
                     elif status == complete:
                        get_all_masters_student_by_start_date_end_date_cmp_female=Student.objects.filter(education_level="MASTERS",start_date=start_date, end_date=end_date, student_status=complete, gender=female)
                        time = datetime.datetime.now()
                        get_time = time.strftime("%c")
                        templates = 'account/masters.html'
                        context = {
                        "get_time":get_time,
                        "get_college":get_college,
                        "get_all_masters_student_by_start_date_end_date_cmp_female":get_all_masters_student_by_start_date_end_date_cmp_female,
                        "count_all_masters":count_all_master,
                        "count_all_masters_male":count_all_master_male,
                        "count_all_masters_female":count_all_master_female,
                        "count_all_masters_comp":count_all_master_comp,
                        "count_all_masters_comp_male":count_all_master_comp_male,
                        "count_all_masters_comp_female":count_all_master_comp_female,
                        "count_all_masters_cont":count_all_master_cont,
                        "count_all_masters_cont_male":count_all_master_cont_male,
                        "count_all_masters_cont_female":count_all_master_cont_female,
                        "count_all_masters_post":count_all_master_post,
                        "count_all_masters_post_male":count_all_master_post_male,
                        "count_all_masters_post_female":count_all_master_post_female,
                        "count_all_masters_final":count_all_master_final,
                        "count_all_masters_final_male":count_all_master_final_male,
                        "count_all_masters_final_female":count_all_master_final_female,
                        "forms":form,
                        "start_date": start_date,
                        "end_date": end_date
                        }
                        return render(request, templates, context)
                     else:
                        get_all_masters_student_by_start_date_end_date_fnl_female=Student.objects.filter(education_level="MASTERS",start_date=start_date, end_date=end_date, student_status=final, gender=female)
                        time = datetime.datetime.now()
                        get_time = time.strftime("%c")
                        templates = 'account/masters.html'
                        context = {
                        "get_time":get_time,
                        "get_college":get_college,
                        "get_all_masters_student_by_start_date_end_date_fnl_female":get_all_masters_student_by_start_date_end_date_fnl_female,
                        "count_all_masters":count_all_master,
                        "count_all_masters_male":count_all_master_male,
                        "count_all_masters_female":count_all_master_female,
                        "count_all_masters_comp":count_all_master_comp,
                        "count_all_masters_comp_male":count_all_master_comp_male,
                        "count_all_masters_comp_female":count_all_master_comp_female,
                        "count_all_masters_cont":count_all_master_cont,
                        "count_all_masters_cont_male":count_all_master_cont_male,
                        "count_all_masters_cont_female":count_all_master_cont_female,
                        "count_all_masters_post":count_all_master_post,
                        "count_all_masters_post_male":count_all_master_post_male,
                        "count_all_masters_post_female":count_all_master_post_female,
                        "count_all_masters_final":count_all_master_final,
                        "count_all_masters_final_male":count_all_master_final_male,
                        "count_all_masters_final_female":count_all_master_final_female,
                        "forms":form,
                        "start_date": start_date,
                        "end_date": end_date
                        }
                        return render(request, templates, context)
        except:
            return HttpResponse("Please Enter valid data")
    else:
        time = datetime.datetime.now()
        get_time = time.strftime("%c")
        templates = 'account/masters.html'
        context = {
        "get_time":get_time,
        "get_college":get_college,
        "get_student":get_all_master_student[:10],
        "count_all_masters":count_all_master,
        "count_all_masters_male":count_all_master_male,
        "count_all_masters_female":count_all_master_female,
        "count_all_masters_comp":count_all_master_comp,
        "count_all_masters_comp_male":count_all_master_comp_male,
        "count_all_masters_comp_female":count_all_master_comp_female,
        "count_all_masters_cont":count_all_master_cont,
        "count_all_masters_cont_male":count_all_master_cont_male,
        "count_all_masters_cont_female":count_all_master_cont_female,
        "count_all_masters_post":count_all_master_post,
        "count_all_masters_post_male":count_all_master_post_male,
        "count_all_masters_post_female":count_all_master_post_female,
        "count_all_masters_final":count_all_master_final,
        "count_all_masters_final_male":count_all_master_final_male,
        "count_all_masters_final_female":count_all_master_final_female,
        "forms":form
        }
        return render(request, templates, context)


@cache_control(no_cache=True, must_revalidate=True, privacy=True, no_store=False)
@login_required(login_url='auth')
def AddStudentView(request):
    create_student_form = forms.CreateStudentForm()
    create_course_form = forms.CreateCourseForm()
    # create_module_form = forms.CreateModuleForm()
    create_college_form = forms.AddCollegeForm()
    if request.method == 'POST':
        form = forms.CreateStudentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'New Student was Added!')
            return redirect("add_student")


    else:
        time = datetime.datetime.now()
        get_time = time.strftime("%c")
        col = Student.objects.all()
        course = Course.objects.all().order_by('-id')
        templates = 'account/add_student.html'
        context = {
         "get_time":get_time,
         "create_student_form":create_student_form,
         "create_course_form":create_course_form,
        #  "create_module_form":create_module_form,
         "create_college_form":create_college_form
        }
        return render(request, templates, context)
# =================all student list ==============
@cache_control(no_cache=True, must_revalidate=True, privacy=True, no_store=False)
@login_required(login_url='auth')
def AllStudentView(request):
    male_student="Male"
    female_student="Female"
    phd_student="PHD"
    masters_student="MASTERS"
    cnt_status="continuous"
    cmp_status="complete"
    pst_status="postpone"
    fnl_status="final"
    form=CreateStudentForm()
    try:
        if request.method =="POST":
            gender=request.POST.get('gender')
            edu_level=request.POST.get('education_level')
            status=request.POST.get('student_status')
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')
            if gender ==''and edu_level=='' and start_date == '' and end_date == '' and status =='':
                get_all_students = Student.objects.all().order_by('-id')
                templates='account/all_student.html'
                context={
                'get_all_students':get_all_students,
                'forms':form
                }
                return render(request, templates, context)
            elif gender and edu_level=='' and start_date == '' and end_date == '' and status =='':
                if gender ==male_student:
                    get_all_male_students =Student.objects.filter(gender=male_student)
                    templates="account/all_student.html"
                    context={
                        "get_all_male_students":get_all_male_students,
                        "forms":form
                    }
                    return render(request, templates, context)
                else:
                    get_all_female_students =Student.objects.filter(gender=female_student)
                    templates="account/all_student.html"
                    context={
                        "get_all_female_students":get_all_female_students,
                        "forms":form
                    }
                    return render(request, templates, context)
            elif gender == '' and edu_level and  start_date=='' and end_date == '' and status =='':
                if edu_level == phd_student:
                    get_all_phd_students =Student.objects.filter(education_level=phd_student)
                    templates="account/all_student.html"
                    context={
                        "get_all_phd_students":get_all_phd_students,
                        "forms":form
                    }
                    return render(request, templates, context)
                else:
                    get_all_masters_students =Student.objects.filter(education_level=masters_student)
                    templates="account/all_student.html"
                    context={
                        "get_all_masters_students":get_all_masters_students,
                        "forms":form
                    }
                    return render(request, templates, context)
            elif gender == '' and edu_level=='' and start_date  and end_date=='' and status =='':
                get_all_students_at_start_date =Student.objects.filter(start_date=str(start_date))
                templates="account/all_student.html"
                context={
                    "get_all_students_at_start_date":get_all_students_at_start_date,
                    "forms":form,
                    "start_date":start_date
                }
                return render(request, templates, context)
            elif gender =='' and edu_level=='' and  start_date =='' and end_date and status=='':
                get_all_students_at_end_date =Student.objects.filter(end_date=str(end_date))
                templates="account/all_student.html"
                context={
                    "get_all_students_at_end_date":get_all_students_at_end_date,
                    "forms":form,
                    "end_date":end_date
                }
                return render(request, templates, context)
            elif gender =='' and edu_level== '' and start_date =='' and end_date=='' and status:
                if status == cnt_status:
                    get_all_cont_students=Student.objects.filter(student_status=cnt_status)
                    templates="account/all_student.html"
                    context={
                        "get_all_cont_students":get_all_cont_students,
                        "forms":form
                    }
                    return render(request, templates, context)
                elif status == pst_status:
                    get_all_pst_students=Student.objects.filter(student_status=pst_status)
                    templates="account/all_student.html"
                    context={
                        "get_all_pst_students":get_all_pst_students,
                        "forms":form
                    }
                    return render(request, templates, context)
                elif status == cmp_status:
                    get_all_cmp_students=Student.objects.filter(student_status=cmp_status)
                    templates="account/all_student.html"
                    context={
                        "get_all_cmp_students":get_all_cmp_students,
                        "forms":form
                    }
                    return render(request, templates, context)
                else:
                    get_all_fnl_students=Student.objects.filter(student_status=fnl_status)
                    templates="account/all_student.html"
                    context={
                        "get_all_fnl_students":get_all_fnl_students,
                        "forms":form
                    }
                    return render(request, templates, context)
            elif gender and  edu_level and start_date=='' and end_date=='' and status=='':
                if gender == male_student:
                    if edu_level == phd_student:
                        get_all_male_phd_students =Student.objects.filter(education_level=phd_student, gender=male_student)
                        templates="account/all_student.html"
                        context={
                            "get_all_male_phd_students":get_all_male_phd_students,
                            "forms":form
                        }
                        return render(request, templates, context)
                    else:
                        get_all_male_masters_students =Student.objects.filter(education_level=masters_student, gender=male_student)
                        templates="account/all_student.html"
                        context={
                            "get_all_male_masters_students":get_all_male_masters_students,
                            "forms":form
                        }
                        return render(request, templates, context)
                else:
                    if edu_level == phd_student:
                        get_all_female_phd_students =Student.objects.filter(education_level=phd_student, gender=female_student)
                        templates="account/all_student.html"
                        context={
                            "get_all_female_phd_students":get_all_female_phd_students,
                            "forms":form
                        }
                        return render(request, templates, context)
                    else:
                        get_all_female_masters_students =Student.objects.filter(education_level=masters_student, gender=female_student)
                        templates="account/all_student.html"
                        context={
                            "get_all_female_masters_students":get_all_female_masters_students,
                            "forms":form
                        }
                        return render(request, templates, context)
            elif gender and edu_level =='' and start_date and end_date== ''and status =='':
                if gender == male_student:
                    get_all_male_student_start_date=Student.objects.filter(gender=male_student, start_date=str(start_date))
                    templates="account/all_student.html"
                    context={
                        "get_all_male_student_start_date":get_all_male_student_start_date,
                        "forms":form,
                        "start_date":start_date
                    }
                    return render (request, templates, context)
                else:
                    get_all_female_student_start_date=Student.objects.filter(gender=female_student, start_date=str(start_date))
                    templates="account/all_student.html"
                    context={
                        "get_all_female_student_start_date":get_all_female_student_start_date,
                        "forms":form,
                        "start_date":start_date
                    }
                    return render (request, templates, context)
            elif gender and edu_level =='' and start_date== '' and end_date and status=='':
                if gender == male_student:
                    get_all_male_student_end_date=Student.objects.filter(gender=male_student, end_date=str(end_date))
                    templates="account/all_student.html"
                    context={
                        "get_all_male_student_end_date":get_all_male_student_end_date,
                        "forms":form,
                        "start_date":end_date
                    }
                    return render (request, templates, context)
                else:
                    get_all_female_student_end_date=Student.objects.filter(gender=female_student, end_date=str(end_date))
                    templates="account/all_student.html"
                    context={
                        "get_all_female_student_end_date":get_all_female_student_end_date,
                        "forms":form,
                        "start_date":end_date
                    }
                    return render (request, templates, context)
            elif gender and edu_level =='' and start_date== '' and end_date=='' and status:
                if gender == male_student:
                    if status == cmp_status:
                        get_all_male_cmp_students=Student.objects.filter(gender=male_student, student_status=cmp_status)
                        templates="account/all_student.html"
                        context={
                            "get_all_male_cmp_students":get_all_male_cmp_students,
                            "forms":form,

                        }
                        return render (request, templates, context)
                    elif status == pst_status:
                        get_all_male_pst_students=Student.objects.filter(gender=male_student, student_status=pst_status)
                        templates="account/all_student.html"
                        context={
                            "get_all_male_pst_students":get_all_male_pst_students,
                            "forms":form,

                        }
                        return render (request, templates, context)
                    elif status == fnl_status:
                        get_all_male_fnl_students=Student.objects.filter(gender=male_student, student_status=fnl_status)
                        templates="account/all_student.html"
                        context={
                            "get_all_male_fnl_students":get_all_male_fnl_students,
                            "forms":form,

                        }
                        return render (request, templates, context)
                    elif status ==cnt_status:
                        get_all_male_cnt_students=Student.objects.filter(gender=male_student, student_status=cnt_status)
                        templates="account/all_student.html"
                        context={
                            "get_all_male_cnt_students":get_all_male_cnt_students,
                            "forms":form,

                        }
                        return render (request, templates, context)
                else:
                    if status == cmp_status:
                        get_all_female_cmp_students=Student.objects.filter(gender=female_student, student_status=cmp_status)
                        templates="account/all_student.html"
                        context={
                            "get_all_female_cmp_students":get_all_female_cmp_students,
                            "forms":form,

                        }
                        return render (request, templates, context)
                    elif status == pst_status:
                        get_all_female_pst_students=Student.objects.filter(gender=female_student, student_status=pst_status)
                        templates="account/all_student.html"
                        context={
                            "get_all_female_pst_students":get_all_female_pst_students,
                            "forms":form,

                        }
                        return render (request, templates, context)
                    elif status == fnl_status:
                        get_all_female_fnl_students=Student.objects.filter(gender=female_student, student_status=fnl_status)
                        templates="account/all_student.html"
                        context={
                            "get_all_female_fnl_students":get_all_female_fnl_students,
                            "forms":form,

                        }
                        return render (request, templates, context)
                    elif status ==cnt_status:
                        get_all_female_cnt_students=Student.objects.filter(gender=female_student, student_status=cnt_status)
                        templates="account/all_student.html"
                        context={
                            "get_all_female_cnt_students":get_all_female_cnt_students,
                            "forms":form,

                        }
                        return render (request, templates, context)

            elif gender =='' and edu_level and start_date and end_date=='' and status =='':
                if edu_level == phd_student:
                    get_all_phd_student_start_date=Student.objects.filter( start_date=str(start_date), education_level=phd_student)
                    templates="account/all_student.html"
                    context={
                        "get_all_phd_student_start_date":get_all_phd_student_start_date,
                        "start_date":start_date,
                        "forms":form
                    }
                    return render(request, templates, context)
                if edu_level == masters_student:
                    print("=============")
                    get_all_masters_student_start_date=Student.objects.filter(start_date=str(start_date), education_level=masters_student)
                    templates="account/all_student.html"
                    context={
                        "get_all_masters_student_start_date":get_all_masters_student_start_date,
                        "start_date":start_date,
                        "forms":form
                    }
                    return render(request, templates, context)
            elif gender =='' and edu_level and start_date== '' and end_date and status =='':
                if edu_level == phd_student:
                    get_all_phd_student_end_date=Student.objects.filter(education_level=phd_student, end_date=str(end_date))
                    templates="account/all_student.html"
                    context={
                        "get_all_phd_student_end_date":get_all_phd_student_end_date,
                        "end_date":end_date,
                        "forms":form
                    }
                    return render (request, templates, context)
                else:
                    get_all_masters_student_end_date=Student.objects.filter(education_level=masters_student, end_date=str(end_date))
                    templates="account/all_student.html"
                    context={
                        "get_all_masters_student_end_date":get_all_masters_student_end_date,
                        "end_date":end_date,
                        "forms":form
                    }
                    return render(request, templates, context)
            elif gender =='' and edu_level and start_date== '' and end_date=='' and status:
                if edu_level == phd_student:
                    if status == cnt_status:
                        get_all_phd_cnt_student=Student.objects.filter(education_level=phd_student, student_status=cnt_status)
                        templates="account/all_student.html"
                        context={
                            "get_all_phd_cnt_student":get_all_phd_cnt_student,
                            "end_date":end_date,
                            "forms":form
                        }
                        return render(request, templates, context)
                    elif status == cmp_status:
                        get_all_phd_cmp_student=Student.objects.filter(education_level=phd_student, student_status=cmp_status)
                        templates="account/all_student.html"
                        context={
                            "get_all_phd_cmp_student":get_all_phd_cmp_student,
                            "end_date":end_date,
                            "forms":form
                        }
                        return render(request, templates, context)
                    elif status == fnl_status:
                        get_all_phd_fnl_student=Student.objects.filter(education_level=phd_student, student_status=fnl_status)
                        templates="account/all_student.html"
                        context={
                            "get_all_phd_fnl_student":get_all_phd_fnl_student,
                            "end_date":end_date,
                            "forms":form
                        }
                        return render(request, templates, context)
                    else:
                        get_all_phd_pst_student=Student.objects.filter(education_level=phd_student, student_status=pst_status)
                        templates="account/all_student.html"
                        context={
                            "get_all_phd_pst_student":get_all_phd_pst_student,
                            "end_date":end_date,
                            "forms":form
                        }
                        return render(request, templates, context)
                else:
                    if status == cnt_status:
                        get_all_masters_cnt_student=Student.objects.filter(education_level=masters_student, student_status=cnt_status)
                        templates="account/all_student.html"
                        context={
                            "get_all_masters_cnt_student":get_all_masters_cnt_student,
                            "end_date":end_date,
                            "forms":form
                        }
                        return render(request, templates, context)
                    elif status == cmp_status:
                        get_all_masters_cmp_student=Student.objects.filter(education_level=masters_student, student_status=cmp_status)
                        templates="account/all_student.html"
                        context={
                            "get_all_masters_cmp_student":get_all_masters_cmp_student,
                            "end_date":end_date,
                            "forms":form
                        }
                        return render(request, templates, context)
                    elif status == fnl_status:
                        get_all_masters_fnl_student=Student.objects.filter(education_level=masters_student, student_status=fnl_status)
                        templates="account/all_student.html"
                        context={
                            "get_all_masters_fnl_student":get_all_masters_fnl_student,
                            "end_date":end_date,
                            "forms":form
                        }
                        return render(request, templates, context)
                    else:
                        get_all_masters_pst_student=Student.objects.filter(education_level=masters_student, student_status=pst_status)
                        templates="account/all_student.html"
                        context={
                            "get_all_masters_pst_student":get_all_masters_pst_student,
                            "end_date":end_date,
                            "forms":form
                        }
                        return render(request, templates, context)



            elif gender =='' and edu_level=='' and start_date and end_date and status=='':
                get_all_from_start_date_up_end_date=Student.objects.filter(start_date=str(start_date), end_date=str(end_date))
                templates="account/all_student.html"
                context={
                    "get_all_from_start_date_up_end_date":get_all_from_start_date_up_end_date,
                    "start_date":start_date,
                    "end_date":end_date,
                    "forms":form
                }
                return render(request, templates, context)

            elif gender =='' and edu_level=='' and start_date and end_date=='' and status:
                if status == cmp_status:
                    get_all_student_from_start_date_cmp=Student.objects.filter(start_date=str(start_date), student_status=cmp_status)
                    templates="account/all_student.html"
                    context={
                        "get_all_student_from_start_date_cmp":get_all_student_from_start_date_cmp,
                        "start_date":start_date,
                        "end_date":end_date,
                        "forms":form
                    }
                    return render(request, templates, context)
                elif status == pst_status:
                    get_all_student_from_start_date_pst=Student.objects.filter(start_date=str(start_date), student_status=pst_status)
                    templates="account/all_student.html"
                    context={
                        "get_all_student_from_start_date_pst":get_all_student_from_start_date_pst,
                        "start_date":start_date,
                        "end_date":end_date,
                        "forms":form
                    }
                    return render(request, templates, context)
                elif status == cnt_status:
                    get_all_student_from_start_date_cnt=Student.objects.filter(start_date=str(start_date), student_status=cnt_status)
                    templates="account/all_student.html"
                    context={
                        "get_all_student_from_start_date_cnt":get_all_student_from_start_date_cnt,
                        "start_date":start_date,
                        "end_date":end_date,
                        "forms":form
                    }
                    return render(request, templates, context)
                else:
                    get_all_student_from_start_date_fnl=Student.objects.filter(start_date=str(start_date), student_status=fnl_status)
                    templates="account/all_student.html"
                    context={
                        "get_all_student_from_start_date_fnl":get_all_student_from_start_date_fnl,
                        "start_date":start_date,
                        "end_date":end_date,
                        "forms":form
                    }
                    return render(request, templates, context)
            elif gender =='' and edu_level=='' and start_date =='' and end_date and status:
                if status == cmp_status:
                    get_all_student_from_end_date_cmp=Student.objects.filter(end_date=str(end_date), student_status=cmp_status)
                    templates="account/all_student.html"
                    context={
                        "get_all_student_from_end_date_cmp":get_all_student_from_end_date_cmp,
                        "start_date":start_date,
                        "end_date":end_date,
                        "forms":form
                    }
                    return render(request, templates, context)
                elif status == pst_status:
                    get_all_student_from_end_date_pst=Student.objects.filter(end_date=str(end_date), student_status=pst_status)
                    templates="account/all_student.html"
                    context={
                        "get_all_student_from_end_date_pst":get_all_student_from_end_date_pst,
                        "start_date":start_date,
                        "end_date":end_date,
                        "forms":form
                    }
                    return render(request, templates, context)
                elif status == cnt_status:
                    get_all_student_from_end_date_cnt=Student.objects.filter(end_date=str(end_date), student_status=cnt_status)
                    templates="account/all_student.html"
                    context={
                        "get_all_student_from_end_date_cnt":get_all_student_from_end_date_cnt,
                        "start_date":start_date,
                        "end_date":end_date,
                        "forms":form
                    }
                    return render(request, templates, context)
                else:
                    get_all_student_from_end_date_fnl=Student.objects.filter(end_date=str(end_date), student_status=fnl_status)
                    templates="account/all_student.html"
                    context={
                        "get_all_student_from_end_date_fnl":get_all_student_from_end_date_fnl,
                        "start_date":start_date,
                        "end_date":end_date,
                        "forms":form
                    }
                    return render(request, templates, context)
            elif gender  and edu_level and start_date and end_date=='' and status=='':
                if gender == male_student:
                    if edu_level == phd_student:
                        get_all_male_phd_student_from_start_date=Student.objects.filter(start_date=str(start_date), gender=male_student, education_level=phd_student)
                        templates="account/all_student.html"
                        context={
                            "get_all_male_phd_student_from_start_date":get_all_male_phd_student_from_start_date,
                            "start_date":start_date,
                            "end_date":end_date,
                            "forms":form
                        }
                        return render(request, templates, context)
                    else:
                        get_all_male_masters_student_from_start_date=Student.objects.filter(start_date=str(start_date), gender=male_student, education_level=masters_student)
                        templates="account/all_student.html"
                        context={
                            "get_all_male_masters_student_from_start_date":get_all_male_masters_student_from_start_date,
                            "start_date":start_date,
                            "end_date":end_date,
                            "forms":form
                        }
                        return render(request, templates, context)
                else:
                    if edu_level == phd_student:
                        get_all_female_phd_student_from_start_date=Student.objects.filter(start_date=str(start_date), gender=female_student, education_level=phd_student)
                        templates="account/all_student.html"
                        context={
                            "get_all_female_phd_student_from_start_date":get_all_female_phd_student_from_start_date,
                            "start_date":start_date,
                            "end_date":end_date,
                            "forms":form
                        }
                        return render(request, templates, context)
                    else:
                        get_all_female_masters_student_from_start_date=Student.objects.filter(start_date=str(start_date), gender=female_student, education_level=masters_student)
                        templates="account/all_student.html"
                        context={
                            "get_all_female_masters_student_from_start_date":get_all_female_masters_student_from_start_date,
                            "start_date":start_date,
                            "end_date":end_date,
                            "forms":form
                        }
                        return render(request, templates, context)

            elif gender  and edu_level and start_date=='' and end_date and status=='':
                if gender == male_student:
                    if edu_level == phd_student:
                        get_all_male_phd_student_from_end_date=Student.objects.filter(end_date=str(end_date), gender=male_student, education_level=phd_student)
                        templates="account/all_student.html"
                        context={
                            "get_all_male_phd_student_from_end_date":get_all_male_phd_student_from_end_date,
                            "start_date":start_date,
                            "end_date":end_date,
                            "forms":form
                        }
                        return render(request, templates, context)
                    else:
                        get_all_male_masters_student_from_end_date=Student.objects.filter(end_date=str(end_date), gender=male_student, education_level=masters_student)
                        templates="account/all_student.html"
                        context={
                            "get_all_male_masters_student_from_end_date":get_all_male_masters_student_from_end_date,
                            "start_date":start_date,
                            "end_date":end_date,
                            "forms":form
                        }
                        return render(request, templates, context)
                else:
                    if edu_level == phd_student:
                        get_all_female_phd_student_from_end_date=Student.objects.filter(end_date=str(end_date), gender=female_student, education_level=phd_student)
                        templates="account/all_student.html"
                        context={
                            "get_all_female_phd_student_from_end_date":get_all_female_phd_student_from_end_date,
                            "start_date":start_date,
                            "end_date":end_date,
                            "forms":form
                        }
                        return render(request, templates, context)
                    else:
                        get_all_female_masters_student_from_end_date=Student.objects.filter(end_date=str(end_date), gender=female_student, education_level=masters_student)
                        templates="account/all_student.html"
                        context={
                            "get_all_female_masters_student_from_end_date":get_all_female_masters_student_from_end_date,
                            "start_date":start_date,
                            "end_date":end_date,
                            "forms":form
                        }
                        return render(request, templates, context)
            elif gender  and edu_level and start_date=='' and end_date=='' and status:
                if gender == male_student:
                    if edu_level == phd_student:
                        if status ==cnt_status:
                            get_all_male_phd_cnt_student=Student.objects.filter(gender=male_student, education_level=phd_student, student_status=cnt_status)
                            templates="account/all_student.html"
                            context={
                                 "get_all_male_phd_cnt_student":get_all_male_phd_cnt_student,
                                 "forms":form
                            }
                            return render(request, templates, context)
                        elif status == cmp_status:
                            get_all_male_phd_cmp_student=Student.objects.filter(gender=male_student, education_level=phd_student, student_status=cmp_status)
                            templates="account/all_student.html"
                            context={
                                 "get_all_male_phd_cmp_student":get_all_male_phd_cmp_student,
                                 "forms":form
                            }
                            return render(request, templates, context)
                        elif status == fnl_status:
                            get_all_male_phd_fnl_student=Student.objects.filter(gender=male_student, education_level=phd_student, student_status=fnl_status)
                            templates="account/all_student.html"
                            context={
                                 "get_all_male_phd_fnl_student":get_all_male_phd_fnl_student,
                                 "forms":form
                            }
                            return render(request, templates, context)
                        else:
                            get_all_male_phd_pst_student=Student.objects.filter(gender=male_student, education_level=phd_student, student_status=pst_status)
                            templates="account/all_student.html"
                            context={
                                 "get_all_male_phd_pst_student":get_all_male_phd_pst_student,
                                 "forms":form
                            }
                            return render(request, templates, context)
                    else:
                        if status ==cnt_status:
                            get_all_male_masters_cnt_student=Student.objects.filter(gender=male_student, education_level=masters_student, student_status=cnt_status)
                            templates="account/all_student.html"
                            context={
                                "get_all_male_masters_cnt_student":get_all_male_masters_cnt_student,
                                "forms":form
                            }
                            return render(request, templates, context)
                        elif status == cmp_status:
                            get_all_male_masters_cmp_student=Student.objects.filter(gender=male_student, education_level=masters_student, student_status=cmp_status)
                            templates="account/all_student.html"
                            context={
                                 "get_all_male_masters_cmp_student":get_all_male_masters_cmp_student,
                                 "forms":form
                            }
                            return render(request, templates, context)
                        elif status == fnl_status:
                            get_all_male_masters_fnl_student=Student.objects.filter(gender=male_student, education_level=masters_student, student_status=fnl_status)
                            templates="account/all_student.html"
                            context={
                                 "get_all_male_masters_fnl_student":get_all_male_masters_fnl_student,
                                 "forms":form
                            }
                            return render(request, templates, context)
                        else:
                            get_all_male_masters_pst_student=Student.objects.filter(gender=male_student, education_level=masters_student, student_status=pst_status)
                            templates="account/all_student.html"
                            context={
                                 "get_all_male_masters_pst_student":get_all_male_masters_pst_student,
                                 "forms":form
                            }
                            return render(request, templates, context)
                else:
                    if edu_level == phd_student:
                        if status ==cnt_status:
                            get_all_female_phd_cnt_student=Student.objects.filter(gender=female_student, education_level=phd_student, student_status=cnt_status)
                            templates="account/all_student.html"
                            context={
                                 "get_all_female_phd_cnt_student":get_all_female_phd_cnt_student,
                                 "forms":form
                            }
                            return render(request, templates, context)
                        elif status == cmp_status:
                            get_all_female_phd_cmp_student=Student.objects.filter(gender=female_student, education_level=phd_student, student_status=cmp_status)
                            templates="account/all_student.html"
                            context={
                                 "get_all_female_phd_cmp_student":get_all_female_phd_cmp_student,
                                 "forms":form
                            }
                            return render(request, templates, context)
                        elif status == fnl_status:
                            get_all_female_phd_fnl_student=Student.objects.filter(gender=female_student, education_level=phd_student, student_status=fnl_status)
                            templates="account/all_student.html"
                            context={
                                 "get_all_female_phd_fnl_student":get_all_female_phd_fnl_student,
                                 "forms":form
                            }
                            return render(request, templates, context)
                        else:
                            get_all_female_phd_pst_student=Student.objects.filter(gender=female_student, education_level=phd_student, student_status=pst_status)
                            templates="account/all_student.html"
                            context={
                                 "get_all_female_phd_pst_student":get_all_female_phd_pst_student,
                                 "forms":form
                            }
                            return render(request, templates, context)
                    else:
                        if status ==cnt_status:
                            get_all_female_masters_cnt_student=Student.objects.filter(gender=female_student, education_level=masters_student, student_status=cnt_status)
                            templates="account/all_student.html"
                            context={
                                "get_all_female_masters_cnt_student":get_all_female_masters_cnt_student,
                                "forms":form
                            }
                            return render(request, templates, context)
                        elif status == cmp_status:
                            get_all_female_masters_cmp_student=Student.objects.filter(gender=female_student, education_level=masters_student, student_status=cmp_status)
                            templates="account/all_student.html"
                            context={
                                 "get_all_female_masters_cmp_student":get_all_female_masters_cmp_student,
                                 "forms":form
                            }
                            return render(request, templates, context)
                        elif status == fnl_status:
                            get_all_female_masters_fnl_student=Student.objects.filter(gender=female_student, education_level=masters_student, student_status=fnl_status)
                            templates="account/all_student.html"
                            context={
                                 "get_all_female_masters_fnl_student":get_all_female_masters_fnl_student,
                                 "forms":form
                            }
                            return render(request, templates, context)
                        else:
                            get_all_female_masters_pst_student=Student.objects.filter(gender=female_student, education_level=masters_student, student_status=pst_status)
                            templates="account/all_student.html"
                            context={
                                 "get_all_female_masters_pst_student":get_all_female_masters_pst_student,
                                 "forms":form
                            }
                            return render(request, templates, context)
            elif gender  and edu_level=='' and start_date and end_date and status=='':
                if gender == male_student:
                    get_all_male_from_start_date_up_end_date=Student.objects.filter(gender=male_student, start_date=str(start_date), end_date=str(end_date))
                    templates="account/all_student.html"
                    context={
                        "get_all_male_from_start_date_up_end_date":get_all_male_from_start_date_up_end_date,
                        "start_date":start_date,
                        "forms":form,
                        "end_date":end_date
                    }
                    return render(request, templates, context)
                else:
                    get_all_female_from_start_date_up_end_date=Student.objects.filter(gender=female_student, start_date=str(start_date), end_date=str(end_date))
                    templates="account/all_student.html"
                    context={
                        "get_all_female_from_start_date_up_end_date":get_all_female_from_start_date_up_end_date,
                        "start_date":start_date,
                        "forms":form,
                        "end_date":end_date
                    }
                    return render(request, templates, context)
            elif gender  and edu_level=='' and start_date and end_date =='' and status:
                if gender == male_student:
                    if status ==cmp_status:
                        if start_date:
                            get_all_male_cmp_from_start_date=Student.objects.filter(gender=male_student, student_status=cmp_status, start_date=str(start_date))
                            templates="account/all_student.html"
                            context={
                                "get_all_male_cmp_from_start_date":get_all_male_cmp_from_start_date,
                                "start_date":start_date,
                                "forms":form
                            }
                            return render (request, templates, context)
                    elif status == cnt_status:
                        if start_date:
                            get_all_male_cnt_from_start_date=Student.objects.filter(gender=male_student, student_status=cnt_status, start_date=str(start_date))
                            templates="account/all_student.html"
                            context={
                                "get_all_male_cnt_from_start_date":get_all_male_cnt_from_start_date,
                                "start_date":start_date,
                                "forms":form
                            }
                            return render (request, templates, context)
                    elif status == pst_status:
                        if start_date:
                            get_all_male_pst_from_start_date=Student.objects.filter(gender=male_student, student_status=pst_status, start_date=str(start_date))
                            templates="account/all_student.html"
                            context={
                                "get_all_male_pst_from_start_date":get_all_male_pst_from_start_date,
                                "start_date":start_date,
                                "forms":form
                            }
                            return render (request, templates, context)
                    else:
                        if start_date:
                            get_all_male_fnl_from_start_date=Student.objects.filter(gender=male_student, student_status=fnl_status, start_date=str(start_date))
                            templates="account/all_student.html"
                            context={
                                "get_all_male_fnl_from_start_date":get_all_male_fnl_from_start_date,
                                "start_date":start_date,
                                "forms":form
                            }
                            return render (request, templates, context)
                else:
                    if status ==cmp_status:
                        if start_date:
                            get_all_female_cmp_from_start_date=Student.objects.filter(gender=female_student, student_status=cmp_status, start_date=str(start_date))
                            templates="account/all_student.html"
                            context={
                                "get_all_female_cmp_from_start_date":get_all_female_cmp_from_start_date,
                                "start_date":start_date,
                                "forms":form
                            }
                            return render (request, templates, context)
                    elif status == cnt_status:
                        if start_date:
                            get_all_female_cnt_from_start_date=Student.objects.filter(gender=female_student, student_status=cnt_status, start_date=str(start_date))
                            templates="account/all_student.html"
                            context={
                                "get_all_female_cnt_from_start_date":get_all_female_cnt_from_start_date,
                                "start_date":start_date,
                                "forms":form
                            }
                            return render (request, templates, context)
                    elif status == pst_status:
                        if start_date:
                            get_all_female_pst_from_start_date=Student.objects.filter(gender=female_student, student_status=pst_status, start_date=str(start_date))
                            templates="account/all_student.html"
                            context={
                                "get_all_female_pst_from_start_date":get_all_female_pst_from_start_date,
                                "start_date":start_date,
                                "forms":form
                            }
                            return render (request, templates, context)
                    else:
                        if start_date:
                            get_all_female_fnl_from_start_date=Student.objects.filter(gender=female_student, student_status=fnl_status, start_date=str(start_date))
                            templates="account/all_student.html"
                            context={
                                "get_all_female_fnl_from_start_date":get_all_female_fnl_from_start_date,
                                "start_date":start_date,
                                "forms":form
                            }
                            return render (request, templates, context)

            elif gender  and edu_level=='' and start_date =='' and end_date and status:
                if gender == male_student:
                    if status ==cmp_status:
                        if end_date:
                            get_all_male_cmp_from_end_date=Student.objects.filter(gender=male_student, student_status=cmp_status, end_date=str(end_date))
                            templates="account/all_student.html"
                            context={
                                "get_all_male_cmp_from_end_date":get_all_male_cmp_from_end_date,
                                "end_date":end_date,
                                "forms":form
                            }
                            return render (request, templates, context)
                    elif status == cnt_status:
                        if end_date:
                            get_all_male_cnt_from_end_date=Student.objects.filter(gender=male_student, student_status=cnt_status, end_date=str(end_date))
                            templates="account/all_student.html"
                            context={
                                "get_all_male_cnt_from_end_date":get_all_male_cnt_from_end_date,
                                "end_date":end_date,
                                "forms":form
                            }
                            return render (request, templates, context)
                    elif status == pst_status:
                        if end_date:
                            get_all_male_pst_from_end_date=Student.objects.filter(gender=male_student, student_status=pst_status, end_date=str(end_date))
                            templates="account/all_student.html"
                            context={
                                "get_all_male_pst_from_end_date":get_all_male_pst_from_end_date,
                                "end_date":end_date,
                                "forms":form
                            }
                            return render (request, templates, context)
                    else:
                        if end_date:
                            get_all_male_fnl_from_end_date=Student.objects.filter(gender=male_student, student_status=fnl_status, end_date=str(end_date))
                            templates="account/all_student.html"
                            context={
                                "get_all_male_fnl_from_end_date":get_all_male_fnl_from_end_date,
                                "end_date":end_date,
                                "forms":form
                            }
                            return render (request, templates, context)
                else:
                    if status ==cmp_status:
                        if end_date:
                            get_all_female_cmp_from_end_date=Student.objects.filter(gender=female_student, student_status=cmp_status, end_date=str(end_date))
                            templates="account/all_student.html"
                            context={
                                "get_all_female_cmp_from_end_date":get_all_female_cmp_from_end_date,
                                "end_date":end_date,
                                "forms":form
                            }
                            return render (request, templates, context)
                    elif status == cnt_status:
                        if end_date:
                            get_all_female_cnt_from_end_date=Student.objects.filter(gender=female_student, student_status=cnt_status, end_date=str(end_date))
                            templates="account/all_student.html"
                            context={
                                "get_all_female_cnt_from_end_date":get_all_female_cnt_from_end_date,
                                "end_date":end_date,
                                "forms":form
                            }
                            return render (request, templates, context)
                    elif status == pst_status:
                        if end_date:
                            get_all_female_pst_from_end_date=Student.objects.filter(gender=female_student, student_status=pst_status, end_date=str(end_date))
                            templates="account/all_student.html"
                            context={
                                "get_all_female_pst_from_end_date":get_all_female_pst_from_end_date,
                                "end_date":end_date,
                                "forms":form
                            }
                            return render (request, templates, context)
                    else:
                        if end_date:
                            get_all_female_fnl_from_end_date=Student.objects.filter(gender=female_student, student_status=fnl_status, end_date=str(end_date))
                            templates="account/all_student.html"
                            context={
                                "get_all_female_fnl_from_end_date":get_all_female_fnl_from_end_date,
                                "end_date":end_date,
                                "forms":form
                            }
                            return render (request, templates, context)
            elif gender  and edu_level and start_date and end_date and status=='':
                if gender == male_student:
                    if edu_level == phd_student:
                        if start_date and end_date:
                            get_all_male_phd_from_start_date_up_end_date=Student.objects.filter(gender=male_student, education_level=phd_student, start_date=str(start_date), end_date=str(end_date))
                            templates = "account/all_student.html"
                            context={
                                "get_all_male_phd_from_start_date_up_end_date":get_all_male_phd_from_start_date_up_end_date,
                                "start_date":start_date,
                                "end_date":end_date
                            }
                            return render (request, templates, context)
                    else:
                        if start_date and end_date:
                            get_all_male_masters_from_start_date_up_end_date=Student.objects.filter(gender=male_student, education_level=masters_student, start_date=str(start_date), end_date=str(end_date))
                            templates = "account/all_student.html"
                            context={
                                "get_all_male_masters_from_start_date_up_end_date":get_all_male_masters_from_start_date_up_end_date,
                                "start_date":start_date,
                                "end_date":end_date
                            }
                            return render (request, templates, context)
                else:
                    if edu_level == phd_student:
                        if start_date and end_date:
                            get_all_female_phd_from_start_date_up_end_date=Student.objects.filter(gender=female_student, education_level=phd_student, start_date=str(start_date), end_date=str(end_date))
                            templates = "account/all_student.html"
                            context={
                                "get_all_female_phd_from_start_date_up_end_date":get_all_female_phd_from_start_date_up_end_date,
                                "start_date":start_date,
                                "end_date":end_date
                            }
                            return render (request, templates, context)
                    else:
                        if start_date and end_date:
                            get_all_female_masters_from_start_date_up_end_date=Student.objects.filter(gender=female_student, education_level=masters_student, start_date=str(start_date), end_date=str(end_date))
                            templates = "account/all_student.html"
                            context={
                                "get_all_female_masters_from_start_date_up_end_date":get_all_female_masters_from_start_date_up_end_date,
                                "start_date":start_date,
                                "end_date":end_date
                            }
                            return render (request, templates, context)
            # anz hapa
            elif gender =='' and edu_level and start_date and end_date and status:
                # phd
                if edu_level == phd_student:
                    if status == cmp_status:
                        if start_date and end_date:
                            get_all_phd_cmp_from_start_date_up_end_date=Student.objects.filter(education_level=phd_student, student_status=cmp_status, start_date=str(start_date), end_date=str(end_date))
                            templates="account/all_student.html"
                            context={
                                "get_all_phd_cmp_from_start_date_up_end_date":get_all_phd_cmp_from_start_date_up_end_date,
                                "start_date":start_date,
                                "end_date":end_date,
                                "forms":form
                            }
                            return render (request, templates, context)
                    elif status == cnt_status:
                        if start_date and end_date:
                            get_all_phd_cnt_from_start_date_up_end_date=Student.objects.filter(education_level=phd_student, student_status=cnt_status, start_date=str(start_date), end_date=str(end_date))
                            templates="account/all_student.html"
                            context={
                                "get_all_phd_cnt_from_start_date_up_end_date":get_all_phd_cnt_from_start_date_up_end_date,
                                "start_date":start_date,
                                "end_date":end_date,
                                "forms":form
                            }
                            return render (request, templates, context)
                    elif status == fnl_status:
                        if start_date and end_date:
                            get_all_phd_fnl_from_start_date_up_end_date=Student.objects.filter(education_level=phd_student, student_status=fnl_status, start_date=str(start_date), end_date=str(end_date))
                            templates="account/all_student.html"
                            context={
                                "get_all_phd_fnl_from_start_date_up_end_date":get_all_phd_fnl_from_start_date_up_end_date,
                                "start_date":start_date,
                                "end_date":end_date,
                                "forms":form
                            }
                            return render (request, templates, context)
                    else:
                        if start_date and end_date:
                            get_all_phd_pst_from_start_date_up_end_date=Student.objects.filter(education_level=phd_student, student_status=pst_status, start_date=str(start_date), end_date=str(end_date))
                            templates="account/all_student.html"
                            context={
                                "get_all_phd_pst_from_start_date_up_end_date":get_all_phd_pst_from_start_date_up_end_date,
                                "start_date":start_date,
                                "end_date":end_date,
                                "forms":form
                            }
                            return render (request, templates, context)
                # masters
                else:
                    if status == cmp_status:
                        if start_date and end_date:
                            get_all_masters_cmp_from_start_date_up_end_date=Student.objects.filter(education_level=masters_student, student_status=cmp_status, start_date=str(start_date), end_date=str(end_date))
                            templates="account/all_student.html"
                            context={
                                "get_all_masters_cmp_from_start_date_up_end_date":get_all_masters_cmp_from_start_date_up_end_date,
                                "start_date":start_date,
                                "end_date":end_date,
                                "forms":form
                            }
                            return render (request, templates, context)
                    elif status == cnt_status:
                        if start_date and end_date:
                            get_all_masters_cnt_from_start_date_up_end_date=Student.objects.filter(education_level=masters_student, student_status=cnt_status, start_date=str(start_date), end_date=str(end_date))
                            templates="account/all_student.html"
                            context={
                                "get_all_masters_cnt_from_start_date_up_end_date":get_all_masters_cnt_from_start_date_up_end_date,
                                "start_date":start_date,
                                "end_date":end_date,
                                "forms":form
                            }
                            return render (request, templates, context)
                    elif status == fnl_status:
                        if start_date and end_date:
                            get_all_masters_fnl_from_start_date_up_end_date=Student.objects.filter(education_level=masters_student, student_status=fnl_status, start_date=str(start_date), end_date=str(end_date))
                            templates="account/all_student.html"
                            context={
                                "get_all_masters_fnl_from_start_date_up_end_date":get_all_masters_fnl_from_start_date_up_end_date,
                                "start_date":start_date,
                                "end_date":end_date,
                                "forms":form
                            }
                            return render (request, templates, context)
                    else:
                        if start_date and end_date:
                            get_all_masters_pst_from_start_date_up_end_date=Student.objects.filter(education_level=masters_student, student_status=pst_status, start_date=str(start_date), end_date=str(end_date))
                            templates="account/all_student.html"
                            context={
                                "get_all_masters_pst_from_start_date_up_end_date":get_all_masters_pst_from_start_date_up_end_date,
                                "start_date":start_date,
                                "end_date":end_date,
                                "forms":form
                            }
                            return render (request, templates, context)
            elif gender  and edu_level =='' and start_date and end_date and status:
                # male
                if gender == male_student:
                    if status == cmp_status:
                        if start_date and end_date:
                            get_all_male_cmp_from_start_date_up_end_date=Student.objects.filter(gender=male_student,  student_status=cmp_status, start_date=str(start_date), end_date=str(end_date))
                            templates="account/all_student.html"
                            context={
                                "get_all_male_cmp_from_start_date_up_end_date":get_all_male_cmp_from_start_date_up_end_date,
                                "start_date":start_date,
                                "end_date":end_date,
                                "forms":form
                            }
                            return render (request, templates, context)
                    elif status == pst_status:
                        if start_date and end_date:
                            get_all_male_pst_from_start_date_up_end_date=Student.objects.filter(gender=male_student,  student_status=pst_status, start_date=str(start_date), end_date=str(end_date))
                            templates="account/all_student.html"
                            context={
                                "get_all_male_pst_from_start_date_up_end_date":get_all_male_pst_from_start_date_up_end_date,
                                "start_date":start_date,
                                "end_date":end_date,
                                "forms":form
                            }
                            return render (request, templates, context)
                    elif status == fnl_status:
                        if start_date and end_date:
                            get_all_male_cnt_from_start_date_up_end_date=Student.objects.filter(gender=male_student,  student_status=cnt_status, start_date=str(start_date), end_date=str(end_date))
                            templates="account/all_student.html"
                            context={
                                "get_all_male_cnt_from_start_date_up_end_date":get_all_male_cnt_from_start_date_up_end_date,
                                "start_date":start_date,
                                "end_date":end_date,
                                "forms":form
                            }
                            return render (request, templates, context)
                    else:
                        if start_date and end_date:
                            get_all_male_fnl_from_start_date_up_end_date=Student.objects.filter(gender=male_student,  student_status=fnl_status, start_date=str(start_date), end_date=str(end_date))
                            templates="account/all_student.html"
                            context={
                                "get_all_male_fnl_from_start_date_up_end_date":get_all_male_fnl_from_start_date_up_end_date,
                                "start_date":start_date,
                                "end_date":end_date,
                                "forms":form
                            }
                            return render (request, templates, context)
                # female
                else:
                    if status == cmp_status:
                        if start_date and end_date:
                            get_all_female_cmp_from_start_date_up_end_date=Student.objects.filter(gender=female_student,  student_status=cmp_status, start_date=str(start_date), end_date=str(end_date))
                            templates="account/all_student.html"
                            context={
                                "get_all_female_cmp_from_start_date_up_end_date":get_all_female_cmp_from_start_date_up_end_date,
                                "start_date":start_date,
                                "end_date":end_date,
                                "forms":form
                            }
                            return render (request, templates, context)
                    elif status == pst_status:
                        if start_date and end_date:
                            get_all_female_pst_from_start_date_up_end_date=Student.objects.filter(gender=female_student,  student_status=pst_status, start_date=str(start_date), end_date=str(end_date))
                            templates="account/all_student.html"
                            context={
                                "get_all_female_pst_from_start_date_up_end_date":get_all_female_pst_from_start_date_up_end_date,
                                "start_date":start_date,
                                "end_date":end_date,
                                "forms":form
                            }
                            return render (request, templates, context)
                    elif status == fnl_status:
                        if start_date and end_date:
                            get_all_female_fnl_from_start_date_up_end_date=Student.objects.filter(gender=female_student,  student_status=fnl_status, start_date=str(start_date), end_date=str(end_date))
                            templates="account/all_student.html"
                            context={
                                "get_all_female_fnl_from_start_date_up_end_date":get_all_female_fnl_from_start_date_up_end_date,
                                "start_date":start_date,
                                "end_date":end_date,
                                "forms":form
                            }
                            return render (request, templates, context)
                    else:
                        if start_date and end_date:
                            get_all_female_cnt_from_start_date_up_end_date=Student.objects.filter(gender=female_student,  student_status=cnt_status, start_date=str(start_date), end_date=str(end_date))
                            templates="account/all_student.html"
                            context={
                                "get_all_female_cnt_from_start_date_up_end_date":get_all_female_cnt_from_start_date_up_end_date,
                                "start_date":start_date,
                                "end_date":end_date,
                                "forms":form
                            }
                            return render (request, templates, context)
            elif gender  and edu_level and start_date== '' and end_date and status:
                # male
                if gender == male_student:
                    if edu_level == phd_student:
                        if status == cmp_status:
                            if end_date:
                                get_all_male_phd_cmp_end_date=Student.objects.filter(gender=male_student, education_level=phd_student,  student_status=cmp_status, end_date=str(end_date))
                                templates="account/all_student.html"
                                context={
                                    "get_all_male_phd_cmp_end_date":get_all_male_phd_cmp_end_date,
                                    "start_date":start_date,
                                    "end_date":end_date,
                                    "forms":form
                                }
                                return render (request, templates, context)
                        elif status == pst_status:
                            if end_date:
                                get_all_male_phd_pst_end_date=Student.objects.filter(gender=male_student, education_level=phd_student,  student_status=pst_status, end_date=str(end_date))
                                templates="account/all_student.html"
                                context={
                                    "get_all_male_phd_pst_end_date":get_all_male_phd_pst_end_date,
                                    "start_date":start_date,
                                    "end_date":end_date,
                                    "forms":form
                                }
                                return render (request, templates, context)
                        elif status == fnl_status:
                            if end_date:
                                get_all_male_phd_fnl_end_date=Student.objects.filter(gender=male_student, education_level=phd_student,  student_status=fnl_status, end_date=str(end_date))
                                templates="account/all_student.html"
                                context={
                                    "get_all_male_phd_fnl_end_date":get_all_male_phd_fnl_end_date,
                                    "start_date":start_date,
                                    "end_date":end_date,
                                    "forms":form
                                }
                                return render (request, templates, context)
                        else:
                            if end_date:
                                get_all_male_phd_cnt_end_date=Student.objects.filter(gender=male_student, education_level=phd_student,  student_status=cnt_status, end_date=str(end_date))
                                templates="account/all_student.html"
                                context={
                                    "get_all_male_phd_cnt_end_date":get_all_male_phd_cnt_end_date,
                                    "start_date":start_date,
                                    "end_date":end_date,
                                    "forms":form
                                }
                                return render (request, templates, context)
                    # masters
                    else:
                        if status == cnt_status:
                            if end_date:
                                get_all_male_masters_cnt_end_date=Student.objects.filter(gender=male_student, education_level=masters_student,  student_status=cnt_status, end_date=str(end_date))
                                templates="account/all_student.html"
                                context={
                                    "get_all_male_masters_cnt_end_date":get_all_male_masters_cnt_end_date,
                                    "start_date":start_date,
                                    "end_date":end_date,
                                    "forms":form
                                }
                                return render (request, templates, context)
                        elif status == fnl_status:
                            if end_date:
                                get_all_male_masters_fnl_end_date=Student.objects.filter(gender=male_student, education_level=masters_student,  student_status=fnl_status, end_date=str(end_date))
                                templates="account/all_student.html"
                                context={
                                    "get_all_male_masters_fnl_end_date":get_all_male_masters_fnl_end_date,
                                    "start_date":start_date,
                                    "end_date":end_date,
                                    "forms":form
                                }
                                return render (request, templates, context)
                        elif status == pst_status:
                            if end_date:
                                get_all_male_masters_pst_end_date=Student.objects.filter(gender=male_student, education_level=masters_student,  student_status=pst_status, end_date=str(end_date))
                                templates="account/all_student.html"
                                context={
                                    "get_all_male_masters_pst_end_date":get_all_male_masters_pst_end_date,
                                    "start_date":start_date,
                                    "end_date":end_date,
                                    "forms":form
                                }
                                return render (request, templates, context)
                        else:
                            get_all_male_masters_cmp_end_date=Student.objects.filter(gender=male_student, education_level=masters_student,  student_status=cmp_status, end_date=str(end_date))
                            templates="account/all_student.html"
                            context={
                                "get_all_male_masters_cmp_end_date":get_all_male_masters_cmp_end_date,
                                "start_date":start_date,
                                "end_date":end_date,
                                "forms":form
                            }
                            return render (request, templates, context)
                # female
                else:
                    if edu_level == phd_student:
                        if status == cmp_status:
                            if end_date:
                                get_all_female_phd_cmp_end_date=Student.objects.filter(gender=female_student, education_level=phd_student,  student_status=cmp_status, end_date=str(end_date))
                                templates="account/all_student.html"
                                context={
                                    "get_all_female_phd_cmp_end_date":get_all_female_phd_cmp_end_date,
                                    "start_date":start_date,
                                    "end_date":end_date,
                                    "forms":form
                                }
                                return render (request, templates, context)
                        elif status == pst_status:
                            if end_date:
                                get_all_female_phd_pst_end_date=Student.objects.filter(gender=female_student, education_level=phd_student,  student_status=pst_status, end_date=str(end_date))
                                templates="account/all_student.html"
                                context={
                                    "get_all_female_phd_pst_end_date":get_all_female_phd_pst_end_date,
                                    "start_date":start_date,
                                    "end_date":end_date,
                                    "forms":form
                                }
                                return render (request, templates, context)
                        elif status == fnl_status:
                            if end_date:
                                get_all_female_phd_fnl_end_date=Student.objects.filter(gender=female_student, education_level=phd_student,  student_status=fnl_status, end_date=str(end_date))
                                templates="account/all_student.html"
                                context={
                                    "get_all_female_phd_fnl_end_date":get_all_female_phd_fnl_end_date,
                                    "start_date":start_date,
                                    "end_date":end_date,
                                    "forms":form
                                }
                                return render (request, templates, context)
                        else:
                            if end_date:
                                get_all_female_phd_cnt_end_date=Student.objects.filter(gender=female_student, education_level=phd_student,  student_status=cnt_status, end_date=str(end_date))
                                templates="account/all_student.html"
                                context={
                                    "get_all_female_phd_cnt_end_date":get_all_female_phd_cnt_end_date,
                                    "start_date":start_date,
                                    "end_date":end_date,
                                    "forms":form
                                }
                                return render (request, templates, context)
                    # masters
                    else:
                        if status == cmp_status:
                            if end_date:
                                get_all_female_masters_cmp_end_date=Student.objects.filter(gender=female_student, education_level=masters_student,  student_status=cmp_status, end_date=str(end_date))
                                templates="account/all_student.html"
                                context={
                                    "get_all_female_masters_cmp_end_date":get_all_female_masters_cmp_end_dates,
                                    "start_date":start_date,
                                    "end_date":end_date,
                                    "forms":form
                                }
                                return render (request, templates, context)

                        elif status == pst_status:
                            if end_date:
                                get_all_female_masters_pst_end_date=Student.objects.filter(gender=female_student, education_level=masters_student,  student_status=pst_status, end_date=str(end_date))
                                templates="account/all_student.html"
                                context={
                                    "get_all_female_masters_pst_end_date":get_all_female_masters_pst_end_date,
                                    "start_date":start_date,
                                    "end_date":end_date,
                                    "forms":form
                                }
                                return render (request, templates, context)
                        elif status == fnl_status:
                            if end_date:
                                get_all_female_masters_fnl_end_date=Student.objects.filter(gender=female_student, education_level=masters_student,  student_status=fnl_status, end_date=str(end_date))
                                templates="account/all_student.html"
                                context={
                                    "get_all_female_masters_fnl_end_date":get_all_female_masters_fnl_end_date,
                                    "start_date":start_date,
                                    "end_date":end_date,
                                    "forms":form
                                }
                                return render (request, templates, context)
                        else:
                            if end_date:
                                get_all_female_masters_cnt_end_date=Student.objects.filter(gender=female_student, education_level=masters_student,  student_status=cnt_status, end_date=str(end_date))
                                templates="account/all_student.html"
                                context={
                                    "get_all_female_masters_cnt_end_date":get_all_female_masters_cnt_end_date,
                                    "start_date":start_date,
                                    "end_date":end_date,
                                    "forms":form
                                }
                                return render (request, templates, context)

            elif gender  and edu_level and start_date and end_date =='' and status:
                # male
                if gender == male_student:
                    if edu_level == phd_student:
                        if status == cmp_status:
                            if start_date:
                                get_all_male_phd_cmp_start_date=Student.objects.filter(gender=male_student, education_level=phd_student,  student_status=cmp_status, start_date=str(start_date))
                                templates="account/all_student.html"
                                context={
                                    "get_all_male_phd_cmp_start_date":get_all_male_phd_cmp_start_date,
                                    "start_date":start_date,
                                    "end_date":end_date,
                                    "forms":form
                                }
                                return render (request, templates, context)
                        elif status == pst_status:
                            if start_date:
                                get_all_male_phd_pst_start_date=Student.objects.filter(gender=male_student, education_level=phd_student,  student_status=pst_status, start_date=str(start_date))
                                templates="account/all_student.html"
                                context={
                                    "get_all_male_phd_pst_start_date":get_all_male_phd_pst_start_date,
                                    "start_date":start_date,
                                    "end_date":end_date,
                                    "forms":form
                                }
                                return render (request, templates, context)
                        elif status == fnl_status:
                            if start_date:
                                get_all_male_phd_fnl_start_date=Student.objects.filter(gender=male_student, education_level=phd_student,  student_status=fnl_status, start_date=str(start_date))
                                templates="account/all_student.html"
                                context={
                                    "get_all_male_phd_fnl_start_date":get_all_male_phd_fnl_start_date,
                                    "start_date":start_date,
                                    "end_date":end_date,
                                    "forms":form
                                }
                                return render (request, templates, context)
                        else:
                            pass
                    # masters
                    else:
                        if status == cmp_status:
                            if start_date:
                                get_all_male_masters_cmp_start_date=Student.objects.filter(gender=male_student, education_level=masters_student,  student_status=cmp_status, start_date=str(start_date))
                                templates="account/all_student.html"
                                context={
                                    "get_all_male_masters_cmp_start_date":get_all_male_masters_cmp_start_date,
                                    "start_date":start_date,
                                    "end_date":end_date,
                                    "forms":form
                                }
                                return render (request, templates, context)
                        elif status == pst_status:
                            if start_date:
                                get_all_male_masters_pst_start_date=Student.objects.filter(gender=male_student, education_level=masters_student,  student_status=pst_status, start_date=str(start_date))
                                templates="account/all_student.html"
                                context={
                                    "get_all_male_masters_pst_start_date":get_all_male_masters_pst_start_date,
                                    "start_date":start_date,
                                    "end_date":end_date,
                                    "forms":form
                                }
                                return render (request, templates, context)
                        elif status == fnl_status:
                            if start_date:
                                get_all_male_masters_fnl_start_date=Student.objects.filter(gender=male_student, education_level=masters_student,  student_status=fnl_status, start_date=str(start_date))
                                templates="account/all_student.html"
                                context={
                                    "get_all_male_masters_fnl_start_date":get_all_male_masters_fnl_start_date,
                                    "start_date":start_date,
                                    "end_date":end_date,
                                    "forms":form
                                }
                                return render (request, templates, context)
                        else:
                            if start_date:
                                get_all_male_masters_cnt_start_date=Student.objects.filter(gender=male_student, education_level=masters_student,  student_status=cnt_status, start_date=str(start_date))
                                templates="account/all_student.html"
                                context={
                                    "get_all_male_masters_cnt_start_date":get_all_male_masters_cnt_start_date,
                                    "start_date":start_date,
                                    "end_date":end_date,
                                    "forms":form
                                }
                                return render (request, templates, context)
                # female
                else:
                    if edu_level == phd_student:
                        if status == cmp_status:
                            if start_date:
                                get_all_female_phd_cmp_start_date=Student.objects.filter(gender=female_student, education_level=phd_student,  student_status=cmp_status, start_date=str(start_date))
                                templates="account/all_student.html"
                                context={
                                    "get_all_female_phd_cmp_start_date":get_all_female_phd_cmp_start_date,
                                    "start_date":start_date,
                                    "end_date":end_date,
                                    "forms":form
                                }
                                return render (request, templates, context)
                        elif status == pst_status:
                            if start_date:
                                get_all_female_phd_pst_start_date=Student.objects.filter(gender=female_student, education_level=phd_student,  student_status=pst_status, start_date=str(start_date))
                                templates="account/all_student.html"
                                context={
                                    "get_all_female_phd_pst_start_date":get_all_female_phd_pst_start_date,
                                    "start_date":start_date,
                                    "end_date":end_date,
                                    "forms":form
                                }
                                return render (request, templates, context)
                        elif status == fnl_status:
                            if start_date:
                                get_all_female_phd_fnl_start_date=Student.objects.filter(gender=female_student, education_level=phd_student,  student_status=fnl_status, start_date=str(start_date))
                                templates="account/all_student.html"
                                context={
                                    "get_all_female_phd_fnl_start_date":get_all_female_phd_fnl_start_date,
                                    "start_date":start_date,
                                    "end_date":end_date,
                                    "forms":form
                                }
                                return render (request, templates, context)
                        else:
                            if start_date:
                                get_all_female_phd_fnl_start_date=Student.objects.filter(gender=female_student, education_level=phd_student,  student_status=fnl_status, start_date=str(start_date))
                                templates="account/all_student.html"
                                context={
                                    "get_all_female_phd_fnl_start_date":get_all_female_phd_fnl_start_date,
                                    "start_date":start_date,
                                    "end_date":end_date,
                                    "forms":form
                                }
                                return render (request, templates, context)
                    # masters
                    else:
                        if status == cmp_status:
                            if start_date:
                                get_all_female_masters_cmp_start_date=Student.objects.filter(gender=female_student, education_level=masters_student,  student_status=cmp_status, start_date=str(start_date))
                                templates="account/all_student.html"
                                context={
                                    "get_all_female_masters_cmp_start_date":get_all_female_masters_cmp_start_date,
                                    "start_date":start_date,
                                    "end_date":end_date,
                                    "forms":form
                                }
                                return render (request, templates, context)
                        elif status == pst_status:
                            if start_date:
                                get_all_female_masters_pst_start_date=Student.objects.filter(gender=female_student, education_level=masters_student, student_status=pst_status, start_date=str(start_date))
                                templates="account/all_student.html"
                                context={
                                    "get_all_female_masters_pst_start_date":get_all_female_masters_pst_start_date,
                                    "start_date":start_date,
                                    "emd_date":end_date,
                                    "forms":form
                                }
                                return render (request, templates, context)

                        elif status == fnl_status:
                            if start_date:
                                get_female_fnl_masters_start_date=Student.objects.filter(gender=female_student, student_status=fnl_status, education_level=masters_student, start_date=str(start_date))
                                templates="account/all_student.html"
                                context={
                                    "get_female_fnl_masters_start_date":get_female_fnl_masters_start_date,
                                    "start_date":start_date,
                                    "end_date":end_date,
                                    "forms":form
                                }
                                return render (request, templates, context)
                        else:
                            if start_date:
                                get_female_cnt_masters_start_date=Student.objects.filter(gender=female_student, education_level=masters_student, student_status=cnt_status, start_date=str(start_date))
                                templates="account/all_student.html"
                                context={
                                    "get_female_cnt_masters_start_date":get_female_cnt_masters_start_date,
                                    "start_date":start_date,
                                    "end_date":end_date,
                                    "forms":form
                                }
                                return render (request, templates, context)
            elif gender  == male_student:
                if edu_level ==phd_student:
                    if status == cnt_status:
                        if start_date and end_date:
                            phd_cont_male_std=Student.objects.filter(gender="Male", education_level="PHD", student_status="continuous", start_date=str(start_date), end_date=str(end_date))
                            form=CreateStudentForm()
                            phd_cont_male_std_true =True
                            templates='account/all_student.html'
                            context={
                                'phd_cont_male_std_true':phd_cont_male_std_true,
                                'phd_cont_male_std':phd_cont_male_std,
                                'forms':form
                            }
                            return render (request, templates, context)

                        elif start_date or end_date:
                            if start_date:
                                phd_cont_male_std=Student.objects.filter(gender="Male", education_level="PHD", student_status="continuous", start_date=str(start_date))
                                form=CreateStudentForm()
                                phd_cont_male_std_true =True
                                templates='account/all_student.html'
                                context={
                                    'phd_cont_male_std_true':phd_cont_male_std_true,
                                    'phd_cont_male_std':phd_cont_male_std,
                                    'forms':form
                                }
                                return render (request, templates, context)
                            else:
                                # print("=========================")
                                phd_cont_male_std=Student.objects.filter(gender="Male", education_level="PHD", student_status="continuous",end_date=str(end_date))
                                form=CreateStudentForm()
                                phd_cont_male_std_true =True
                                templates='account/all_student.html'
                                context={
                                    'phd_cont_male_std_true':phd_cont_male_std_true,
                                    'phd_cont_male_std':phd_cont_male_std,
                                    'forms':form
                                }
                                return render (request, templates, context)
                        else:
                            # print("=========================")
                            phd_cont_male_std=Student.objects.filter(gender="Male", education_level="PHD", student_status="continuous")
                            form=CreateStudentForm()
                            phd_cont_male_std_true =True
                            templates='account/all_student.html'
                            context={
                                'phd_cont_male_std_true':phd_cont_male_std_true,
                                'phd_cont_male_std':phd_cont_male_std,
                                'forms':form
                            }
                            return render (request, templates, context)
                    elif status == cmp_status:
                        if start_date and end_date:
                            phd_cmp_male_std=Student.objects.filter(gender="Male", education_level="PHD", student_status="complete",start_date=str(start_date), end_date=str(end_date))
                            form=CreateStudentForm()
                            phd_cmp_male_std_true =True
                            templates='account/all_student.html'
                            context={
                                'phd_cmp_male_std_true':phd_cmp_male_std_true,
                                'phd_cmp_male_std':phd_cmp_male_std,
                                'forms':form
                            }
                            return render (request, templates, context)

                        elif start_date or end_date:
                            if start_date:
                                phd_cmp_male_std=Student.objects.filter(gender="Male", education_level="PHD", student_status="complete",start_date=str(start_date))
                                form=CreateStudentForm()
                                phd_cmp_male_std_true =True
                                templates='account/all_student.html'
                                context={
                                    'phd_cmp_male_std_true':phd_cmp_male_std_true,
                                    'phd_cmp_male_std':phd_cmp_male_std,
                                    'forms':form
                                }
                                return render (request, templates, context)
                            else:
                                # print("=========================")
                                phd_cmp_male_std=Student.objects.filter(gender="Male", education_level="PHD", student_status="complete", end_date=str(end_date))
                                form=CreateStudentForm()
                                phd_cmp_male_std_true =True
                                templates='account/all_student.html'
                                context={
                                    'phd_cmp_male_std_true':phd_cmp_male_std_true,
                                    'phd_cmp_male_std':phd_cmp_male_std,
                                    'forms':form
                                }
                                return render (request, templates, context)
                        else:
                            phd_cmp_male_std=Student.objects.filter(gender="Male", education_level="PHD", student_status="complete")
                            form=CreateStudentForm()
                            phd_cmp_male_std_true =True
                            templates='account/all_student.html'
                            context={
                                'phd_cmp_male_std_true':phd_cmp_male_std_true,
                                'phd_cmp_male_std':phd_cmp_male_std,
                                'forms':form
                            }
                            return render (request, templates, context)
                    elif status == pst_status:
                        if start_date and end_date:
                            phd_pst_male_std=Student.objects.filter(gender="Male", education_level="PHD", student_status="postpone",start_date=str(start_date), end_date=str(end_date))
                            form=CreateStudentForm()
                            phd_pst_male_std_true = True
                            templates='account/all_student.html'
                            context={
                                'phd_pst_male_std_true':phd_pst_male_std_true,
                                'phd_pst_male_std':phd_pst_male_std,
                                'forms':form
                            }
                            return render (request, templates, context)
                        elif start_date or end_date:
                            if start_date:
                                phd_pst_male_std=Student.objects.filter(gender="Male", education_level="PHD", student_status="postpone",start_date=str(start_date))
                                form=CreateStudentForm()
                                phd_pst_male_std_true = True
                                templates='account/all_student.html'
                                context={
                                    'phd_pst_male_std_true':phd_pst_male_std_true,
                                    'phd_pst_male_std':phd_pst_male_std,
                                    'forms':form
                                }
                                return render (request, templates, context)
                            else:
                                # print("=========================")
                                phd_pst_male_std=Student.objects.filter(gender="Male", education_level="PHD", student_status="postpone", end_date=str(end_date))
                                form=CreateStudentForm()
                                phd_pst_male_std_true = True
                                templates='account/all_student.html'
                                context={
                                    'phd_pst_male_std_true':phd_pst_male_std_true,
                                    'phd_pst_male_std':phd_pst_male_std,
                                    'forms':form
                                }
                                return render (request, templates, context)
                        else:
                            phd_pst_male_std=Student.objects.filter(gender="Male", education_level="PHD", student_status="postpone")
                            form=CreateStudentForm()
                            phd_pst_male_std_true = True
                            templates='account/all_student.html'
                            context={
                                'phd_pst_male_std_true':phd_pst_male_std_true,
                                'phd_pst_male_std':phd_pst_male_std,
                                'forms':form
                            }
                            return render (request, templates, context)

                    elif status == fnl_status:
                        if start_date and end_date:
                            phd_fnl_male_std=Student.objects.filter(gender="Male", education_level="PHD", student_status="final",start_date=str(start_date), end_date=str(end_date))
                            form=CreateStudentForm()
                            phd_fnl_male_std_true = True
                            templates='account/all_student.html'
                            context={
                                'phd_fnl_male_std_true':phd_fnl_male_std_true,
                                'phd_fnl_male_std':phd_fnl_male_std,
                                'forms':form
                            }
                            return render (request, templates, context)
                        elif start_date or end_date:
                            if start_date:
                                phd_fnl_male_std=Student.objects.filter(gender="Male", education_level="PHD", student_status="final",start_date=str(start_date))
                                form=CreateStudentForm()
                                phd_fnl_male_std_true = True
                                templates='account/all_student.html'
                                context={
                                    'phd_fnl_male_std_true':phd_fnl_male_std_true,
                                    'phd_fnl_male_std':phd_fnl_male_std,
                                    'forms':form
                                }
                                return render (request, templates, context)
                            else:
                                # print("=========================")
                                phd_fnl_male_std=Student.objects.filter(gender="Male", education_level="PHD", student_status="final", end_date=str(end_date))
                                form=CreateStudentForm()
                                phd_fnl_male_std_true = True
                                templates='account/all_student.html'
                                context={
                                    'phd_fnl_male_std_true':phd_fnl_male_std_true,
                                    'phd_fnl_male_std':phd_fnl_male_std,
                                    'forms':form
                                }
                                return render (request, templates, context)
                        else:
                            phd_fnl_male_std=Student.objects.filter(gender="Male", education_level="PHD", student_status="final")
                            form=CreateStudentForm()
                            phd_fnl_male_std_true = True
                            templates='account/all_student.html'
                            context={
                                'phd_fnl_male_std_true':phd_fnl_male_std_true,
                                'phd_fnl_male_std':phd_fnl_male_std,
                                'forms':form
                            }
                            return render (request, templates, context)

                elif  edu_level == masters_student:
                    if status == cnt_status:
                        if start_date and end_date:
                            mst_cnt_male_std=Student.objects.filter(gender="Male", education_level="MASTERS", student_status="continuous",start_date=str(start_date), end_date=str(end_date))
                            form=CreateStudentForm()
                            mst_cnt_male_std_true = True
                            templates='account/all_student.html'
                            context={
                                'mst_cnt_male_std_true':mst_cnt_male_std_true,
                                'mst_cnt_male_std':mst_cnt_male_std,
                                'forms':form
                            }
                            return render (request, templates, context)
                        elif start_date or end_date:
                            if start_date:
                                mst_cnt_male_std=Student.objects.filter(gender="Male", education_level="MASTERS", student_status="continuous",start_date=str(start_date))
                                form=CreateStudentForm()
                                mst_cnt_male_std_true = True
                                templates='account/all_student.html'
                                context={
                                    'mst_cnt_male_std_true':mst_cnt_male_std_true,
                                    'mst_cnt_male_std':mst_cnt_male_std,
                                    'forms':form
                                }
                                return render (request, templates, context)
                            else:
                                mst_cnt_male_std=Student.objects.filter(gender="Male", education_level="MASTERS", student_status="continuous", end_date=str(end_date))
                                form=CreateStudentForm()
                                mst_cnt_male_std_true = True
                                templates='account/all_student.html'
                                context={
                                    'mst_cnt_male_std_true':mst_cnt_male_std_true,
                                    'mst_cnt_male_std':mst_cnt_male_std,
                                    'forms':form
                                }
                                return render (request, templates, context)
                        else:
                            mst_cnt_male_std=Student.objects.filter(gender="Male", education_level="MASTERS", student_status="continuous")
                            form=CreateStudentForm()
                            mst_cnt_male_std_true = True
                            templates='account/all_student.html'
                            context={
                                'mst_cnt_male_std_true':mst_cnt_male_std_true,
                                'mst_cnt_male_std':mst_cnt_male_std,
                                'forms':form
                            }
                            return render (request, templates, context)

                    elif status == cmp_status:
                        if start_date and end_date:
                            mst_cmp_male_std=Student.objects.filter(gender="Male", education_level="MASTERS", student_status="complete",start_date=str(start_date), end_date=str(end_date))
                            form=CreateStudentForm()
                            mst_cmp_male_std_true = True
                            templates='account/all_student.html'
                            context={
                                'mst_cmp_male_std_true':mst_cmp_male_std_true,
                                'mst_cmp_male_std':mst_cmp_male_std,
                                'forms':form
                            }
                            return render (request, templates, context)
                        elif start_date or end_date:
                            if start_date:
                                mst_cmp_male_std=Student.objects.filter(gender="Male", education_level="MASTERS", student_status="complete",start_date=str(start_date))
                                form=CreateStudentForm()
                                mst_cmp_male_std_true = True
                                templates='account/all_student.html'
                                context={
                                    'mst_cmp_male_std_true':mst_cmp_male_std_true,
                                    'mst_cmp_male_std':mst_cmp_male_std,
                                    'forms':form
                                }
                                return render (request, templates, context)
                            else:
                                mst_cmp_male_std=Student.objects.filter(gender="Male", education_level="MASTERS", student_status="complete", end_date=str(end_date))
                                form=CreateStudentForm()
                                mst_cmp_male_std_true = True
                                templates='account/all_student.html'
                                context={
                                    'mst_cmp_male_std_true':mst_cmp_male_std_true,
                                    'mst_cmp_male_std':mst_cmp_male_std,
                                    'forms':form
                                }
                                return render (request, templates, context)
                        else:
                            mst_cmp_male_std=Student.objects.filter(gender="Male", education_level="MASTERS", student_status="complete")
                            form=CreateStudentForm()
                            mst_cmp_male_std_true = True
                            templates='account/all_student.html'
                            context={
                                'mst_cmp_male_std_true':mst_cmp_male_std_true,
                                'mst_cmp_male_std':mst_cmp_male_std,
                                'forms':form
                            }
                            return render (request, templates, context)

                    elif status == pst_status:
                        if start_date and end_date:
                            mst_pst_male_std=Student.objects.filter(gender="Male", education_level="MASTERS", student_status="postpone",start_date=str(start_date), end_date=str(end_date))
                            form=CreateStudentForm()
                            mst_pst_male_std_true = True
                            templates='account/all_student.html'
                            context={
                                'mst_pst_male_std_true':mst_pst_male_std_true,
                                'mst_pst_male_std':mst_pst_male_std,
                                'forms':form
                            }
                            return render (request, templates, context)
                        elif start_date or end_date:
                            if start_date:
                                mst_pst_male_std=Student.objects.filter(gender="Male", education_level="MASTERS", student_status="postpone",start_date=str(start_date))
                                form=CreateStudentForm()
                                mst_pst_male_std_true = True
                                templates='account/all_student.html'
                                context={
                                    'mst_pst_male_std_true':mst_pst_male_std_true,
                                    'mst_pst_male_std':mst_pst_male_std,
                                    'forms':form
                                }
                                return render (request, templates, context)
                            else:
                                mst_pst_male_std=Student.objects.filter(gender="Male", education_level="MASTERS", student_status="postpone", end_date=str(end_date))
                                form=CreateStudentForm()
                                mst_pst_male_std_true = True
                                templates='account/all_student.html'
                                context={
                                    'mst_pst_male_std_true':mst_pst_male_std_true,
                                    'mst_pst_male_std':mst_pst_male_std,
                                    'forms':form
                                }
                                return render (request, templates, context)
                        else:
                            mst_pst_male_std=Student.objects.filter(gender="Male", education_level="MASTERS", student_status="postpone")
                            form=CreateStudentForm()
                            mst_pst_male_std_true = True
                            templates='account/all_student.html'
                            context={
                                'mst_pst_male_std_true':mst_pst_male_std_true,
                                'mst_pst_male_std':mst_pst_male_std,
                                'forms':form
                            }
                            return render (request, templates, context)

                    elif status == fnl_status:
                        if start_date and end_date:
                            mst_fnl_male_std=Student.objects.filter(gender="Male", education_level="MASTERS", student_status="final",start_date=str(start_date), end_date=str(end_date))
                            form=CreateStudentForm()
                            mst_fnl_male_std_true = True
                            templates='account/all_student.html'
                            context={
                                'mst_fnl_male_std_true':mst_fnl_male_std_true,
                                'mst_fnl_male_std':mst_fnl_male_std,
                                'forms':form
                            }
                            return render (request, templates, context)
                        elif start_date or end_date:
                            if start_date:
                                mst_fnl_male_std=Student.objects.filter(gender="Male", education_level="MASTERS", student_status="final",start_date=str(start_date))
                                form=CreateStudentForm()
                                mst_fnl_male_std_true = True
                                templates='account/all_student.html'
                                context={
                                    'mst_fnl_male_std_true':mst_fnl_male_std_true,
                                    'mst_fnl_male_std':mst_fnl_male_std,
                                    'forms':form
                                }
                                return render (request, templates, context)
                            else:
                                mst_fnl_male_std=Student.objects.filter(gender="Male", education_level="MASTERS", student_status="final", end_date=str(end_date))
                                form=CreateStudentForm()
                                mst_fnl_male_std_true = True
                                templates='account/all_student.html'
                                context={
                                    'mst_fnl_male_std_true':mst_fnl_male_std_true,
                                    'mst_fnl_male_std':mst_fnl_male_std,
                                    'forms':form
                                }
                                return render (request, templates, context)
                        else:
                            mst_fnl_male_std=Student.objects.filter(gender="Male", education_level="MASTERS", student_status="final")
                            form=CreateStudentForm()
                            mst_fnl_male_std_true = True
                            templates='account/all_student.html'
                            context={
                                'mst_fnl_male_std_true':mst_fnl_male_std_true,
                                'mst_fnl_male_std':mst_fnl_male_std,
                                'forms':form
                            }
                            return render (request, templates, context)
            else:
                if edu_level ==phd_student:
                    if status == cnt_status:
                        if start_date and end_date:
                            phd_cont_female_std=Student.objects.filter(gender="Female", education_level="PHD", student_status="continuous", start_date=str(start_date), end_date=str(end_date))
                            form=CreateStudentForm()
                            phd_cont_female_std_true =True
                            templates='account/all_student.html'
                            context={
                                'phd_cont_female_std_true':phd_cont_female_std_true,
                                'phd_cont_female_std':phd_cont_female_std,
                                'forms':form
                            }
                            return render (request, templates, context)

                        elif start_date or end_date:
                            if start_date:
                                phd_cont_female_std=Student.objects.filter(gender="Female", education_level="PHD", student_status="continuous", start_date=str(start_date))
                                form=CreateStudentForm()
                                phd_cont_female_std_true =True
                                templates='account/all_student.html'
                                context={
                                    'phd_cont_female_std_true':phd_cont_female_std_true,
                                    'phd_cont_female_std':phd_cont_female_std,
                                    'forms':form
                                }
                                return render (request, templates, context)
                            else:
                                # print("=========================")
                                phd_cont_female_std=Student.objects.filter(gender="Female", education_level="PHD", student_status="continuous", end_date=str(end_date))
                                form=CreateStudentForm()
                                phd_cont_female_std_true =True
                                templates='account/all_student.html'
                                context={
                                    'phd_cont_female_std_true':phd_cont_female_std_true,
                                    'phd_cont_female_std':phd_cont_female_std,
                                    'forms':form
                                }
                                return render (request, templates, context)
                        else:
                            # print("=========================")
                            phd_cont_female_std=Student.objects.filter(gender="Female", education_level="PHD", student_status="continuous")
                            form=CreateStudentForm()
                            phd_cont_female_std_true =True
                            templates='account/all_student.html'
                            context={
                                'phd_cont_female_std_true':phd_cont_female_std_true,
                                'phd_cont_female_std':phd_cont_female_std,
                                'forms':form
                            }
                            return render (request, templates, context)

                    elif status == cmp_status:
                        if start_date and end_date:
                            # print("=========================")
                            phd_cmp_female_std=Student.objects.filter(gender="Female", education_level="PHD", student_status="complete",start_date=str(start_date),end_date=str(end_date))
                            form=CreateStudentForm()
                            phd_cmp_female_std_true =True
                            templates='account/all_student.html'
                            context={
                                'phd_cmp_female_std_true':phd_cmp_female_std_true,
                                'phd_cmp_female_std':phd_cmp_female_std,
                                'forms':form
                            }
                            return render (request, templates, context)

                        elif start_date or end_date:
                            if start_date:
                                phd_cmp_female_std=Student.objects.filter(gender="Female", education_level="PHD", student_status="complete",start_date=str(start_date))
                                form=CreateStudentForm()
                                phd_cmp_female_std_true =True
                                templates='account/all_student.html'
                                context={
                                    'phd_cmp_female_std_true':phd_cmp_female_std_true,
                                    'phd_cmp_female_std':phd_cmp_female_std,
                                    'forms':form
                                }
                                return render (request, templates, context)
                            else:
                                # print("=========================")
                                phd_cmp_female_std=Student.objects.filter(gender="Female", education_level="PHD", student_status="complete",end_date=str(end_date))
                                form=CreateStudentForm()
                                phd_cmp_female_std_true =True
                                templates='account/all_student.html'
                                context={
                                    'phd_cmp_female_std_true':phd_cmp_female_std_true,
                                    'phd_cmp_female_std':phd_cmp_female_std,
                                    'forms':form
                                }
                                return render (request, templates, context)
                        else:
                            # print("=========================")
                            phd_cmp_female_std=Student.objects.filter(gender="Female", education_level="PHD", student_status="complete")
                            form=CreateStudentForm()
                            phd_cmp_female_std_true =True
                            templates='account/all_student.html'
                            context={
                                'phd_cmp_female_std_true':phd_cmp_female_std_true,
                                'phd_cmp_female_std':phd_cmp_female_std,
                                'forms':form
                            }
                            return render (request, templates, context)
                    elif status == pst_status:
                        if start_date and end_date:
                            # print("=========================")
                            phd_pst_female_std=Student.objects.filter(gender="Female", education_level="PHD", student_status="postpone",start_date=str(start_date),end_date=str(end_date))
                            form=CreateStudentForm()
                            phd_pst_female_std_true =True
                            templates='account/all_student.html'
                            context={
                                'phd_pst_male_std_female_std_true':phd_pst_female_std_true,
                                'phd_pst_female_std':phd_pst_female_std,
                                'forms':form
                            }
                            return render (request, templates, context)

                        elif start_date or end_date:
                            if start_date:
                                phd_pst_female_std=Student.objects.filter(gender="Female", education_level="PHD", student_status="postpone",start_date=str(start_date))
                                form=CreateStudentForm()
                                phd_pst_female_std_true =True
                                templates='account/all_student.html'
                                context={
                                    'phd_pst_male_std_female_std_true':phd_pst_female_std_true,
                                    'phd_pst_female_std':phd_pst_female_std,
                                    'forms':form
                                }
                                return render (request, templates, context)
                            else:
                                # print("=========================")
                                phd_pst_female_std=Student.objects.filter(gender="Female", education_level="PHD", student_status="postpone",end_date=str(end_date))
                                form=CreateStudentForm()
                                phd_pst_female_std_true =True
                                templates='account/all_student.html'
                                context={
                                    'phd_pst_male_std_female_std_true':phd_pst_female_std_true,
                                    'phd_pst_female_std':phd_pst_female_std,
                                    'forms':form
                                }
                                return render (request, templates, context)
                        else:
                            # print("=========================")
                            phd_pst_female_std=Student.objects.filter(gender="Female", education_level="PHD", student_status="postpone")
                            form=CreateStudentForm()
                            phd_pst_female_std_true =True
                            templates='account/all_student.html'
                            context={
                                'phd_pst_male_std_female_std_true':phd_pst_female_std_true,
                                'phd_pst_female_std':phd_pst_female_std,
                                'forms':form
                            }
                            return render (request, templates, context)

                    elif status == fnl_status:
                        if start_date and end_date:
                            # print("=========================")
                            phd_fnl_female_std=Student.objects.filter(gender="Female", education_level="PHD", student_status="final",start_date=str(start_date),end_date=str(end_date))
                            form=CreateStudentForm()
                            phd_fnl_female_std_true = True
                            templates='account/all_student.html'
                            context={
                                'phd_fnl_female_std_true':phd_fnl_female_std_true,
                                'phd_fnl_female_std':phd_fnl_female_std,
                                'forms':form
                            }
                            return render (request, templates, context)

                        elif start_date or end_date:
                            if start_date:
                                phd_fnl_female_std=Student.objects.filter(gender="Female", education_level="PHD", student_status="final",start_date=str(start_date))
                                form=CreateStudentForm()
                                phd_fnl_female_std_true =True
                                templates='account/all_student.html'
                                context={
                                    'phd_fnl_male_std_female_std_true':phd_fnl_female_std_true,
                                    'phd_fnl_female_std':phd_fnl_female_std,
                                    'forms':form
                                }
                                return render (request, templates, context)
                            else:
                                # print("=========================")
                                phd_fnl_female_std=Student.objects.filter(gender="Female", education_level="PHD", student_status="final",end_date=str(end_date))
                                form=CreateStudentForm()
                                phd_fnl_female_std_true =True
                                templates='account/all_student.html'
                                context={
                                    'phd_fnl_male_std_female_std_true':phd_fnl_female_std_true,
                                    'phd_fnl_female_std':phd_fnl_female_std,
                                    'forms':form
                                }
                                return render (request, templates, context)
                        else:
                            # print("=========================")
                            phd_fnl_female_std=Student.objects.filter(gender="Female", education_level="PHD", student_status="final")
                            form=CreateStudentForm()
                            phd_fnl_female_std_true =True
                            templates='account/all_student.html'
                            context={
                                'phd_fnl_male_std_female_std_true':phd_fnl_female_std_true,
                                'phd_fnl_female_std':phd_fnl_female_std,
                                'forms':form
                            }
                            return render (request, templates, context)

                elif  edu_level == masters_student:
                    if status == cnt_status:
                        if start_date and end_date:
                            # print("=========================")
                            mst_cnt_female_std=Student.objects.filter(gender="Female", education_level="MASTERS", student_status="continuous",start_date=str(start_date), end_date=str(end_date))
                            form=CreateStudentForm()
                            mst_cnt_female_std_true = True
                            templates='account/all_student.html'
                            context={
                                'mst_cnt_female_std_true':mst_cnt_female_std_true,
                                'mst_cnt_female_std':mst_cnt_female_std,
                                'forms':form
                            }
                            return render (request, templates, context)

                        elif start_date or end_date:
                            if start_date:
                                mst_cnt_female_std=Student.objects.filter(gender="Female", education_level="MASTERS", student_status="continuous",start_date=str(start_date))
                                form=CreateStudentForm()
                                mst_cnt_female_std_true = True
                                templates='account/all_student.html'
                                context={
                                    'mst_cnt_female_std_true':mst_cnt_female_std_true,
                                    'mst_cnt_female_std':mst_cnt_female_std,
                                    'forms':form
                                }
                                return render (request, templates, context)
                            else:
                                # print("=========================")
                                mst_cnt_female_std=Student.objects.filter(gender="Female", education_level="MASTERS", student_status="continuous", end_date=str(end_date))
                                form=CreateStudentForm()
                                mst_cnt_female_std_true = True
                                templates='account/all_student.html'
                                context={
                                    'mst_cnt_female_std_true':mst_cnt_female_std_true,
                                    'mst_cnt_female_std':mst_cnt_female_std,
                                    'forms':form
                                }
                                return render (request, templates, context)
                        else:
                            # print("=========================")
                            mst_cnt_female_std=Student.objects.filter(gender="Female", education_level="MASTERS", student_status="continuous")
                            form=CreateStudentForm()
                            mst_cnt_female_std_true = True
                            templates='account/all_student.html'
                            context={
                                'mst_cnt_female_std_true':mst_cnt_female_std_true,
                                'mst_cnt_female_std':mst_cnt_female_std,
                                'forms':form
                            }
                            return render (request, templates, context)

                    elif status == cmp_status:
                        if start_date and end_date:
                            # print("=========================")
                            mst_cmp_female_std=Student.objects.filter(gender="Female", education_level="MASTERS", student_status="complete",start_date=str(start_date), end_date=str(end_date))
                            form=CreateStudentForm()
                            mst_cmp_female_std_true = True
                            templates = 'account/all_student.html'
                            context={
                                'mst_cmp_female_std_true':mst_cmp_female_std_true,
                                'mst_cmp_female_std':mst_cmp_female_std,
                                'forms':form
                            }
                            return render (request, templates, context)
                        elif start_date or end_date:
                            if start_date:
                                mst_cmp_female_std=Student.objects.filter(gender="Female", education_level="MASTERS", student_status="complete",start_date=str(start_date))
                                form=CreateStudentForm()
                                mst_cmp_female_std_true = True
                                templates = 'account/all_student.html'
                                context={
                                    'mst_cmp_female_std_true':mst_cmp_female_std_true,
                                    'mst_cmp_female_std':mst_cmp_female_std,
                                    'forms':form
                                }
                                return render (request, templates, context)
                            else:
                                # print("=========================")
                                mst_cmp_female_std=Student.objects.filter(gender="Female", education_level="MASTERS", student_status="complete",start_date=str(start_date), end_date=str(end_date))
                                form=CreateStudentForm()
                                mst_cmp_female_std_true = True
                                templates = 'account/all_student.html'
                                context={
                                    'mst_cmp_female_std_true':mst_cmp_female_std_true,
                                    'mst_cmp_female_std':mst_cmp_female_std,
                                    'forms':form
                                }
                                return render (request, templates, context)
                        else:
                            # print("=========================")
                            mst_cmp_female_std=Student.objects.filter(gender="Female", education_level="MASTERS", student_status="complete")
                            form=CreateStudentForm()
                            mst_cmp_female_std_true = True
                            templates = 'account/all_student.html'
                            context={
                                'mst_cmp_female_std_true':mst_cmp_female_std_true,
                                'mst_cmp_female_std':mst_cmp_female_std,
                                'forms':form
                            }
                            return render (request, templates, context)
                    elif status == pst_status:
                        if start_date and end_date:
                            # print("=========================")
                            mst_pst_female_std=Student.objects.filter(gender="Female", education_level="MASTERS", student_status="postpone",start_date=str(start_date), end_date=str(end_date))
                            form=CreateStudentForm()
                            mst_pst_female_std_true = True
                            templates='account/all_student.html'
                            context={
                                'mst_pst_female_std_true':mst_pst_female_std_true,
                                'mst_pst_female_std':mst_pst_female_std,
                                'forms':form
                            }
                            return render (request, templates, context)

                        elif start_date or end_date:
                            if start_date:
                                mst_pst_female_std=Student.objects.filter(gender="Female", education_level="MASTERS", student_status="postpone",start_date=str(start_date))
                                form=CreateStudentForm()
                                mst_pst_female_std_true = True
                                templates='account/all_student.html'
                                context={
                                    'mst_pst_female_std_true':mst_pst_female_std_true,
                                    'mst_pst_female_std':mst_pst_female_std,
                                    'forms':form
                                }
                                return render (request, templates, context)
                            else:
                                # print("=========================")
                                mst_pst_female_std=Student.objects.filter(gender="Female", education_level="MASTERS", student_status="postpone", end_date=str(end_date))
                                form=CreateStudentForm()
                                mst_pst_female_std_true = True
                                templates='account/all_student.html'
                                context={
                                    'mst_pst_female_std_true':mst_pst_female_std_true,
                                    'mst_pst_female_std':mst_pst_female_std,
                                    'forms':form
                                }
                                return render (request, templates, context)
                        else:
                            # print("=========================")
                            mst_pst_female_std=Student.objects.filter(gender="Female", education_level="MASTERS", student_status="postpone")
                            form=CreateStudentForm()
                            mst_pst_female_std_true = True
                            templates='account/all_student.html'
                            context={
                                'mst_pst_female_std_true':mst_pst_female_std_true,
                                'mst_pst_female_std':mst_pst_female_std,
                                'forms':form
                            }
                            return render (request, templates, context)

                    elif status == fnl_status:
                        if start_date and end_date:
                            # print("=========================")
                            mst_fnl_female_std=Student.objects.filter(gender="Female", education_level="MASTERS", student_status="final",start_date=str(start_date), end_date=str(end_date))
                            form=CreateStudentForm()
                            mst_fnl_female_std_true = True
                            templates='account/all_student.html'
                            context={
                                'mst_fnl_female_std_true':mst_fnl_female_std_true,
                                'mst_fnl_female_std':mst_fnl_female_std,
                                'forms':form
                            }
                            return render (request, templates, context)

                        elif start_date or end_date:
                            if start_date:
                                mst_fnl_female_std=Student.objects.filter(gender="Female", education_level="MASTERS", student_status="final",start_date=str(start_date))
                                form=CreateStudentForm()
                                mst_fnl_female_std_true = True
                                templates='account/all_student.html'
                                context={
                                    'mst_fnl_female_std_true':mst_fnl_female_std_true,
                                    'mst_fnl_female_std':mst_fnl_female_std,
                                    'forms':form
                                }
                                return render (request, templates, context)
                            else:
                                # print("=========================")
                                mst_fnl_female_std=Student.objects.filter(gender="Female", education_level="MASTERS", student_status="final", end_date=str(end_date))
                                form=CreateStudentForm()
                                mst_fnl_female_std_true = True
                                templates='account/all_student.html'
                                context={
                                    'mst_fnl_female_std_true':mst_fnl_female_std_true,
                                    'mst_fnl_female_std':mst_fnl_female_std,
                                    'forms':form
                                }
                                return render (request, templates, context)
                        else:
                            # print("=========================")
                            mst_fnl_female_std=Student.objects.filter(gender="Female", education_level="MASTERS", student_status="final")
                            form=CreateStudentForm()
                            mst_fnl_female_std_true = True
                            templates='account/all_student.html'
                            context={
                                'mst_fnl_female_std_true':mst_fnl_female_std_true,
                                'mst_fnl_female_std':mst_fnl_female_std,
                                'forms':form
                            }
                            return render (request, templates, context)

        else:
            get_all_students= Student.objects.all().order_by('-id')
            templates = 'account/all_student.html'
            context={
                "get_all_students": get_all_students,
                "forms":form
            }
            return render(request, templates, context)
    except:
        return messages.info(request, "Bad request")

@cache_control(no_cache=True, must_revalidate=True, privacy=True, no_store=False)
@login_required(login_url='auth')
def AddCollegeView(request):
    create_college_form = forms.AddCollegeForm()
    if request.method == 'POST':
        form = forms.AddCollegeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'New College was Added!')
            return redirect('add_student')
    else:
        templates = 'account/add_student.html'
        context = {
        "create_college_form":create_college_form
        }
        return render(request, templates, context)

@cache_control(no_cache=True, must_revalidate=True, privacy=True, no_store=False)
@login_required(login_url='auth')
def AddCourseView(request):
    create_course_form = forms.CreateCourseForm()
    if request.method == 'POST':
        form = forms.CreateCourseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Course was created! successfull ')
            return redirect('add_student')
    else:
        templates = 'account/add_student.html'
        context = {
        "create_course_form":create_course_form
        }
        return render(request, templates, context)

@cache_control(no_cache=True, must_revalidate=True, privacy=True, no_store=False)
@login_required(login_url='auth')
def AddModuleView(request):
    create_module_form = forms.CreateModuleForm()
    if request.method == 'POST':
        form = forms.CreateModuleForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Module was created! successfull ')
            return redirect('add_student')
    else:
        templates = 'account/add_student.html'
        context = {
        "create_module_form":create_module_form
        }
        return render(request, templates, context)

@cache_control(no_cache=True, must_revalidate=True, privacy=True, no_store=False)
@login_required(login_url='auth')
def UpdateStudentView(request,pk):
    if request.method == 'POST':
        form = CreateStudentForm(request.POST)
        if form.is_valid():
            student = Student.objects.get(id=pk)
            student.delete()
            form.save()
            return redirect("all_std")
        else:
            messages.info(request, 'update failed! please enter valid input')
            return redirect('update', pk)
    else:
        student = Student.objects.get(id=pk)
        form = CreateStudentForm(instance=student)
        templates = 'account/update_student.html'
        context = {
         "forms":form
        }

        return render(request, templates, context)

@cache_control(no_cache=True, must_revalidate=True, privacy=True, no_store=False)
@login_required(login_url='auth')
def DeleteStudentView(request, pk):
    student=Student.objects.get(id=pk)
    student.delete()
    messages.info(request, "success student deleted !!")
    return redirect('all_std')

############# DOWNLOAD CSV FILES
@cache_control(no_cache=True, must_revalidate=True, privacy=True, no_store=False)
@login_required(login_url='auth')
def DownloadAllView(request):
    response = HttpResponse(content_type='text/csv')
    get_college_name = College.objects.all()
    get_course_name = Course.objects.all()
    writer = csv.writer(response)
    writer.writerow(['firstname','middle_name','surname','email','dob','age','gender','contact','nationality','registration_number','programme_name','start_date','end_date','college','education_level','student_status'
    ])

    for student in Student.objects.all().values_list('firstname','middle_name','surname','email','dob','age','gender','contact','nationality','registration_number','programme_name','start_date','end_date','college','education_level','student_status'):
        if student[10] and student[13] :
            course=Course.objects.get(id=student[10])
            college = College.objects.get(id=student[13])
            new_list=list(student)
            new_list[10]=course
            new_list[13]=college
            writer.writerow(new_list)
        else:
            writer.writerow(student)

    response['Content-Disposition'] = 'attachment;filename="list_of_student.csv"'
    return response

@cache_control(no_cache=True, must_revalidate=True, privacy=True, no_store=False)
@login_required(login_url='auth')
def DownloadPhdView(request):
    response = HttpResponse(content_type='text/csv')
    writer = csv.writer(response)
    writer.writerow(
    [
    'firstname','middle_name','surname','email','dob','age','gender','contact','nationality','registration_number','programme_name','start_date','end_date','college','education_level','student_status'
    ]
    )

    for phd_student in Student.objects.filter(education_level='PHD').values_list('firstname','middle_name','surname','email','dob','age','gender','contact','nationality','registration_number','programme_name','start_date','end_date','college','education_level','student_status'):
        if phd_student[10] and phd_student[13] :
            course=Course.objects.get(id=phd_student[10])
            college = College.objects.get(id=phd_student[13])
            new_list=list(phd_student)
            new_list[10]=course
            new_list[13]=college
            writer.writerow(new_list)
        else:
            writer.writerow(phd_student)

    response['Content-Disposition'] = 'attachment;filename="phd_all_student.csv"'
    return response

@cache_control(no_cache=True, must_revalidate=True, privacy=True, no_store=False)
@login_required(login_url='auth')
def DownloadMastersView(request):
    response = HttpResponse(content_type='text/csv')
    writer = csv.writer(response)
    writer.writerow(['firstname','middle_name','surname','email','dob','age','gender','contact','nationality','registration_number','programme_name','start_date','end_date','college','education_level','student_status'])

    for masters_student in Student.objects.filter(education_level='MASTERS').values_list('firstname','middle_name','surname','email','dob','age','gender','contact','nationality','registration_number','programme_name','start_date','end_date','college','education_level','student_status'):
        if masters_student[10] and masters_student[13] :
            course=Course.objects.get(id=masters_student[10])
            college = College.objects.get(id=masters_student[13])
            new_list=list(masters_student)
            new_list[10]=course
            new_list[13]=college
            writer.writerow(new_list)
        else:
            writer.writerow(masters_student)
    response['Content-Disposition'] = 'attachment;filename="all_masters_student.csv"'
    return response

################# DOWNLOAD ONLY MALE PHD & MASTERS
def DownloadPhdContMaleView(request):
    response = HttpResponse(content_type='text/csv')
    writer = csv.writer(response)
    writer.writerow(
    [
    'firstname','middle_name','surname','email','dob','age','gender','contact','nationality','registration_number','programme_name','start_date','end_date','college','education_level','student_status'
    ]
    )

    for phd_student in Student.objects.filter(education_level='PHD', gender='Male', student_status='continuous').values_list('firstname','middle_name','surname','email','dob','age','gender','contact','nationality','registration_number','programme_name','start_date','end_date','college','education_level','student_status'):
        if phd_student[10] and phd_student[13] :
            course=Course.objects.get(id=phd_student[10])
            college = College.objects.get(id=phd_student[13])
            new_list=list(phd_student)
            new_list[10]=course
            new_list[13]=college
            writer.writerow(new_list)
        else:
            writer.writerow(phd_student)

    response['Content-Disposition'] = 'attachment;filename="phd_continuous_male_student.csv"'
    return response

def DownloadPhdCmpMaleView(request):
    response = HttpResponse(content_type='text/csv')
    writer = csv.writer(response)
    writer.writerow(
    [
    'firstname','middle_name','surname','email','dob','age','gender','contact','nationality','registration_number','programme_name','start_date','end_date','college','education_level','student_status'
    ]
    )

    for phd_student in Student.objects.filter(education_level='PHD', gender='Male', student_status='complete').values_list('firstname','middle_name','surname','email','dob','age','gender','contact','nationality','registration_number','programme_name','start_date','end_date','college','education_level','student_status'):
        if phd_student[10] and phd_student[13] :
            course=Course.objects.get(id=phd_student[10])
            college = College.objects.get(id=phd_student[13])
            new_list=list(phd_student)
            new_list[10]=course
            new_list[13]=college
            writer.writerow(new_list)
        else:
            writer.writerow(phd_student)

    response['Content-Disposition'] = 'attachment;filename="phd_completed_male_student.csv"'
    return response
def DownloadPhdPstMaleView(request):
    response = HttpResponse(content_type='text/csv')
    writer = csv.writer(response)
    writer.writerow(
    [
    'firstname','middle_name','surname','email','dob','age','gender','contact','nationality','registration_number','programme_name','start_date','end_date','college','education_level','student_status'
    ]
    )

    for phd_student in Student.objects.filter(education_level='PHD', gender='Male', student_status='postpone').values_list('firstname','middle_name','surname','email','dob','age','gender','contact','nationality','registration_number','programme_name','start_date','end_date','college','education_level','student_status'):
        if phd_student[10] and phd_student[13] :
            course=Course.objects.get(id=phd_student[10])
            college = College.objects.get(id=phd_student[13])
            new_list=list(phd_student)
            new_list[10]=course
            new_list[13]=college
            writer.writerow(new_list)
        else:
            writer.writerow(phd_student)

    response['Content-Disposition'] = 'attachment;filename="phd_postpone_male_student.csv"'
    return response
def DownloadPhdFnlMaleView(request):
    response = HttpResponse(content_type='text/csv')
    writer = csv.writer(response)
    writer.writerow(
    [
    'firstname','middle_name','surname','email','dob','age','gender','contact','nationality','registration_number','programme_name','start_date','end_date','college','education_level','student_status'
    ]
    )

    for phd_student in Student.objects.filter(education_level='PHD', gender='Male', student_status='final').values_list('firstname','middle_name','surname','email','dob','age','gender','contact','nationality','registration_number','programme_name','start_date','end_date','college','education_level','student_status'):
        if phd_student[10] and phd_student[13] :
            course=Course.objects.get(id=phd_student[10])
            college = College.objects.get(id=phd_student[13])
            new_list=list(phd_student)
            new_list[10]=course
            new_list[13]=college
            writer.writerow(new_list)
        else:
            writer.writerow(phd_student)

    response['Content-Disposition'] = 'attachment;filename="phd_final_male_student.csv"'
    return response
def DownloadMstCntMaleView(request):
    response = HttpResponse(content_type='text/csv')
    writer = csv.writer(response)
    writer.writerow(
    [
    'firstname','middle_name','surname','email','dob','age','gender','contact','nationality','registration_number','programme_name','start_date','end_date','college','education_level','student_status'
    ]
    )

    for masters_student in Student.objects.filter(education_level='MASTERS', gender='Male', student_status='continuous').values_list('firstname','middle_name','surname','email','dob','age','gender','contact','nationality','registration_number','programme_name','start_date','end_date','college','education_level','student_status'):
        if masters_student[10] and masters_student[13] :
            course=Course.objects.get(id=masters_student[10])
            college = College.objects.get(id=masters_student[13])
            new_list=list(masters_student)
            new_list[10]=course
            new_list[13]=college
            writer.writerow(new_list)
        else:
            writer.writerow(masters_student)

    response['Content-Disposition'] = 'attachment;filename="masters_continuous_male_student.csv"'
    return response
def DownloadMstCmpMaleView(request):
    response = HttpResponse(content_type='text/csv')
    writer = csv.writer(response)
    writer.writerow(
    [
    'firstname','middle_name','surname','email','dob','age','gender','contact','nationality','registration_number','programme_name','start_date','end_date','college','education_level','student_status'
    ]
    )

    for phd_student in Student.objects.filter(education_level='MASTERS', gender='Male', student_status='complete').values_list('firstname','middle_name','surname','email','dob','age','gender','contact','nationality','registration_number','programme_name','start_date','end_date','college','education_level','student_status'):
        if phd_student[10] and phd_student[13] :
            course=Course.objects.get(id=phd_student[10])
            college = College.objects.get(id=phd_student[13])
            new_list=list(phd_student)
            new_list[10]=course
            new_list[13]=college
            writer.writerow(new_list)
        else:
            writer.writerow(phd_student)

    response['Content-Disposition'] = 'attachment;filename="masters_completed_male_student.csv"'
    return response
def DownloadMstPstMaleView(request):
    response = HttpResponse(content_type='text/csv')
    writer = csv.writer(response)
    writer.writerow(
    [
    'firstname','middle_name','surname','email','dob','age','gender','contact','nationality','registration_number','programme_name','start_date','end_date','college','education_level','student_status'
    ]
    )

    for phd_student in Student.objects.filter(education_level='MASTERS', gender='Male', student_status='postpone').values_list('firstname','middle_name','surname','email','dob','age','gender','contact','nationality','registration_number','programme_name','start_date','end_date','college','education_level','student_status'):
        if phd_student[10] and phd_student[13] :
            course=Course.objects.get(id=phd_student[10])
            college = College.objects.get(id=phd_student[13])
            new_list=list(phd_student)
            new_list[10]=course
            new_list[13]=college
            writer.writerow(new_list)
        else:
            writer.writerow(phd_student)

    response['Content-Disposition'] = 'attachment;filename="masters_postpone_male_student.csv"'
    return response
def DownloadMstFnlMaleView(request):
    response = HttpResponse(content_type='text/csv')
    writer = csv.writer(response)
    writer.writerow(
    [
    'firstname','middle_name','surname','email','dob','age','gender','contact','nationality','registration_number','programme_name','start_date','end_date','college','education_level','student_status'
    ]
    )

    for phd_student in Student.objects.filter(education_level='MASTERS', gender='Male', student_status='final').values_list('firstname','middle_name','surname','email','dob','age','gender','contact','nationality','registration_number','programme_name','start_date','end_date','college','education_level','student_status'):
        if phd_student[10] and phd_student[13] :
            course=Course.objects.get(id=phd_student[10])
            college = College.objects.get(id=phd_student[13])
            new_list=list(phd_student)
            new_list[10]=course
            new_list[13]=college
            writer.writerow(new_list)
        else:
            writer.writerow(phd_student)

    response['Content-Disposition'] = 'attachment;filename="masters_final_male_student.csv"'
    return response


############### DOWNLOAD ONLY FEMALE PHD & MASTERS
def DownloadPhdContFemaleView(request):
    response = HttpResponse(content_type='text/csv')
    writer = csv.writer(response)
    writer.writerow(
    [
    'firstname','middle_name','surname','email','dob','age','gender','contact','nationality','registration_number','programme_name','start_date','end_date','college','education_level','student_status'
    ]
    )

    for phd_student in Student.objects.filter(education_level='PHD', gender='Female', student_status='continuous').values_list('firstname','middle_name','surname','email','dob','age','gender','contact','nationality','registration_number','programme_name','start_date','end_date','college','education_level','student_status'):
        if phd_student[10] and phd_student[13] :
            course=Course.objects.get(id=phd_student[10])
            college = College.objects.get(id=phd_student[13])
            new_list=list(phd_student)
            new_list[10]=course
            new_list[13]=college
            writer.writerow(new_list)
        else:
            writer.writerow(phd_student)

    response['Content-Disposition'] = 'attachment;filename="phd_continuous_female_student.csv"'
    return response
def DownloadPhdCmpFemaleView(request):
    response = HttpResponse(content_type='text/csv')
    writer = csv.writer(response)
    writer.writerow(
    [
    'firstname','middle_name','surname','email','dob','age','gender','contact','nationality','registration_number','programme_name','start_date','end_date','college','education_level','student_status'
    ]
    )

    for phd_student in Student.objects.filter(education_level='PHD', gender='Female', student_status='complete').values_list('firstname','middle_name','surname','email','dob','age','gender','contact','nationality','registration_number','programme_name','start_date','end_date','college','education_level','student_status'):
        if phd_student[10] and phd_student[13] :
            course=Course.objects.get(id=phd_student[10])
            college = College.objects.get(id=phd_student[13])
            new_list=list(phd_student)
            new_list[10]=course
            new_list[13]=college
            writer.writerow(new_list)
        else:
            writer.writerow(phd_student)

    response['Content-Disposition'] = 'attachment;filename="phd_complete_female_student.csv"'
    return response
def DownloadPhdPstFemaleView(request):
    response = HttpResponse(content_type='text/csv')
    writer = csv.writer(response)
    writer.writerow(
    [
    'firstname','middle_name','surname','email','dob','age','gender','contact','nationality','registration_number','programme_name','start_date','end_date','college','education_level','student_status'
    ]
    )

    for phd_student in Student.objects.filter(education_level='PHD', gender='Female', student_status='postpone').values_list('firstname','middle_name','surname','email','dob','age','gender','contact','nationality','registration_number','programme_name','start_date','end_date','college','education_level','student_status'):
        if phd_student[10] and phd_student[13] :
            course=Course.objects.get(id=phd_student[10])
            college = College.objects.get(id=phd_student[13])
            new_list=list(phd_student)
            new_list[10]=course
            new_list[13]=college
            writer.writerow(new_list)
        else:
            writer.writerow(phd_student)

    response['Content-Disposition'] = 'attachment;filename="phd_postpone_female_student.csv"'
    return response
def DownloadPhdFnlFemaleView(request):
    response = HttpResponse(content_type='text/csv')
    writer = csv.writer(response)
    writer.writerow(
    [
    'firstname','middle_name','surname','email','dob','age','gender','contact','nationality','registration_number','programme_name','start_date','end_date','college','education_level','student_status'
    ]
    )

    for phd_student in Student.objects.filter(education_level='PHD', gender='Female', student_status='final').values_list('firstname','middle_name','surname','email','dob','age','gender','contact','nationality','registration_number','programme_name','start_date','end_date','college','education_level','student_status'):
        if phd_student[10] and phd_student[13] :
            course=Course.objects.get(id=phd_student[10])
            college = College.objects.get(id=phd_student[13])
            new_list=list(phd_student)
            new_list[10]=course
            new_list[13]=college
            writer.writerow(new_list)
        else:
            writer.writerow(phd_student)

    response['Content-Disposition'] = 'attachment;filename="phd_final_female_student.csv"'
    return response
def DownloadMstCntFemaleView(request):
    response = HttpResponse(content_type='text/csv')
    writer = csv.writer(response)
    writer.writerow(
    [
    'firstname','middle_name','surname','email','dob','age','gender','contact','nationality','registration_number','programme_name','start_date','end_date','college','education_level','student_status'
    ]
    )

    for phd_student in Student.objects.filter(education_level='MASTERS', gender='Female', student_status='continuous').values_list('firstname','middle_name','surname','email','dob','age','gender','contact','nationality','registration_number','programme_name','start_date','end_date','college','education_level','student_status'):
        if phd_student[10] and phd_student[13] :
            course=Course.objects.get(id=phd_student[10])
            college = College.objects.get(id=phd_student[13])
            new_list=list(phd_student)
            new_list[10]=course
            new_list[13]=college
            writer.writerow(new_list)
        else:
            writer.writerow(phd_student)

    response['Content-Disposition'] = 'attachment;filename="masters_continuous_female_student.csv"'
    return response
def DownloadMstCmpFemaleView(request):
    response = HttpResponse(content_type='text/csv')
    writer = csv.writer(response)
    writer.writerow(
    [
    'firstname','middle_name','surname','email','dob','age','gender','contact','nationality','registration_number','programme_name','start_date','end_date','college','education_level','student_status'
    ]
    )

    for phd_student in Student.objects.filter(education_level='MASTERS', gender='Female', student_status='complete').values_list('firstname','middle_name','surname','email','dob','age','gender','contact','nationality','registration_number','programme_name','start_date','end_date','college','education_level','student_status'):
        if phd_student[10] and phd_student[13] :
            course=Course.objects.get(id=phd_student[10])
            college = College.objects.get(id=phd_student[13])
            new_list=list(phd_student)
            new_list[10]=course
            new_list[13]=college
            writer.writerow(new_list)
        else:
            writer.writerow(phd_student)

    response['Content-Disposition'] = 'attachment;filename="masters_completed_female_student.csv"'
    return response
def DownloadMstPstFemaleView(request):
    response = HttpResponse(content_type='text/csv')
    writer = csv.writer(response)
    writer.writerow(
    [
    'firstname','middle_name','surname','email','dob','age','gender','contact','nationality','registration_number','programme_name','start_date','end_date','college','education_level','student_status'
    ]
    )

    for phd_student in Student.objects.filter(education_level='PHD', gender='Female', student_status='postpone').values_list('firstname','middle_name','surname','email','dob','age','gender','contact','nationality','registration_number','programme_name','start_date','end_date','college','education_level','student_status'):
        if phd_student[10] and phd_student[13] :
            course=Course.objects.get(id=phd_student[10])
            college = College.objects.get(id=phd_student[13])
            new_list=list(phd_student)
            new_list[10]=course
            new_list[13]=college
            writer.writerow(new_list)
        else:
            writer.writerow(phd_student)

    response['Content-Disposition'] = 'attachment;filename="masters_postpone_female_student.csv"'
    return response
def DownloadMstFnlFemaleView(request):
    response = HttpResponse(content_type='text/csv')
    writer = csv.writer(response)
    writer.writerow(
    [
    'firstname','middle_name','surname','email','dob','age','gender','contact','nationality','registration_number','programme_name','start_date','end_date','college','education_level','student_status'
    ]
    )

    for phd_student in Student.objects.filter(education_level='MASTERS', gender='Female', student_status='final').values_list('firstname','middle_name','surname','email','dob','age','gender','contact','nationality','registration_number','programme_name','start_date','end_date','college','education_level','student_status'):
        if phd_student[10] and phd_student[13] :
            course=Course.objects.get(id=phd_student[10])
            college = College.objects.get(id=phd_student[13])
            new_list=list(phd_student)
            new_list[10]=course
            new_list[13]=college
            writer.writerow(new_list)
        else:
            writer.writerow(phd_student)

    response['Content-Disposition'] = 'attachment;filename="masters_final_female_student.csv"'
    return response

# ====== hap hap  ====
def DownloadMaleStdView(request):
    response = HttpResponse(content_type='text/csv')
    writer = csv.writer(response)
    writer.writerow(
    [
    'firstname','middle_name','surname','email','dob','age','gender','contact','nationality','registration_number','programme_name','start_date','end_date','college','education_level','student_status'
    ]
    )

    for male_student in Student.objects.filter(gender='Male').values_list('firstname','middle_name','surname','email','dob','age','gender','contact','nationality','registration_number','programme_name','start_date','end_date','college','education_level','student_status'):
        if male_student[10] and male_student[13] :
            course=Course.objects.get(id=male_student[10])
            college = College.objects.get(id=male_student[13])
            new_list=list(male_student)
            new_list[10]=course
            new_list[13]=college
            writer.writerow(new_list)
        else:
            writer.writerow(male_student)

    response['Content-Disposition'] = 'attachment;filename="all_male_student.csv"'
    return response
def DownloadFemaleStdView(request):
    response = HttpResponse(content_type="txt/csv")
    writer= csv.writer(response)
    writer.writerow([
    'firstname','middle_name','surname','email','dob','age','gender','contact','nationality','registration_number','programme_name','start_date','end_date','college','education_level','student_status'
    ]
    )
    for female_student in Student.objects.filter(gender='Female').values_list('firstname','middle_name','surname','email','dob','age','gender','contact','nationality','registration_number','programme_name','start_date','end_date','college','education_level','student_status'):
        if female_student[10] and female_student[13] :
            course=Course.objects.get(id=female_student[10])
            college = College.objects.get(id=female_student[13])
            new_list=list(female_student)
            new_list[10]=course
            new_list[13]=college
            writer.writerow(new_list)
        else:
            writer.writerow(female_student)

    response['Content-Disposition'] = 'attachment;filename="all_Female_student.csv"'
    return response
def DownloadMalePhdView(request):
    response=HttpResponse(content_type="txt/csv")
    writer=csv.writer(response)
    writer.writerow([
    'firstname','middle_name','surname','email','dob','age','gender','contact','nationality','registration_number','programme_name','start_date','end_date','college','education_level','student_status'
    ]
    )
    for std in Student.objects.filter(gender='Male', education_level="PHD").values_list('firstname','middle_name','surname','email','dob','age','gender','contact','nationality','registration_number','programme_name','start_date','end_date','college','education_level','student_status'):
        if std[10] and std[13] :
            course=Course.objects.get(id=std[10])
            college = College.objects.get(id=std[13])
            new_list=list(std)
            new_list[10]=course
            new_list[13]=college
            writer.writerow(new_list)
        else:
            writer.writerow(std)

    response['Content-Disposition'] = 'attachment;filename="List_of_all_male_who_have_phd.csv"'
    return response
def DownloadFemalePhdView(request):
    response=HttpResponse(content_type="txt/csv")
    writer=csv.writer(response)
    writer.writerow([
    'firstname','middle_name','surname','email','dob','age','gender','contact','nationality','registration_number','programme_name','start_date','end_date','college','education_level','student_status'
    ]
    )
    for std in Student.objects.filter(gender="Female", education_level="PHD").values_list('firstname','middle_name','surname','email','dob','age','gender','contact','nationality','registration_number','programme_name','start_date','end_date','college','education_level','student_status'):
      if std[10] and std[13] :
          course=Course.objects.get(id=std[10])
          college = College.objects.get(id=std[13])
          new_list=list(std)
          new_list[10]=course
          new_list[13]=college
          writer.writerow(new_list)

    else:
        writer.writerow(std)

    response['Content-Disposition'] = 'attachment;filename="all_female_who_have_phd.csv"'
    return response
def DownloadPhdStudent(request):
    response=HttpResponse(content_type="txt/csv")
    writer=csv.writer(response)
    writer.writerow([
    'firstname','middle_name','surname','email','dob','age','gender','contact','nationality','registration_number','programme_name','start_date','end_date','college','education_level','student_status'
    ]
    )
    for std in Student.objects.filter(education_level="PHD").values_list('firstname','middle_name','surname','email','dob','age','gender','contact','nationality','registration_number','programme_name','start_date','end_date','college','education_level','student_status'):
        if std[10] and std[13] :
          course=Course.objects.get(id=std[10])
          college = College.objects.get(id=std[13])
          new_list=list(std)
          new_list[10]=course
          new_list[13]=college
          writer.writerow(new_list)

    else:
        writer.writerow(std)

    response['Content-Disposition'] = 'attachment;filename="all_phd_student.csv"'
    return response
def DownloadMastersStudent(request):
    response=HttpResponse(content_type="txt/csv")
    writer=csv.writer(response)
    writer.writerow([
    'firstname','middle_name','surname','email','dob','age','gender','contact','nationality','registration_number','programme_name','start_date','end_date','college','education_level','student_status'
    ]
    )
    for std in Student.objects.filter(education_level="MASTERS").values_list('firstname','middle_name','surname','email','dob','age','gender','contact','nationality','registration_number','programme_name','start_date','end_date','college','education_level','student_status'):
        if std[10] and std[13] :
          course=Course.objects.get(id=std[10])
          college = College.objects.get(id=std[13])
          new_list=list(std)
          new_list[10]=course
          new_list[13]=college
          writer.writerow(new_list)

    else:
        writer.writerow(std)

    response['Content-Disposition'] = 'attachment;filename="all_masters_student.csv"'
    return response
def DownloadStudentFromStartDate(request, start_date):
    response=HttpResponse(content_type="txt/csv")
    writer=csv.writer(response)
    writer.writerow([
    'firstname','middle_name','surname','email','dob','age','gender','contact','nationality','registration_number','programme_name','start_date','end_date','college','education_level','student_status'
    ]
    )
    for std in Student.objects.filter(start_date=str(start_date)).values_list('firstname','middle_name','surname','email','dob','age','gender','contact','nationality','registration_number','programme_name','start_date','end_date','college','education_level','student_status'):
        print("===============")
        if std[10] and std[13] :
          course=Course.objects.get(id=std[10])
          college = College.objects.get(id=std[13])
          new_list=list(std)
          new_list[10]=course
          new_list[13]=college
          writer.writerow(new_list)
        else:
            writer.writerow(std)

    response['Content-Disposition'] = (f'attachment;filename="all_student_from_{start_date}.csv"')
    return response
def DownloadStudentAtEndDate(request, end_date):
    response=HttpResponse(content_type="txt/csv")
    writer=csv.writer(response)
    writer.writerow([
    'firstname','middle_name','surname','email','dob','age','gender','contact','nationality','registration_number','programme_name','start_date','end_date','college','education_level','student_status'
    ]
    )
    for std in Student.objects.filter(end_date=str(end_date)).values_list('firstname','middle_name','surname','email','dob','age','gender','contact','nationality','registration_number','programme_name','start_date','end_date','college','education_level','student_status'):
        if std[10] and std[13] :
          course=Course.objects.get(id=std[10])
          college = College.objects.get(id=std[13])
          new_list=list(std)
          new_list[10]=course
          new_list[13]=college
          writer.writerow(new_list)
        else:
            writer.writerow(std)

    response['Content-Disposition'] = (f'attachment;filename="all_student_whose_courses_ended_at_{end_date}.csv"')
    return response
def DownloadContinuousStudentView(request):
    response=HttpResponse(content_type="txt/csv")
    writer=csv.writer(response)
    writer.writerow([
    'firstname','middle_name','surname','email','dob','age','gender','contact','nationality','registration_number','programme_name','start_date','end_date','college','education_level','student_status'
    ]
    )
    for std in Student.objects.filter(student_status="continuous").values_list('firstname','middle_name','surname','email','dob','age','gender','contact','nationality','registration_number','programme_name','start_date','end_date','college','education_level','student_status'):
        if std[10] and std[13] :
          course=Course.objects.get(id=std[10])
          college = College.objects.get(id=std[13])
          new_list=list(std)
          new_list[10]=course
          new_list[13]=college
          writer.writerow(new_list)
        else:
            writer.writerow(std)

    response['Content-Disposition'] = (f'attachment;filename="all_continuous_student_.csv"')
    return response
def DownloadPostponedStudentView(request):
    response=HttpResponse(content_type="txt/csv")
    writer=csv.writer(response)
    writer.writerow([
    'firstname','middle_name','surname','email','dob','age','gender','contact','nationality','registration_number','programme_name','start_date','end_date','college','education_level','student_status'
    ]
    )
    for std in Student.objects.filter(student_status="postpone").values_list('firstname','middle_name','surname','email','dob','age','gender','contact','nationality','registration_number','programme_name','start_date','end_date','college','education_level','student_status'):
        if std[10] and std[13] :
          course=Course.objects.get(id=std[10])
          college = College.objects.get(id=std[13])
          new_list=list(std)
          new_list[10]=course
          new_list[13]=college
          writer.writerow(new_list)
        else:
            writer.writerow(std)

    response['Content-Disposition'] = (f'attachment;filename="all_postponed_student_.csv"')
    return response
def DownloadCompletedStudentView(request):
    response=HttpResponse(content_type="txt/csv")
    writer=csv.writer(response)
    writer.writerow([
    'firstname','middle_name','surname','email','dob','age','gender','contact','nationality','registration_number','programme_name','start_date','end_date','college','education_level','student_status'
    ]
    )
    for std in Student.objects.filter(student_status="complete").values_list('firstname','middle_name','surname','email','dob','age','gender','contact','nationality','registration_number','programme_name','start_date','end_date','college','education_level','student_status'):
        if std[10] and std[13] :
          course=Course.objects.get(id=std[10])
          college = College.objects.get(id=std[13])
          new_list=list(std)
          new_list[10]=course
          new_list[13]=college
          writer.writerow(new_list)
        else:
            writer.writerow(std)

    response['Content-Disposition'] = (f'attachment;filename="all_student_who_completed_courses.csv"')
    return response
def DownloadFinalistStudentView(request):
    response=HttpResponse(content_type="txt/csv")
    writer=csv.writer(response)
    writer.writerow([
    'firstname','middle_name','surname','email','dob','age','gender','contact','nationality','registration_number','programme_name','start_date','end_date','college','education_level','student_status'
    ]
    )
    for std in Student.objects.filter(student_status="final").values_list('firstname','middle_name','surname','email','dob','age','gender','contact','nationality','registration_number','programme_name','start_date','end_date','college','education_level','student_status'):
        if std[10] and std[13] :
          course=Course.objects.get(id=std[10])
          college = College.objects.get(id=std[13])
          new_list=list(std)
          new_list[10]=course
          new_list[13]=college
          writer.writerow(new_list)
        else:
            writer.writerow(std)

    response['Content-Disposition'] = (f'attachment;filename="all_student_who_are_finalist_.csv"')
    return response
def DownloadMaleMastersStudentView(request):
    response=HttpResponse(content_type="txt/csv")
    writer=csv.writer(response)
    writer.writerow([
    'firstname','middle_name','surname','email','dob','age','gender','contact','nationality','registration_number','programme_name','start_date','end_date','college','education_level','student_status'
    ]
    )
    for std in Student.objects.filter(gender="Male", education_level="MASTERS").values_list('firstname','middle_name','surname','email','dob','age','gender','contact','nationality','registration_number','programme_name','start_date','end_date','college','education_level','student_status'):
        if std[10] and std[13] :
          course=Course.objects.get(id=std[10])
          college = College.objects.get(id=std[13])
          new_list=list(std)
          new_list[10]=course
          new_list[13]=college
          writer.writerow(new_list)
        else:
            writer.writerow(std)

    response['Content-Disposition'] = (f'attachment;filename="all_male_who have_masters.csv"')
    return response

############## STUDENT DETAIL VIEW ##############
def StudentDetailView(request, pk):
    get_std = Student.objects.get(id=pk)
    templates = "account/student_detail.html"
    context = {
    "get_std" : get_std
    }

    return render(request, templates, context)

def plotGraphView(request):
    total_female=Student.objects.filter(gender="Female").count()
    total_male=Student.objects.filter(gender="Male").count()
    x=["male", "female"]
    y=[total_male, total_female]
    chart=get_plot(x, y)
    total_male_cont=Student.objects.filter(gender="Male", student_status="continuous").count()
    total_female_count=Student.objects.filter(gender="Female",  student_status="continuous").count()
    y=[total_male_cont, total_female_count]
    chart2=get_graph_cnt(x, y)
    total_male_cmp=Student.objects.filter(gender="Male", student_status="complete").count()
    total_female_cmp=Student.objects.filter(gender="Female",  student_status="complete").count()
    y=[total_male_cmp, total_female_cmp]
    chart3=get_graph_cmp(x,y)
    total_male_fnl=Student.objects.filter(gender="Male", student_status="final").count()
    total_female_fnl=Student.objects.filter(gender="female", student_status="final").count()
    y=[total_male_fnl, total_female_fnl]
    chart4=get_graph_fnl(x, y)
    total_female_pst=Student.objects.filter(gender="female", student_status="postponed").count()
    total_male_pst=Student.objects.filter(gender="Male", student_status="postponed").count()
    y=[total_male_pst, total_female_pst]
    chart5=get_graph_pst(x,y)
    total_female_phd=Student.objects.filter(gender="female", education_level="PHD").count()
    total_male_phd=Student.objects.filter(gender="Male", student_status="PHD").count()
    y=[total_male_phd, total_male_phd]
    chart6=get_graph_phd(x, y)
    total_male_mst=Student.objects.filter(gender="Male", education_level="MASTERS").count()
    total_female_mst=Student.objects.filter(gender="Female", education_level="MASTERS").count()
    y=[total_male_mst, total_female_mst]
    chart7=get_graph_mst(x, y)

    templates='account/charts.html'
    context={
        "charts":chart,
        "chart2":chart2,
        "chart3":chart3,
        "chart4":chart4,
        "chart5":chart5,
        "chart6":chart6,
        "chart7":chart7,
    }
    return  render(request, templates, context)
