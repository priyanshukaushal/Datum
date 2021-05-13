from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from app_one.models import UserInfo, StudentInfo, TeacherInfo, Course_taken, Course_teaching, Mark, Attendance, User, Course, Timetable
from django.contrib import messages
from datetime import datetime
from dateutil import parser
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages

# Create your views here.

def login_view(request):
    message = ''
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username = username, password = password)
        if user:
            login(request, user)
            users = UserInfo.objects.filter(user = user)
            user_instance = None
            for i in users:
                user_instance = i
            if user_instance == None:
                message = 'Invalid Login'
            else :
                return redirect('home_url')
        else:
                message = 'Invalid Username or Password'

    return render(request, 'login.html', {'message' : message})


@login_required
def home_view(request):
    user_instance = UserInfo.objects.get(user = request.user)
    if user_instance.role == False:
        student = StudentInfo.objects.get(admin = user_instance)
        name = student.name
    if user_instance.role == True:
        teacher = TeacherInfo.objects.get(admin = user_instance)
        name = teacher.name
    return render(request, 'home.html', {'name' : name})

@login_required
def profile_view(request):
    admin = UserInfo.objects.get(user = request.user)
    if admin.role == False:
        student = StudentInfo.objects.get(admin = admin)
        if student.gender=="M":
            gender="Male"
        elif student.gender=="F":
            gender="Female"
        else:
            gender=None


        profile_details = {'name' : student.name, 'address' : student.address, 'age' : student.age, 'gender' : gender, 'contact' : student.contact, 'emailid' : student.emailID}
        return render(request, 'profile.html', profile_details)
    else:
        teacher = TeacherInfo.objects.get(admin = admin)
        if teacher.gender=="M":
            gender="Male"
        elif teacher.gender=="F":
            gender="Female"
        else:
            gender=None
        profile_details = {'name' : teacher.name, 'address' : teacher.address, 'age' : teacher.age, 'gender' : gender, 'contact' : teacher.contact, 'emailid' : teacher.emailID}
        return render(request, 'profile.html', profile_details)


@login_required
def logout_view(request):
    logout(request)
    return redirect('login_url')

def developers_view(request):
    return render(request, 'developers.html')

def about_view(request):
    return render(request, 'about.html')

def password_validator(pass_word):
    if(len(pass_word) < 9):
        return False
    num_flag = 0
    lowchar_flag = 0
    upchar_flag = 0
    nums_lst = ['1','2','3','4','5','6','7','8','9','0']
    lowchars_lst = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    upchars_lst = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    for i in pass_word:
        if i in nums_lst:
            num_flag = 1
        if i in lowchars_lst:
            lowchar_flag = 1
        if i in upchars_lst:
            upchar_flag = 1
    if(num_flag and lowchar_flag and upchar_flag):
        return True
    else:
        return False


@login_required
def edit_profile_view(request):
    error_message = ''
    if request.method == 'POST':
        if 'old_password' in request.POST:
            old_password = request.POST.get('old_password')
            new_password = request.POST.get('new_password')
            new_password_1 = request.POST.get('new_password_1')
            user = authenticate(username = request.user.username , password = old_password)
            if user is not None:
                if old_password == new_password :
                    error_message = "Old and New password can't be same"
                elif(password_validator(new_password)):
                    if(new_password == new_password_1):
                        user.set_password(new_password)
                        print("error1")
                        user.save()
                        update_session_auth_hash(request, user)
                        print("error2")
                        messages.success(request, 'Password updated successfully!')
                        return redirect('profile_url')
                    else:
                        error_message = 'Passwords do not match'
                else:
                    error_message = 'Choose a strong password'
            else:
                error_message = 'Old password is not correct'
        else:
            name = request.POST.get('name')
            email = request.POST.get('email')
            address = request.POST.get('address')
            age = request.POST.get('age')
            contact = request.POST.get('contact')
            sex = request.POST.get('sex')
            if name == '':
                name = None
            if email == '':
                email = None
            if address == '':
                address = None
            if contact == '':
                contact = None
            if sex == '':
                sex = None
            if age == '':
                age = None
            admin = UserInfo.objects.get(user = request.user)
            if admin.role == False:
                studentinfo = StudentInfo.objects.get_or_create(admin = admin)
                student = studentinfo[0]
                if name is not None:
                    student.name = name
                if email is not None:
                    student.emailID = email
                if address is not None:
                    student.address = address
                if age is not None:
                    student.age = int(age)
                if contact is not None:
                    student.contact = contact
                if sex is not None:
                    student.gender = sex
                student.save()
            else:
                teacherinfo = TeacherInfo.objects.get_or_create(admin = admin)
                teacher = teacherinfo[0]
                if name is not None:
                    teacher.name = name
                if email is not None:
                    teacher.emailID = email
                if address is not None:
                    teacher.address = address
                if age is not None:
                    teacher.age = age
                if contact is not None:
                    teacher.contact = contact
                if sex is not None:
                    teacher.gender = sex
                teacher.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile_url')
    return render(request, 'edit_profile.html', {'error' : error_message})


