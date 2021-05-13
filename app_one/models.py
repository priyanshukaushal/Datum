from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
# Create your models here.

class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    role_types = ((False, "Student"), (True, "Teacher"))
    role = models.BooleanField(choices = role_types, default = False)

    def __str__(self):
        return self.user.username

class StudentInfo(models.Model):
    admin = models.OneToOneField(UserInfo, on_delete = models.CASCADE)
    name = models.CharField(max_length = 20, null = True, blank = True)
    address = models.CharField(max_length = 100, null = True, blank = True)
    age = models.IntegerField(null = True, blank = True)
    gender_types = (("M", "Male"), ("F", "Female"))
    gender = models.CharField(choices = gender_types, max_length = 1, null = True, blank = True)
    contact = models.CharField(max_length = 10, null = True, blank = True)
    emailID = models.EmailField(max_length = 50, null = True, blank = True)

    def __str__(self):
        return str(self.admin.user.username)



class TeacherInfo(models.Model):
    admin = models.OneToOneField(UserInfo, on_delete = models.CASCADE)
    name = models.CharField(max_length = 20, null = True, blank = True)
    address = models.CharField(max_length = 100, null = True, blank = True)
    age = models.IntegerField(null = True, blank = True)
    gender_types = (("M", "Male"), ("F", "Female"))
    gender = models.CharField(choices = gender_types, max_length = 1, null = True, blank = True)
    contact = models.CharField(max_length = 10, null = True, blank = True)
    emailID = models.EmailField(max_length = 50, null = True, blank = True)

    def __str__(self):
        return str(self.admin.user.username)

class Course(models.Model):
    course_name = models.CharField(max_length = 50)
    course_id = models.CharField(max_length = 10, primary_key = True)

    def __str__(self):
        return str(self.course_id)

class Mark(models.Model):
    student_id = models.ForeignKey(StudentInfo, on_delete = models.CASCADE)
    course_id = models.ForeignKey(Course, on_delete = models.CASCADE)
    quiz1 = models.FloatField(null = True, blank = True)
    quiz2 = models.FloatField(null = True, blank = True)
    mst = models.FloatField( null = True, blank = True)
    est = models.FloatField( null = True, blank = True)

    def __str__(self):
        return str(self.student_id.admin.user.username + " " + self.course_id.course_id)

class Attendance(models.Model):
    student_id = models.ForeignKey(StudentInfo, on_delete = models.CASCADE)
    course_id = models.ForeignKey(Course, on_delete = models.CASCADE)
    date = models.DateField()
    status_choices = ((True, "Present"), (False, "Absent"))
    status = models.BooleanField(choices = status_choices,default=False,null = True, blank = True)

    def __str__(self):
        return str(self.student_id.admin.user.username + " " + self.course_id.course_id)

class Course_taken(models.Model):
    student_id = models.ForeignKey(StudentInfo, on_delete = models.CASCADE)
    course_id = models.ForeignKey(Course, on_delete = models.CASCADE)

    def __str__(self):
        return str(self.student_id.admin.user.username + " " + self.course_id.course_id)


class Course_teaching(models.Model):
    teacher_id = models.ForeignKey(TeacherInfo, on_delete = models.CASCADE)
    course_id = models.ForeignKey(Course, on_delete = models.CASCADE)

    def __str__(self):
        return str(self.teacher_id.admin.user.username + " " + self.course_id.course_id)

class Timetable(models.Model):
    role_choices = ((False, "Student"), (True, "Teacher"))
    user_type = models.BooleanField(choices = role_choices, default = False)
    day_choices = ((1, "Monday"), (2, "Tuesday"), (3, "Wednesday"), (4, "Thursday"), (5, "Friday"))
    day = models.IntegerField(choices=day_choices, default=1)
    slot1 = models.ForeignKey(Course, on_delete = models.CASCADE, related_name = "slot1", null = True, blank = True)
    slot2 = models.ForeignKey(Course, on_delete = models.CASCADE, related_name = "slot2", null = True, blank = True)
    slot3 = models.ForeignKey(Course, on_delete = models.CASCADE, related_name = "slot3", null = True, blank = True)
    slot4 = models.ForeignKey(Course, on_delete = models.CASCADE, related_name = "slot4", null = True, blank = True)
    slot5 = models.ForeignKey(Course, on_delete = models.CASCADE, related_name = "slot5", null = True, blank = True)

    def __str__(self):
        if self.user_type == True:
            name = 'Teacher'
        else:
            name = 'Student'
        lst = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        return str(name + " " + lst[self.day-1])

@receiver(post_save, sender = UserInfo)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.role == False:
            StudentInfo.objects.create(admin = instance)
        if instance.role == True:
            TeacherInfo.objects.create(admin = instance)

@receiver(post_save, sender = UserInfo)
def save_user_profile(sender, instance, **kwargs):
    if instance.role == False:
        instance.studentinfo.save()
    if instance.role == True:
        instance.teacherinfo.save()
