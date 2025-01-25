from django.db import models
from django.utils import timezone

class Contact(models.Model):
    name = models.CharField(max_length=100, verbose_name='نام')
    email = models.EmailField(verbose_name='ایمیل')
    subject = models.CharField(max_length=100, verbose_name='عنوان')
    message = models.TextField(verbose_name='متن پیام')
    date = models.DateField(default=timezone.now, verbose_name='تاریخ ارسال')

    class Meta:
        verbose_name = 'پیام کاربر'
        verbose_name_plural = 'پیام های کاربران'
    
    def __str__(self):
        return 'پیام کاربر'