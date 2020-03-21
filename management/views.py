from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from .models import *
import datetime
from django.db.models import Sum
from .forms import *
from django.core.cache import cache
from .decorators import superuser_only,class_teacher_only
#@superuser_only

#from django.contrib.auth.decorators import user_passes_test
#@user_passes_test(lambda u: u.is_superuser)
#use the upper for only superuser access

# Create your views here.

@login_required
def home(request):
    di={'title': 'Dashboard'}
    di['noti_b_object'] = Notification.objects.all().order_by('-timestamp')
    class_t_o = Class.objects.filter(class_teacher= request.user).first()
    if request.user.is_superuser:
        try:
            date_today = Attendance.objects.filter(date=str(datetime.date.today()),status='P').count()
            date_yesterday = Attendance.objects.filter(date=str(datetime.date.today() - datetime.timedelta(days=1)),status='P').count()
            percent = ((date_today/Student.objects.filter().count())*100) - ((date_yesterday/Student.objects.filter().count())*100)
            di['att_per'] = percent
            stu = Student.objects.filter(date_join=str(datetime.date.today())).count()
            di['stu'] = stu
            birth1 = Student.objects.filter(date_of_birth=str(datetime.date.today())).count()
            di['birth1'] = birth1
            birth2 = Profile.objects.filter(date_of_birth=str(datetime.date.today())).count()
            di['birth2'] = birth2
            di['class'] = Class.objects.filter().count()
            di['studcou'] = Student.objects.filter().count()
            di['teacher'] = Profile.objects.filter().count()
            di['build'] = Dormitories.objects.filter().count()
            marks_dict = {}
            for i in Student.objects.all().distinct():
                marks_dict[i.adm_no]=Exam_marks.objects.filter(student_id=i,exam_id=request.user.settings.exam_id).aggregate(Sum('marks'))['marks__sum']
            x=[]
            l=list(marks_dict.values())
            l.sort()
            for i in range(len(l)):
                for j in marks_dict:
                    if marks_dict[j]==l[i]:
                         x.append(j)
            marks_dict=dict(zip(x,l))
            key_list = list(marks_dict.keys())
            varc,di_di=1,{}
            for i in key_list[-1:-5:-1]:
                dict_ee = {}
                dict_ee['position'] = varc
                dict_ee['name_'] = Student.objects.filter(adm_no=i).first().first_name+ ' ' + Student.objects.filter(adm_no=i).first().last_name
                dict_ee['marks'] = marks_dict[i]
                dict_ee['class_'] = Student.objects.filter(adm_no=i).first().class_id.class_name
                di_di[str(varc)+'child']=dict_ee
                varc+=1
            di['di']=di_di
        except Exception as e:
            if str(e) == "\'<\' not supported between instances of \'NoneType\' and \'NoneType\'":
                messages.error(request, 'Please Select an Examination for Student Stats')
            else:
                messages.error(request, e)
    elif not class_t_o:
        di['jt'] = 0
    else:
        try:
            cl_na = Class.objects.filter(class_teacher= request.user).first()
            date_today = Attendance.objects.filter(date=str(datetime.date.today()),status='P',class_id = cl_na).count()
            date_yesterday = Attendance.objects.filter(date=str(datetime.date.today() - datetime.timedelta(days=1)),status='P',class_id = cl_na).count()
            percent = ((date_today/Student.objects.filter(class_id=cl_na).count())*100) - ((date_yesterday/Student.objects.filter(class_id=cl_na).count())*100)
            di['att_per'] = percent
            stu = Student.objects.filter(date_join=str(datetime.date.today()),class_id=cl_na).count()
            di['stu'] = stu
            birth1 = Student.objects.filter(date_of_birth=str(datetime.date.today()),class_id=cl_na).count()
            di['birth1'] = birth1
            birth2 = Profile.objects.filter(date_of_birth=str(datetime.date.today())).count()
            di['birth2'] = birth2
            marks_dict = {}
            for i in Student.objects.filter(class_id=cl_na).distinct():
                marks_dict[i.adm_no]=Exam_marks.objects.filter(student_id=i,exam_id=request.user.settings.exam_id).aggregate(Sum('marks'))['marks__sum']
            x=[]
            l=list(marks_dict.values())
            l.sort()
            for i in range(len(l)):
                for j in marks_dict:
                    if marks_dict[j]==l[i]:
                         x.append(j)
            marks_dict=dict(zip(x,l))
            key_list = list(marks_dict.keys())
            varc,di_di=1,{}
            for i in key_list[-1:-5:-1]:
                dict_ee = {}
                dict_ee['position'] = varc
                dict_ee['name_'] = Student.objects.filter(adm_no=i).first().first_name+ ' ' + Student.objects.filter(adm_no=i).first().last_name
                dict_ee['marks'] = marks_dict[i]
                dict_ee['class_'] = Student.objects.filter(adm_no=i).first().class_id.class_name
                di_di[str(varc)+'child']=dict_ee
                varc+=1
            di['di']=di_di
            birth_dict=Student.objects.filter(date_of_birth=str(datetime.date.today()),class_id=cl_na).distinct()
            di['birth_dict']=birth_dict
        except Exception as e:
            messages.error(request, e)
    try:
        users = Settings.objects.get(user=request.user)
        if request.method == 'POST':
            form = SettingsForm(request.POST,instance=users)
            # check whether it's valid:
            if form.is_valid():
                # process the data in form.cleaned_data as require
                data = form.save()
                messages.success(request, 'Your Settings was successfully updated!')
                # redirect to a new URL:
                return redirect('home')
            else:
                messages.error(request, 'Some error occured!')

        # if a GET (or any other method) we'll create a blank form
        else:
            form = SettingsForm(instance=users)
            di['form'] = form
    except Exception as e:
        messages.error(request, 'Tell the administrator to add you in Settings Database!')
    return render(request, 'home.html' ,di)

