from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


class Dormitories(models.Model):
    dormitory = models.CharField(max_length=20)
    dormdesc = models.CharField(max_length=50, null=True,blank=True)

    def __str__(self):
        return f'{self.dormitory}, {self.dormdesc}'


class Class(models.Model):
    class_name = models.CharField(max_length=20)
    class_teacher = models.OneToOneField(User, on_delete=models.CASCADE,null=True,blank=True)
    dormitory_id = models.ForeignKey(Dormitories, on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        return f'{self.class_name}, {self.dormitory_id.dormitory} , {self.class_teacher.first_name} {self.class_teacher.last_name}'

class Subject(models.Model):
    subject_name = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.subject_name}'

class Class_schedule(models.Model):
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE)
    subject_id = models.ForeignKey(Subject, on_delete=models.CASCADE)
    Day_of_week = [
        ('MON', 'MONDAY'),
        ('TUE', 'TUESDAY'),
        ('WED', 'WEDNESSDAY'),
        ('THU', 'THURSDAY'),
        ('FRI', 'FRIDAY'),
        ('SAT', 'SATURDAY'),
    ]
    day = models.CharField(
        max_length=3,
        choices=Day_of_week,
    )
    class Suit(models.IntegerChoices):
        period_1 = 1
        period_2 = 2
        period_3 = 3
        period_4 = 4
        period_5 = 5
        period_6 = 6
        period_7 = 7
        period_8 = 8

    Period = models.IntegerField(choices=Suit.choices)

    def __str__(self):
        return f'{self.class_id}, {self.day}, {self.subject_id}, {self.Period}'

class Exam_list(models.Model):
    exam_name = models.CharField(max_length=30)
    exam_desc = models.CharField(max_length=50)
    exam_date = models.DateField(auto_now=False, auto_now_add=False, null=True,blank=True)

    def __str__(self):
        return f'{self.exam_name}, {self.exam_date}'

class Student(models.Model):
    adm_no = models.CharField(max_length=50,primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    phone_no = models.BigIntegerField(default=1234567890)
    date_join = models.DateField(auto_now=False, auto_now_add=False)
    addhar_no = models.BigIntegerField()
    fathers_name = models.CharField(max_length=50)
    mothers_name = models.CharField(max_length=50)
    gender_choice = [
        ('M', 'MALE'),
        ('F', 'FEMALE'),
        ('O', 'OTHERS'),
    ]
    gender = models.CharField(
        max_length=1,
        choices=gender_choice,
    )
    date_of_birth = models.DateField(auto_now=False, auto_now_add=False)
    addrress = models.CharField(max_length=50)
    weight = models.CharField(max_length=50, null=True,blank=True)
    height = models.CharField(max_length=50, null=True,blank=True)
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE)
    roll_no = models.IntegerField()

    def __str__(self):
        return f'{self.adm_no}, {self.first_name} {self.last_name}'

class Exam_marks(models.Model):
    exam_id = models.ForeignKey(Exam_list, on_delete=models.CASCADE)
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE)
    subject_id = models.ForeignKey(Subject, on_delete=models.CASCADE)
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    marks = models.IntegerField(default=0)
    full_marks = models.IntegerField(default=100)

    def __str__(self):
        return f'{self.exam_id.exam_name}, {self.student_id}, {self.subject_id}'

class Attendance(models.Model):
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE)
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField(auto_now=False, auto_now_add=False)
    status_choice = [
        ('P', 'PRESENT'),
        ('A', 'ABSENT'),
    ]
    status = models.CharField(
        max_length=1,
        choices=status_choice,
    )

    def __str__(self):
        return f'{self.class_id}, {self.student_id}, {self.date}'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    addhar_no = models.BigIntegerField(null=True,blank=True)
    phone_no = models.BigIntegerField(null=True,blank=True)
    fathers_name = models.CharField(max_length=50)
    gender_choice = [
        ('M', 'MALE'),
        ('F', 'FEMALE'),
        ('O', 'OTHERS'),
    ]
    gender = models.CharField(
        max_length=1,
        choices=gender_choice,
    )
    date_of_birth = models.DateField(auto_now=False, auto_now_add=False)
    addrress = models.CharField(max_length=50,null=True,blank=True)
    subject = models.CharField(max_length=50,null=True,blank=True)
    e_id = models.IntegerField()

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}, E_ID: {self.e_id} Profile'


class Settings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    theme_elem =[
        ('dark-edition','dark-edition'),
        ('no-theme','no-theme'),
    ]
    theme = models.CharField(
        max_length=12,
        choices=theme_elem,
        default='no-theme',
    )
    exam_id = models.ForeignKey(Exam_list, on_delete=models.CASCADE, null=True,blank=True)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name} Settings'


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return f'{self.user.first_name} {self.timestamp}'


@receiver(post_save, sender=User)
def user_is_created (sender, instance, created, **kwargs):
    if created:
        Settings.objects.create(user=instance)
    else:
        instance.settings.save()
