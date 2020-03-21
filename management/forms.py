from django import forms
from .models import *

class SettingsForm(forms.ModelForm):
    class Meta:
        model = Settings
        fields = ['theme', 'exam_id']

class SearchAdmForm(forms.Form):
    adm_no = forms.CharField(max_length=50,label='Admission No')

    def save(self):
        return self.cleaned_data

class SearchPhForm(forms.Form):
    phone_no = forms.IntegerField(label='Phone No')

    def save(self):
        return self.cleaned_data

class SearchClForm(forms.Form):
    Class = forms.CharField(max_length=50,label='Class')

    def save(self):
        return self.cleaned_data

class SearchADMForm(forms.Form):
    adm_no = forms.CharField(max_length=50,label='Admission No')
    date_from = forms.DateField(label='From Date')
    date_to = forms.DateField(label='To Date')

    def save(self):
        return self.cleaned_data


class SearchStatusForm(forms.Form):
    status_choice = [
        ('P', 'PRESENT'),
        ('A', 'ABSENT'),
    ]
    status = forms.ChoiceField(choices = status_choice,label='Status')
    date = forms.DateField(label='Date')

    def save(self):
        return self.cleaned_data

class UpdateAttendanceForm(forms.Form):
    adm_no = forms.CharField(max_length=50,label='Admission No')
    date = forms.DateField(label='Date')

    def save(self):
        return self.cleaned_data

class AAttendanceForm(forms.Form):
    adm_no = forms.CharField(max_length=50,label='Admission No')

    def save(self):
        return self.cleaned_data

class AddAttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['student_id','date', 'status']

class SearchMarksForm(forms.Form):
    admission = forms.CharField(max_length=50,label='Admission No')

    def save(self):
        return self.cleaned_data

class UMarksForm(forms.Form):
    adm = forms.CharField(max_length=50,label='Admission No')
    subject_c=list(Subject.objects.values('subject_name'))
    subject_choice=[]
    for i in subject_c:
        subject_choice.append((i['subject_name'],i['subject_name']))
    subject = forms.ChoiceField(choices = subject_choice,label='Subject')

    def save(self):
        return self.cleaned_data

class AddMarksForm(forms.ModelForm):
    class Meta:
        model = Exam_marks
        fields = ['subject_id','marks', 'full_marks']

class AddNotificatationForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = ['text']

class RepoSetsForm(forms.Form):
    adm_no = forms.CharField(max_length=50,label='Admission No')
    exam_li_repo = forms.CharField(max_length=50,label='Exam ID (1stPractical,2nd Theory-SEPERATED BY COMMA):')
    seession = forms.CharField(max_length=200,label='Session')
    remarks = forms.CharField(max_length=200,label='Remarks')

    def save(self):
        return self.cleaned_data