def logout_view(request):
    logout(request)
    messages.success(request, f'You have been logged out, Please Login again!')
    return redirect('login')

@login_required
def profile(request):
    di={'title':'Profile'}
    di['noti_b_object'] = Notification.objects.all().order_by('-timestamp')
    class_t_o = Class.objects.filter(class_teacher= request.user).first()
    if not class_t_o:
        di['jt'] = 0
    return render(request, 'profile.html',di)

@login_required
def change_password(request):
    di={'form': form,'title':'Password Change'}
    di['noti_b_object'] = Notification.objects.all().order_by('-timestamp')
    class_t_o = Class.objects.filter(class_teacher= request.user).first()
    if not class_t_o:
        di['jt'] = 0
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('/profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change-password.html', di)


@login_required
@superuser_only
def classes(request):
    dict = {'title': 'Classes'}
    dict['noti_b_object'] = Notification.objects.all()
    dict_class, varc={},1
    for i in Class.objects.all():
        dict_ee={}
        dict_ee['#'] = varc
        dict_ee['class'] = i.class_name
        dict_ee['class_teacher'] = i.class_teacher
        dict_ee['block'] = i.dormitory_id
        dict_class[varc] = dict_ee
        varc+=1
    dict['di'] = dict_class
    return render(request,'classes.html' , dict)