@login_required
def course_view(request):
    admin = UserInfo.objects.get(user = request.user)
    if request.method == 'POST':
        user_demand = request.POST.get('user_demand')
        action_and_id = user_demand.split(',')
        request.session['cid'] = action_and_id[1]
        if action_and_id[0]  == 'marks':
            if admin.role == False:
                return redirect('student_marks_url')
            else :
                return redirect('teacher_marks_url')
        else :
            if admin.role == False:
                return redirect('student_attendance_url')
            else :
                return redirect('teacher_attendance_url')
    lst = []
    if admin.role == False:
        student = StudentInfo.objects.get(admin = admin)
        courses = Course_taken.objects.filter(student_id = student).order_by('course_id')
        for course in courses:
            lst.append((course.course_id.course_id, course.course_id.course_name))

    else:
        teacher = TeacherInfo.objects.get(admin = admin)
        courses = Course_teaching.objects.filter(teacher_id = teacher).order_by('course_id')
        for course in courses:
            lst.append((course.course_id.course_id, course.course_id.course_name))
    return render(request, 'course.html', {'courses' : lst})

@login_required
def student_marks_view(request):
    avg_marks = [0,0,0,0]
    highest_marks = [0,0,0,0]
    lowest_marks = [100,100,100,100]
    curr_marks = [0,0,0,0]
    admin = UserInfo.objects.get(user = request.user)
    student = StudentInfo.objects.get(admin = admin)
    marks_obj = Mark.objects.filter(student_id = student, course_id = request.session['cid'])
    marks_for_graph = Mark.objects.filter(course_id = request.session['cid'])
    # --------------quiz1 marks-------------
    count = 0
    for i in marks_for_graph:
        if i.quiz1 is not None:
            avg_marks[0] += i.quiz1
            count += 1
            if i.quiz1 > highest_marks[0]:
                highest_marks[0] = i.quiz1
            if i.quiz1 < lowest_marks[0]:
                lowest_marks[0] = i.quiz1
    if count!=0:
        avg_marks[0] =  avg_marks[0]/count
    # ------------mst marks-------------
    count = 0
    for i in marks_for_graph:
        if i.mst is not None:
            avg_marks[1] += i.mst
            count += 1
            if i.mst > highest_marks[1]:
                highest_marks[1] = i.mst
            if i.mst < lowest_marks[1]:
                lowest_marks[1] = i.mst
    if count!=0:
        avg_marks[1] =  avg_marks[1]/count
    # ------------quiz2 marks-----------
    count = 0
    for i in marks_for_graph:
        if i.quiz2 is not None:
            avg_marks[2] += i.quiz2
            count += 1
            if i.quiz2 > highest_marks[2]:
                highest_marks[2] = i.quiz2
            if i.quiz2 < lowest_marks[2]:
                lowest_marks[2] = i.quiz2
    if count!=0:
        avg_marks[2] =  avg_marks[2]/count

    # -----------est marks--------------
    count = 0
    for i in marks_for_graph:
        if i.est is not None:
            avg_marks[3] += i.est
            count += 1
            if i.est > highest_marks[3]:
                highest_marks[3] = i.est
            if i.est < lowest_marks[3]:
                lowest_marks[3] = i.est
    if count!=0:
        avg_marks[3] =  avg_marks[3]/count
    # -----------------------------------
    for i in marks_obj:
        if i.quiz1 is not None:
            curr_marks[0] = i.quiz1
        if i.mst is not None:
            curr_marks[1] = i.mst
        if i.quiz2 is not None:
            curr_marks[2] = i.quiz2
        if i.est is not None:
            curr_marks[3] = i.est
    # -----------------------------------
    for i in range(0,4):
        if lowest_marks[i]==100:
            lowest_marks[i]=0
    context_dict = {}
    for marks in marks_obj:
        context_dict['q1'] = marks.quiz1
        context_dict['q2'] = marks.quiz2
        context_dict['mst'] = marks.mst
        context_dict['est'] = marks.est
        total = 0
        outof = 0
        markexist = 0
        if marks.quiz1 is not None:
            markexist = 1
            outof += 10
            total += marks.quiz1
        if marks.quiz2 is not None:
            markexist = 1
            outof += 10
            total += marks.quiz2
        if marks.mst is not None:
            markexist = 1
            outof += 30
            total += marks.mst
        if marks.est is not None:
            markexist = 1
            outof += 50
            total += marks.est

        if markexist == 1:
            context_dict['percentage'] = int((total*100)/outof)
        else:
            context_dict['percentage'] = None
    context_dict['my_marks'] = curr_marks
    context_dict['avg_marks'] = avg_marks
    context_dict['highest_marks'] = highest_marks
    context_dict['lowest_marks'] = lowest_marks
    return render(request, 'student_marks.html', context_dict)

