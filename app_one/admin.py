from django.contrib import admin
from app_one.models import UserInfo, StudentInfo, TeacherInfo, Course, Mark, Attendance, Course_taken, Course_teaching, Timetable
# Register your models here.

admin.site.register(UserInfo)
admin.site.register(StudentInfo)
admin.site.register(TeacherInfo)
admin.site.register(Course)
admin.site.register(Mark)
admin.site.register(Attendance)
admin.site.register(Course_teaching)
admin.site.register(Course_taken)
admin.site.register(Timetable)