@login_required
def student(request):
    class_t_o = Class.objects.filter(class_teacher= request.user).first()
    if not class_t_o:
        return render(request, '403.html')
    dict = {'title': 'Student'}
    dict['noti_b_object'] = Notification.objects.all()
    dict['adm_obj'] = cache.get('adm_obj')
    dict['ph_obj'] = cache.get('ph_obj')
    dict['cl_obj'] = cache.get('cl_obj')
    cache.clear()

    if request.user.is_superuser:
        dict['male'] = Student.objects.filter(gender='M').count()
        dict['other'] = Student.objects.filter(gender='O').count()
        dict['female'] = Student.objects.filter(gender='F').count()

    if not request.user.is_superuser:
        stuli={}
        cl_na = Class.objects.filter(class_teacher= request.user).first()
        for i in Student.objects.filter(class_id=cl_na).distinct():
            stuli[i.adm_no]=i.first_name + ' ' +i.last_name
        dict['stuli'] = stuli
        dict['male'] = Student.objects.filter(gender='M',class_id=cl_na).count()
        dict['female'] = Student.objects.filter(gender='F',class_id=cl_na).count()
        dict['other'] = Student.objects.filter(gender='O',class_id=cl_na).count()

    if request.method == 'POST':
        form = SearchAdmForm(request.POST)
        form1 = SearchPhForm(request.POST)
        form2 = SearchClForm(request.POST)
        if form.is_valid():
            adm_no = form.save()
            if request.user.is_superuser:
                adm_obj = Student.objects.filter(adm_no=adm_no['adm_no'])
            else:
                cl_na = Class.objects.filter(class_teacher= request.user).first()
                adm_obj = Student.objects.filter(adm_no=adm_no['adm_no'],class_id=cl_na)
            cache.set('adm_obj',adm_obj)
            return redirect('student')
        elif form1.is_valid():
            phone_no = form1.save()
            if request.user.is_superuser:
                ph_obj = Student.objects.filter(phone_no=phone_no['phone_no'])
            else:
                cl_na = Class.objects.filter(class_teacher= request.user).first()
                ph_obj = Student.objects.filter(phone_no=phone_no['phone_no'],class_id=cl_na)
            cache.set('ph_obj',ph_obj)
            return redirect('student')
        elif form2.is_valid():
            class_name = form2.save()
            cll = Class.objects.filter(class_name=class_name['Class']).first().id
            cl_obj = Student.objects.filter(class_id = cll)
            cache.set('cl_obj',cl_obj)
            return redirect('student')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = SearchAdmForm()
        form1 = SearchPhForm()
        form2 = SearchClForm()
        dict['form'] = form
        dict['form1'] = form1
        dict['form2'] = form2
    return render(request,'student.html' , dict)

@login_required
@class_teacher_only
def attendance(request):
    di = {'title': 'Attendance'}
    di['noti_b_object'] = Notification.objects.all().order_by('-timestamp')
    class_t_o = Class.objects.filter(class_teacher= request.user).first()
    di['present'] = Attendance.objects.filter(status='P',class_id=class_t_o,date=str(datetime.date.today())).count()
    di['absent'] = Attendance.objects.filter(status='A',class_id=class_t_o,date=str(datetime.date.today())).count()
    di['stat_at'] = cache.get('stat_at')
    di['tsat_obj'] = cache.get('tsat_obj')
    di['tsat_obj_co'] = cache.get('tsat_obj_co')

    if cache.get('messgae'):
        messages.success(request, cache.get('messgae'))
    cache.clear()

    if request.method == 'POST':
        form = SearchADMForm(request.POST)
        form1 = UpdateAttendanceForm(request.POST)
        form2 = SearchStatusForm(request.POST)
        form3 = AAttendanceForm(request.POST)
        if form.is_valid():
            adm_no = form.save()
            try:
                stu_id=Student.objects.filter(adm_no=adm_no['adm_no']).first()
                stu_p = Attendance.objects.filter(class_id=class_t_o,student_id=stu_id,status='P',date__gte=adm_no['date_from'],date__lte=adm_no['date_to']).count()
                stu_a = Attendance.objects.filter(class_id=class_t_o,student_id=stu_id,status='A',date__gte=adm_no['date_from'],date__lte=adm_no['date_to']).count()
                stu_t=stu_p+stu_a
                percent=stu_p/stu_t*100
                stat_at={'#':1,'Total Working Days': stu_t,'Present':stu_p,'Absent':stu_a,'Percentage':percent}
                cache.set('stat_at',stat_at)
            except Exception as e:
                cache.set('messgae','The Student either dosent exist or is not present in your class')
            return redirect('attendance')
        elif form1.is_valid():
            update_p = form1.save()
            cache.set('update_p',update_p)
            return redirect('updateattendance')
        elif form2.is_valid():
            status_cl = form2.save()
            tsat_obj = Attendance.objects.filter(class_id=class_t_o,status=status_cl['status'],date=status_cl['date'])
            cache.set('tsat_obj_co',tsat_obj.count())
            cache.set('tsat_obj',tsat_obj)
            return redirect('attendance')
        elif form3.is_valid():
            add_p = form3.save()
            cache.set('add_p',add_p)
            return redirect('add-attendance')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = SearchADMForm()
        form1 = UpdateAttendanceForm()
        form2 = SearchStatusForm()
        form3=AAttendanceForm()
        di['form'] = form
        di['form1'] = form1
        di['form2'] = form2
        di['form3'] = form3
    return render(request, 'attendance.html', di)