@login_required
def student_attendance_view(request):
    admin = UserInfo.objects.get(user = request.user)
    student = StudentInfo.objects.get(admin = admin)
    lst = []
    count_total = 0
    count_present = 0
    attendance_obj = Attendance.objects.filter(student_id = student, course_id = request.session['cid']).order_by('date')
    for i in attendance_obj:
        count_total += 1
        if i.status == True:
            count_present += 1
            lst.append((i.date, 'Present'))
        else:
            lst.append((i.date, 'Absent'))
    if count_total == 0:
        percentage = None
    else:
        percentage = int((count_present*100)/count_total)

    return render(request, 'student_attendance.html', {'attendance' : lst, 'percentage' : percentage})



@login_required
def teacher_attendance_view(request):
    if request.method == 'POST':
        date = request.POST.get('user_demand')
        request.session['date'] = date
        return redirect('view_attendance_url')
    admin = UserInfo.objects.get(user = request.user)
    teacher = TeacherInfo.objects.get(admin = admin)
    attendance_obj = Attendance.objects.filter(course_id = request.session['cid']).order_by('date')
    lst = []
    count = 0
    for i in attendance_obj:
        if i.date not in lst:
            lst.append(i.date)
            count += 1
    return render(request, 'teacher_attendance.html', {'dates' : lst, 'count' : count})


@login_required
def mark_attendance_view(request):
    course_instance = Course.objects.get(course_id = request.session['cid'])
    students_list = Course_taken.objects.filter(course_id = course_instance)
    lst = []
    for i in students_list:
        uname = i.student_id.admin.user.username
        if uname not in lst:
            lst.append(uname)
    lst.sort()
    if request.method == 'POST':
        for i in lst:
            user = User.objects.get(username = i)
            userinfo = UserInfo.objects.get(user = user)
            studentinfo = StudentInfo.objects.get(admin = userinfo)
            if request.POST.get(i) is not None:
                attendance_obj_lst = Attendance.objects.get_or_create(date=request.POST.get('date'),course_id = course_instance, student_id = studentinfo)
                attendance_obj=attendance_obj_lst[0]
                attendance_obj.status=True
                attendance_obj.save()
            else:
                attendance_obj_lst= Attendance.objects.get_or_create(date=request.POST.get('date'), course_id = course_instance, student_id = studentinfo)
                attendance_obj=attendance_obj_lst[0]
                attendance_obj.status=False
                attendance_obj.save()
        messages.success(request, 'Attendance updated successfully!')
        return redirect('teacher_attendance_url')
    return render(request, 'mark_attendance.html', {'students' : lst})


@login_required
def teacher_marks_view(request):
    students_list = Mark.objects.filter(course_id = request.session['cid'])
    lst = []
    student_lst = []
    for i in students_list:
        uname = i.student_id.admin.user.username
        if uname not in lst:
            lst.append(uname)
    lst.sort()
    for i in lst:
            user = User.objects.get(username = i)
            userinfo = UserInfo.objects.get(user = user)
            studentinfo = StudentInfo.objects.get(admin = userinfo)
            course_instance = Course.objects.get(course_id = request.session['cid'])
            marks_obj = Mark.objects.filter(student_id = studentinfo, course_id = course_instance)
            total = 0
            for obj in marks_obj:
                if obj.quiz1 is not None:
                    total += obj.quiz1
                if obj.quiz2 is not None:
                    total += obj.quiz2
                if obj.mst is not None:
                    total += obj.mst
                if obj.est is not None:
                    total += obj.est
                student_lst.append((obj, total))
    return render(request, 'teacher_marks.html', {'students' : student_lst})


