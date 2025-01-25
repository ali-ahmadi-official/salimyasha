from django.db import models
from django.utils import timezone
from account.models import CustomUser

class Amount(models.Model):
    amount = models.IntegerField(verbose_name='مبلغ خدمات', help_text='مبلغ را به ریال و بدون استفاده از کاما وارد کنید.')

    class Meta:
        verbose_name = 'مبلغ خدمات'
        verbose_name_plural = 'مبالغ خدمات'
    
    def __str__(self):
        return f'مبلغ خدمات'

class Transaction(models.Model):
    status = models.IntegerField(verbose_name='وضعیت', help_text='1 به معنای تراکنش موفق است')
    amount = models.CharField(max_length=20, verbose_name='مبلغ به ریال')
    transId = models.CharField(max_length=20, verbose_name='شماره تراکنش')
    factorNumber = models.CharField(max_length=20, verbose_name='شماره فاکتور', help_text='همان شناسه نوبت یا مشاوره است')
    mobile = models.CharField(max_length=10, verbose_name='شماره موبایل')
    description = models.TextField(verbose_name='توضیحات')

    class Meta:
        verbose_name = 'تراکنش'
        verbose_name_plural = 'تراکنش ها'
    
    def __str__(self):
        return f'تراکنش شماره {self.transId}'

class TemplateAppointment(models.Model):
    template_day = [
        ('0', 'روز های شنبه'),
        ('1', 'روز های یک شنبه'),
        ('2', 'روز های دو شنبه'),
        ('3', 'روز های سه شنبه'),
        ('4', 'روز های چهار شنبه'),
        ('5', 'روز های پنج شنبه'),
        ('6', 'روز های جمعه'),
    ]
    doctor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='td', verbose_name='دکتر')
    day = models.CharField(max_length=30, choices=template_day, verbose_name='روز هفته')
    start_time = models.TimeField(verbose_name='ساعت شروع', default=timezone.now)
    end_time = models.TimeField(verbose_name='ساعت پایان', default=timezone.now)

    class Meta:
        verbose_name = 'الگو نوبت دهی'
        verbose_name_plural = 'الگو های نوبت دهی'
    
    def __str__(self):
        return f'الگو نوبت دهی برای {self.doctor}'

class Appointment(models.Model):
    appointment_status = [
        ('آزاد', 'آزاد'),
        ('رزرو شده', 'رزرو شده'),
        ('تکمیل شده', 'تکمیل شده'),
    ]
    method_choices = [
        ('1', 'از روی الگو'),
        ('2', 'خارج از الگو'),
    ]
    method = models.CharField(max_length=1, choices=method_choices, verbose_name='روش ایجاد')
    doctor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='doctor_appointment', verbose_name='دکتر')
    patient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='patient_appointment', verbose_name='بیمار', null=True, blank=True)
    date = models.CharField(max_length= 10, verbose_name='تاریخ نوبت')
    start_time = models.TimeField(verbose_name='ساعت شروع', default=timezone.now)
    status = models.CharField(max_length=20, choices=appointment_status, default='آزاد', verbose_name='وضعیت نوبت')
    cancle = models.BooleanField(default=False, verbose_name='اجازه کنسل')

    class Meta:
        verbose_name = 'نوبت'
        verbose_name_plural = 'نوبت ها'
    
    def __str__(self):
        return f'نوبت برای {self.patient} از {self.doctor}'

class Consultation(models.Model):
    consultation_status = [
        ('آزاد', 'آزاد'),
        ('رزرو شده', 'رزرو شده'),
        ('تکمیل شده', 'تکمیل شده'),
    ]
    method_choices = [
        ('1', 'از روی الگو'),
        ('2', 'خارج از الگو'),
    ]
    method = models.CharField(max_length=1, choices=method_choices, default='2', verbose_name='روش ایجاد')
    doctor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='doctor_consultation', verbose_name='دکتر')
    patient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='patient_consultation', verbose_name='بیمار', null=True, blank=True)
    date = models.CharField(max_length= 10, verbose_name='تاریخ مشاوره')
    start_time = models.TimeField(verbose_name='ساعت شروع', default=timezone.now)
    end_time = models.TimeField(verbose_name='ساعت پایان', default=timezone.now)
    status = models.CharField(max_length=20, choices=consultation_status, default='آزاد', verbose_name='وضعیت مشاوره')
    allowed = models.BooleanField(default=False, verbose_name='اجازه چت')
    cancle = models.BooleanField(default=False, verbose_name='اجازه کنسل')

    class Meta:
        verbose_name = 'مشاوره'
        verbose_name_plural = 'مشاوره ها'
    
    def __str__(self):
        return f'مشاوره برای {self.patient} از {self.doctor}'

class Message(models.Model):
    consultation = models.ForeignKey(Consultation, on_delete=models.CASCADE, related_name='consultation_message', verbose_name='مشاوره', default='')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='author_message', verbose_name='نویسنده')
    text = models.TextField(verbose_name='متن پیام')
    file = models.FileField(verbose_name='فایل ضمیمه', null=True, blank=True, upload_to='message_files/')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='تاریخ ارسال')

    class Meta:
        verbose_name = 'پیام'
        verbose_name_plural = 'پیام ها'

    def __str__(self):
        return f'پیام از طرف {self.author}'
    
    def save(self, *args, **kwargs):
        self.created_at = timezone.now()
        super().save(*args, **kwargs)

class AppointmentComment(models.Model):
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, verbose_name='نوبت')
    star = models.CharField(max_length=1, verbose_name='ستاره', default='5')
    content = models.CharField(max_length=800, verbose_name='متن نظر')
    date = models.DateField(default=timezone.now, verbose_name='تاریخ')
    
    class Meta:
        verbose_name = 'نظر'
        verbose_name_plural = 'نظرات'

    def __str__(self):
        return f'از طرف {self.appointment.patient} برای نوبت از {self.appointment.doctor}'
    
class ConsultationComment(models.Model):
    consultation = models.OneToOneField(Consultation, on_delete=models.CASCADE, verbose_name='مشاوره')
    star = models.CharField(max_length=1, verbose_name='ستاره', default='5')
    content = models.CharField(max_length=800, verbose_name='متن نظر')
    date = models.DateField(default=timezone.now, verbose_name='تاریخ')
    
    class Meta:
        verbose_name = 'نظر'
        verbose_name_plural = 'نظرات'

    def __str__(self):
        return f'از طرف {self.consultation.patient} برای مشاوره از {self.consultation.doctor}'