@login_required
@class_teacher_only
def updateattendance(request):
    di={'title':'Update Attendance','update':'update'}
    di['noti_b_object'] = Notification.objects.all().order_by('-timestamp')
    di['update_p'] = cache.get('update_p')
    class_t_o = Class.objects.filter(class_teacher= request.user).first()

    if request.method == 'POST':
        stu_oj=Student.objects.filter(adm_no=di['update_p']['adm_no']).first()
        childs = Attendance.objects.get(student_id=stu_oj,date=di['update_p']['date'])
        form = AddAttendanceForm(request.POST,instance=childs)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as require
            data = form.save()
            cache.clear()
            messages.success(request, 'successfully updated!')
            # redirect to a new URL:
            return redirect('attendance')
        else:
            messages.error(request, 'Some error occured!')

    # if a GET (or any other method) we'll create a blank form
    else:
        try:
            stu_oj=Student.objects.filter(adm_no=di['update_p']['adm_no']).first()
            childs = Attendance.objects.get(student_id=stu_oj,date=di['update_p']['date'])
            form = AddAttendanceForm(instance=childs)
            di['form'] = form
        except:
            messages.error(request, 'Please enter correct details!')
            return redirect('attendance')

    return render(request,'changeattendance.html',di)

@login_required
@class_teacher_only
def addattendance(request):
    di={'title':'Add Attendance','add':'add'}
    di['noti_b_object'] = Notification.objects.all().order_by('-timestamp')
    di['add_p'] = cache.get('add_p')
    class_t_o = Class.objects.filter(class_teacher= request.user).first()
    stu_oj=Student.objects.filter(adm_no=di['add_p']['adm_no']).first()
    childs = Attendance(student_id=stu_oj,class_id=class_t_o)
    if request.method == 'POST':
        form = AddAttendanceForm(request.POST,instance=childs)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as require
            data = form.save()
            cache.clear()
            messages.success(request, 'successfully added!')
            # redirect to a new URL:
            return redirect('attendance')
        else:
            messages.error(request, 'Some error occured!')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = AddAttendanceForm(instance=childs)
        di['form'] = form
    return render(request,'changeattendance.html',di)

@login_required
@class_teacher_only
def examarks(request):
    di={'title':'Exam Marks'}
    di['noti_b_object'] = Notification.objects.all().order_by('-timestamp')
    class_t_o = Class.objects.filter(class_teacher= request.user).first()
    exam_id=request.user.settings.exam_id
    di['mark_object'] = cache.get('mark_object')

    if cache.get('messgae'):
        messages.success(request, cache.get('messgae'))
    cache.clear()
    if request.method == 'POST':
        form = SearchAdmForm(request.POST)
        form1 = UMarksForm(request.POST)
        form2 = SearchMarksForm(request.POST)
        if form.is_valid():
            data = form.save()
            cache.set('uamdata',data)
            return redirect('aexamarks')
        elif form1.is_valid():
            data1 = form1.save()
            cache.set('umdata',data1)
            return redirect('uexamarks')
        elif form2.is_valid():
            adm_no = form2.save()
            try:
                stu_id=Student.objects.filter(adm_no=adm_no['admission']).first()
                mark_object = Exam_marks.objects.filter(exam_id=exam_id,class_id=class_t_o,student_id=stu_id)
                cache.set('mark_object',mark_object)
            except Exception as e:
                cache.set('messgae','The Student either dosent exist or is not present in your class')
            return redirect('examarks')
        else:
            messages.error(request, 'Some error occured!')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = SearchAdmForm()
        form1 = UMarksForm()
        form2 = SearchMarksForm()
        di['form'] = form
        di['form1'] = form1
        di['form2'] = form2
    return render(request, 'examarks.html', di)

