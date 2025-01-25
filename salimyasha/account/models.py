from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.utils import timezone
from .cities import CITY_CHOICES
from .expertise import EXPERTISE_CHOICES

class CustomUser(AbstractUser):
    user_type_choices = [
        ('بیمار', 'بیمار'),
        ('دکتر', 'دکتر'),
    ]
    user_type = models.CharField(max_length=10, choices=user_type_choices, null=True, blank=True, verbose_name='نوع کاربر')
    profile_image = models.ImageField(default='default/profile.jpg', upload_to='user_photos/', verbose_name='تصویر پروفایل')
    phone_number = models.CharField(max_length=10, validators=[RegexValidator(r'^\d{10}$', message='شماره موبایل باید 10 رقمی باشد')], verbose_name='شماره تلفن', default='9123456789')
    phone_number_verification = models.BooleanField(verbose_name='تایید شماره موبایل', default=False)
    email = models.EmailField(blank=True, null=True, verbose_name='ایمیل')

    class Meta:
        verbose_name = 'اکانت'
        verbose_name_plural = 'اکانت‌ ها'

    def __str__(self):
        if self.first_name or self.last_name:
            if self.user_type:
                return f'{self.user_type} {self.first_name} {self.last_name}'
            else:
                return f'{self.first_name} {self.last_name}'
        else:
            return self.username
    
class PatientProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='patientprofile')
    national_id = models.CharField(max_length=10, verbose_name='کد ملی', default='')
    birth_date = models.CharField(max_length= 10, verbose_name='تاریخ تولد', default='')
    inventory = models.IntegerField(verbose_name='موجودی کیف پول', default=0)

    class Meta:
        verbose_name = 'پروفایل بیمار'

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

class DoctorProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='doctorprofile')
    account_verification = models.BooleanField(verbose_name='تایید حساب کاربری', default=False)
    father_name = models.CharField(max_length=100, verbose_name='نام پدر')
    national_id = models.CharField(max_length=10, verbose_name='کد ملی')
    medical_system_number = models.CharField(max_length=10, verbose_name='شماره نظام پزشکی')
    birth_date = models.CharField(max_length= 10, verbose_name='تاریخ تولد', default='')
    bio = models.TextField(default='', verbose_name='معرفی پزشک')
    city = models.CharField(max_length=100, choices=CITY_CHOICES, verbose_name='شهر / استان')
    expertise = models.CharField(max_length=100, choices=EXPERTISE_CHOICES, default='', verbose_name='تخصص')

    class Meta:
        verbose_name = 'پروفایل پزشک'

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

class Clinic(models.Model):
    doctor = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name='نام مطب')
    location = models.CharField(max_length=1000, verbose_name='لوکیشن', null=True, blank=True)
    address = models.CharField(max_length=500, verbose_name='آدرس مطب')

    class Meta:
        verbose_name = 'مطب پزشک'

    def __str__(self):
        return 'مطب پزشک'
    
class Ticket(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='کاربر')
    message = models.TextField(verbose_name='مشکل و یا سوال کاربر')
    date = models.DateField(default=timezone.now, verbose_name='تاریخ میلادی ارسال')
    answer = models.TextField(verbose_name='پاسخ ادمین')

    class Meta:
        verbose_name = 'تیکت کاربر'
        verbose_name_plural = 'تیکت های کاربران'

    def __str__(self):
        return f'تیکت از طرف {self.user}'