@login_required
def mark_marks_view(request):
    students_list = Course_taken.objects.filter(course_id = request.session['cid'])
    lst = []
    for i in students_list:
        uname = i.student_id.admin.user.username
        if uname not in lst:
            lst.append(uname)
    lst.sort()
    if request.method == 'POST':
        user = User.objects.get(username = request.POST.get('sid'))
        userinfo = UserInfo.objects.get(user = user)
        studentinfo = StudentInfo.objects.get(admin = userinfo)
        course_instance = Course.objects.get(course_id = request.session['cid'])
        marks_obj = Mark.objects.get_or_create(student_id = studentinfo, course_id = course_instance)
        if request.POST.get('quiz1') == '':
            if marks_obj[0].quiz1 is None:
                marks_obj[0].quiz1 = None
        else:
            marks_obj[0].quiz1 = request.POST.get('quiz1')
        if request.POST.get('quiz2') == '':
            if marks_obj[0].quiz2 is None:
                marks_obj[0].quiz2 = None
        else:
            marks_obj[0].quiz2 = request.POST.get('quiz2')
        if request.POST.get('mst') == '':
            if marks_obj[0].mst is None:
                marks_obj[0].mst = None
        else:
            marks_obj[0].mst = request.POST.get('mst')
        if request.POST.get('est') == '':
            if marks_obj[0].est is None:
                marks_obj[0].est = None
        else:
            marks_obj[0].est = request.POST.get('est')
        marks_obj[0].save()
        messages.success(request, 'Marks updated successfully!')
        return redirect('teacher_marks_url')
    return render(request, 'mark_marks.html', {'students' : lst})


@login_required
def view_attendance_view(request):
    date = request.session['date']
    course_instance = Course.objects.get(course_id = request.session['cid'])
    instance_lst = Attendance.objects.filter(course_id = course_instance, date = parser.parse(date))
    attendance_lst = []
    nopresent = 0
    noabsent = 0
    for i in instance_lst:
        status_i = "Absent"
        if i.status:
            status_i = "Present"
            nopresent += 1
        else:
            noabsent += 1
        attendance_lst.append((i.student_id.admin.user.username, status_i))
    def myfun(item1):
        return item1[0]
    attendance_lst = sorted(attendance_lst, key=myfun)
    return render(request, 'view_attendance.html', {'date' : date, 'attendance' : attendance_lst, 'present':nopresent, 'absent':noabsent})


@login_required
def timetable_view(request):
    admin = UserInfo.objects.get(user = request.user)
    if admin.role == False:
        studentinfo = StudentInfo.objects.get(admin = admin)
        course_lst = Course_taken.objects.filter(student_id = studentinfo)
        courses_of_user = []
        for i in course_lst:
            courses_of_user.append(i.course_id.course_id)
    else:
        teacherinfo = TeacherInfo.objects.get(admin = admin)
        course_lst = Course_teaching.objects.filter(teacher_id = teacherinfo)
        courses_of_user = []
        for i in course_lst:
            courses_of_user.append(i.course_id.course_id)
    timetable_obj = Timetable.objects.filter(user_type = admin.role).order_by('day')
    context_dict = {}
    for i in timetable_obj:
        lst = []
        if  i.slot1 is not None and i.slot1.course_id in courses_of_user:
            lst.append(i.slot1.course_name)
        else:
            lst.append(None)
        if  i.slot2 is not None and i.slot2.course_id in courses_of_user:
            lst.append(i.slot2.course_name)
        else:
            lst.append(None)
        if  i.slot3 is not None and i.slot3.course_id in courses_of_user:
            lst.append(i.slot3.course_name)
        else:
            lst.append(None)
        if  i.slot4 is not None and i.slot4.course_id in courses_of_user:
            lst.append(i.slot4.course_name)
        else:
            lst.append(None)
        if i.slot5 is not None and i.slot5.course_id in courses_of_user:
            lst.append(i.slot5.course_name)
        else:
            lst.append(None)
#///////////////////////////////////////////////////
        if i.day == 1:
            context_dict['monday'] = lst
        elif i.day == 2:
            context_dict['tuesday'] = lst
        elif i.day == 3:
            context_dict['wednesday'] = lst
        elif i.day == 4:
            context_dict['thursday'] = lst
        else:
            context_dict['friday'] = lst
    return render(request, 'timetable.html', context_dict)