@login_required
@class_teacher_only
def aexamarks(request):
    di={'title':'Exam Marks','addm':'addm'}
    di['noti_b_object'] = Notification.objects.all().order_by('-timestamp')
    di['uamdata'] = cache.get('uamdata')
    class_t_o = Class.objects.filter(class_teacher= request.user).first()
    exam_id=request.user.settings.exam_id
    stu_oj=Student.objects.filter(adm_no=di['uamdata']['adm_no']).first()
    childs=Exam_marks(exam_id=exam_id,class_id=class_t_o,student_id=stu_oj)
    if request.method == 'POST':
        form = AddMarksForm(request.POST,instance=childs)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as require
            data = form.save()
            print(data)
            cache.clear()
            messages.success(request, 'successfully added!')
            # redirect to a new URL:
            return redirect('examarks')
        else:
            messages.error(request, 'Some error occured!')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = AddMarksForm(instance=childs)
        di['form'] = form
    return render(request, 'examarks.html', di)


@login_required
@class_teacher_only
def uexamarks(request):
    di={'title':'Exam Marks','addm':'addm'}
    di['noti_b_object'] = Notification.objects.all().order_by('-timestamp')
    di['umdata'] = cache.get('umdata')
    class_t_o = Class.objects.filter(class_teacher= request.user).first()
    exam_id=request.user.settings.exam_id
    if request.method == 'POST':
        stu_oj=Student.objects.filter(adm_no=di['umdata']['adm']).first()
        sub_oj=Subject.objects.filter(subject_name =di['umdata']['subject']).first()
        childs=Exam_marks.objects.get(exam_id=exam_id,class_id=class_t_o,student_id=stu_oj,subject_id=sub_oj)
        form = AddMarksForm(request.POST,instance=childs)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as require
            data = form.save()
            cache.clear()
            messages.success(request, 'successfully added!')
            # redirect to a new URL:
            return redirect('examarks')
        else:
            messages.error(request, 'Some error occured!')

    # if a GET (or any other method) we'll create a blank form
    else:
        try:
            stu_oj=Student.objects.filter(adm_no=di['umdata']['adm']).first()
            sub_oj=Subject.objects.filter(subject_name =di['umdata']['subject']).first()
            childs=Exam_marks.objects.get(exam_id=exam_id,class_id=class_t_o,student_id=stu_oj,subject_id=sub_oj)
            print(childs)
            form = AddMarksForm(instance=childs)
            di['form'] = form
        except:
            messages.error(request, 'please enter correct values!')
            return redirect('examarks')
    return render(request, 'examarks.html', di)

@login_required
@class_teacher_only
def schedule(request):
    di = {'title':'Class Schedule'}
    di['noti_b_object'] = Notification.objects.all().order_by('-timestamp')
    class_t_o = Class.objects.filter(class_teacher= request.user).first()
    di['schedule'] = Class_schedule.objects.filter(class_id=class_t_o)
    di['schedule_m'] = Class_schedule.objects.filter(class_id=class_t_o,day='MON').order_by('Period')
    di['schedule_t'] = Class_schedule.objects.filter(class_id=class_t_o,day='TUE').order_by('Period')
    di['schedule_w'] = Class_schedule.objects.filter(class_id=class_t_o,day='WED').order_by('Period')
    di['schedule_th'] = Class_schedule.objects.filter(class_id=class_t_o,day='THU').order_by('Period')
    di['schedule_f'] = Class_schedule.objects.filter(class_id=class_t_o,day='FRI').order_by('Period')
    di['schedule_s'] = Class_schedule.objects.filter(class_id=class_t_o,day='SAT').order_by('Period')

    return render(request, 'schedule.html', di)

