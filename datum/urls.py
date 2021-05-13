"""datum URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app_one import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login_view, name = 'login_url'),
    path('home/', views.home_view, name = 'home_url'),
    path('about/', views.about_view, name = 'about_url'),
    path('developers/', views.developers_view, name = 'developers_url'),
    path('logout/', views.logout_view, name = 'logout_url'),
    path('profile/', views.profile_view, name = 'profile_url'),
    path('edit_profile/', views.edit_profile_view, name = 'edit_profile_url'),
    path('courses/', views.course_view, name = 'course_url'),
    path('student_marks/', views.student_marks_view, name = 'student_marks_url'),
    path('student_attendance/', views.student_attendance_view, name = 'student_attendance_url'),
    path('teacher_attendance/', views.teacher_attendance_view, name = 'teacher_attendance_url'),
    path('teacher_marks/', views.teacher_marks_view, name = 'teacher_marks_url'),
    path('mark_attendance/', views.mark_attendance_view, name = 'mark_attendance_url'),
    path('mark_marks/', views.mark_marks_view, name = 'mark_marks_url'),
    path('timetable/', views.timetable_view, name = 'timetable_url'),
    path('view_attendance/', views.view_attendance_view, name = 'view_attendance_url'),
]
