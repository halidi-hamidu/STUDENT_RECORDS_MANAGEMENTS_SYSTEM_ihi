from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    #user account
    path('', views.LoginView, name="auth"),
    path('register/', views.RegisterView, name="register"),
    path('logged-out/', views.LogOutView, name="logout"),
    #password reset
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='account/password_reset.html'), name="password_reset"),
    path('password-reset-done/', auth_views.PasswordResetDoneView.as_view(template_name='account/password_reset_done.html'), name="password_reset_done"),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='account/password_reset_confirm.html'), name="password_reset_confirm"),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='account/password_reset_complete.html'), name="password_reset_complete"),
    #dashboard url
    path('dashboard/', views.DashboardView, name="dashboard"),
    path('phd/', views.PhdView, name="phd"),
    path('masters/', views.MastersView, name="masters"),
    path('add-student/', views.AddStudentView, name="add_student"),
    path('add-module/', views.AddModuleView, name="add_module"),
    path('add-college/', views.AddCollegeView, name="add_college"),
    path('add-course/', views.AddCourseView, name="add_course"),
    path('all-student/', views.AllStudentView, name="all_std"),

    ### CRUD OPERATION
    path('update-student/<str:pk>/', views.UpdateStudentView, name="update"),
    path('delete-student/<str:pk>/', views.DeleteStudentView, name="delete"),

    ### EXPORT CSV FILES
    path('download/', views.DownloadAllView, name="download"),
    path('download-phd/', views.DownloadPhdView, name="download_phd"),
    path('download-masters/', views.DownloadMastersView, name="download_masters"),
    path('download-phd-cont-male/',views.DownloadPhdContMaleView, name="phd_cont_male"),
    path('download-phd-cmp-male/', views.DownloadPhdCmpMaleView, name="phd_cmp_male"),
    path('download-phd-pst-male/', views.DownloadPhdPstMaleView, name="phd_pst_male"),
    path('download-phd-fnl-male/', views.DownloadPhdFnlMaleView, name="phd_fnl_male"),
    path('download-mst-cnt-male/', views.DownloadMstCntMaleView, name="mst_cnt_male"),
    path('download-mst-cmp-male/', views.DownloadMstCmpMaleView, name="mst_cmp_male"),
    path('download-mst-pst-male/', views.DownloadMstPstMaleView, name="mst_pst_male"),
    path('download-mst-fnl-male/', views.DownloadMstFnlMaleView, name="mst_fnl_male"),

    path('download-phd-cont-female/', views.DownloadPhdContFemaleView, name="phd_cont_female"),
    path('download-phd-cmp-female/', views.DownloadPhdCmpFemaleView, name="phd_cmp_female"),
    path('download-phd-pst-female/', views.DownloadPhdPstFemaleView, name="phd_pst_female"),
    path('download-phd-fnl-female/', views.DownloadPhdFnlFemaleView, name="phd_fnl_female"),
    path('download-mst-cnt-female/', views.DownloadMstCntFemaleView, name="mst_cnt_female"),
    path('download-mst-cmp-female/', views.DownloadMstCmpFemaleView, name="mst_cmp_female"),
    path('download-mst-pst-female/', views.DownloadMstPstFemaleView, name="mst_pst_female"),
    path('download-mst-fnl-female/', views.DownloadMstFnlFemaleView, name="mst_fnl_female"),
    path('download-all-male/', views.DownloadMaleStdView, name="male_std"),
    path('download-all-female/', views.DownloadFemaleStdView, name="female_std"),
    path('download-all-male-phd/', views.DownloadMalePhdView, name='phd_male'),
    path('download-all-female-phd/', views.DownloadFemalePhdView, name='phd_female'),
    path('download-all-phd-std/', views.DownloadPhdStudent, name="phd_std"),
    path('download-all-mst-std/', views.DownloadMastersStudent, name="mst_std"),
    path('download-specific-date/<str:start_date>/', views.DownloadStudentFromStartDate, name='start_date_std'),
    path('download-std-at/<str:end_date>/', views.DownloadStudentAtEndDate, name='at_end_date'),
    path('download-all-continuous-student/', views.DownloadContinuousStudentView, name='cnt_std'),
    path('download-all-postponed-student/', views.DownloadPostponedStudentView, name='pst_std'),
    path('download-all-completed-student/', views.DownloadCompletedStudentView, name='cmp_std'),
    path('download-all-finalist-student/', views.DownloadFinalistStudentView, name='fnl_std'),
    path('download-all-male-with-masters/', views.DownloadMaleMastersStudentView, name='masters_male'),
    ######## STUDENT DETAIL VIEW
    path('student-detail/student/<str:pk>/', views.StudentDetailView, name="student_detail"),
    path("student/gender-relation-chart", views.plotGraphView, name="chart"),
]