@login_required
@superuser_only
def pushnotification(request):
    di={'title':'Push Notification'}
    di['noti_b_object'] = Notification.objects.all().order_by('-timestamp')
    childs=Notification(user=request.user)
    di['noti_object'] = Notification.objects.all()
    if request.method == 'POST':
        form = AddNotificatationForm(request.POST,instance=childs)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as require
            data = form.save()
            messages.success(request, 'successfully added!')
            # redirect to a new URL:
            return redirect('pushnotification')
        else:
            messages.error(request, 'Some error occured!')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = AddNotificatationForm(instance=childs)
        di['form'] = form
    return render(request, 'pushnotification.html', di)

@login_required
@superuser_only
def delete_noti(request,pk):
    id = pk
    try:
        Notification.objects.get(pk=id).delete()
        messages.success(request, 'successfully Deleted!')
    except Exception as e:
        messages.error(request, e)
    return redirect('pushnotification')

def report_card(request):
    di={'title': 'Report Card'}
    di['noti_b_object'] = Notification.objects.all().order_by('-timestamp')
    di['exam_li'] = Exam_list.objects.all()
    cache.clear()
    if request.method == 'POST':
        form = RepoSetsForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as require
            repo_set = form.save()
            cache.set('repo_set',repo_set)
            return redirect('repo_result')
        else:
            messages.error(request, 'Some error occured!')
    else:
        form = RepoSetsForm()
        di['form'] = form
    return render(request,'report-card.html', di)


def repo_result(request):
    di={'title': 'Report Card'}
    set_di = cache.get('repo_set')
    di['session'] = set_di['seession']
    di['remarks'] = set_di['remarks']
    di['stu_obj'] = Student.objects.filter(adm_no=set_di['adm_no']).first()
    exam1,exam2 = set_di['exam_li_repo'][:2]
    class_t_o = Class.objects.filter(class_teacher= request.user).first()
    m_di={}
    fail,total,ftotal=0,0,0
    for i in Exam_marks.objects.filter(exam_id=Exam_list.objects.filter(id=2).first(),class_id=class_t_o,student_id=di['stu_obj']):
        audi={}
        for j in Exam_marks.objects.filter(exam_id=Exam_list.objects.filter(id=1).first(),class_id=class_t_o,student_id=di['stu_obj']):
            if j.subject_id == i.subject_id:
                audi['subject'] = i.subject_id.subject_name
                audi['practicle'] = j.marks
                audi['fullpracticle'] = j.full_marks
                audi['theory'] = i.marks
                audi['fulltheory'] = i.full_marks
                audi['total']= str(audi['practicle']+audi['theory'])+'/'+str(audi['fullpracticle'] + audi['fulltheory'])
                if (audi['practicle']+audi['theory']) >= 90:
                    grade='A+'
                elif (audi['practicle']+audi['theory']) >= 80:
                    grade='A'
                elif (audi['practicle']+audi['theory']) >= 70:
                    grade='B+'
                elif (audi['practicle']+audi['theory']) >= 60:
                    grade='B'
                elif (audi['practicle']+audi['theory']) >= 50:
                    grade='C'
                elif (audi['practicle']+audi['theory']) >= 40:
                    grade='D'
                elif (audi['practicle']+audi['theory']) >= 33:
                    grade='E'
                else:
                    grade='F'
                    fail+=1
                audi['grade'] = grade
                total+=(audi['practicle']+audi['theory'])
                ftotal+=(audi['fullpracticle'] + audi['fulltheory'])
        if audi:
            m_di[audi['subject']]=audi
    m_di.update({'Total':{'subject':'Total','practicle':'-','fpracticle':'-','tpracticle':'-','ftpracticle':'-','total':(str(total)+'/'+str(ftotal)),'grade':('Pass' if fail < 1 else 'Fail')}})
    di['m_di']=m_di

    return render(request,'report-result.html', di)
