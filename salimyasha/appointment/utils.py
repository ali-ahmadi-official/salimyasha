from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
from django.utils import timezone
from django.utils.timezone import make_aware
from account.jalali import Persian
from .models import Appointment, Consultation

def expired_appointments():
    free_appointments = Appointment.objects.filter(status='آزاد')
    free_consultations = Consultation.objects.filter(status='آزاد')
    taked_appointments = Appointment.objects.filter(status='رزرو شده')
    taked_consultations = Consultation.objects.filter(status='رزرو شده')

    for free_appointment in free_appointments:
        geo_date = Persian(free_appointment.date).gregorian_datetime()
        start_datetime = datetime.combine(geo_date, free_appointment.start_time)
        start_datetime = make_aware(start_datetime)

        if start_datetime < timezone.now():
            free_appointment.delete()

    for free_consultation in free_consultations:
        geo_date = Persian(free_consultation.date).gregorian_datetime()
        start_datetime = datetime.combine(geo_date, free_consultation.start_time)
        start_datetime = make_aware(start_datetime)

        if start_datetime < timezone.now():
            free_consultation.delete()

    for taked_appointment in taked_appointments:
        geo_date = Persian(taked_appointment.date).gregorian_datetime()
        start_datetime = datetime.combine(geo_date, taked_appointment.start_time)
        start_datetime = make_aware(start_datetime)

        if start_datetime > timezone.now() + timedelta(hours=48):
            taked_appointment.cancle = True
            taked_appointment.save()
        else:
            taked_appointment.cancle = False
            taked_appointment.save()

        if start_datetime < timezone.now():
            taked_appointment.status = 'تکمیل شده'
            taked_appointment.save()

    for taked_consultation in taked_consultations:
        geo_date = Persian(taked_consultation.date).gregorian_datetime()
        start_datetime = datetime.combine(geo_date, taked_consultation.start_time)
        start_datetime = make_aware(start_datetime)
        end_datetime = datetime.combine(geo_date, taked_consultation.end_time)
        end_datetime = make_aware(end_datetime)

        if start_datetime <= timezone.now() and timezone.now() <= end_datetime:
            taked_consultation.allowed = True
            taked_consultation.save()
        else:
            taked_consultation.allowed = False
            taked_consultation.save()
        
        if start_datetime > timezone.now() + timedelta(hours=48):
            taked_consultation.cancle = True
            taked_consultation.save()
        else:
            taked_consultation.cancle = False
            taked_consultation.save()

        if end_datetime < timezone.now():
            taked_consultation.status = 'تکمیل شده'
            taked_consultation.save()

def start_delete_expired_appointments():
    scheduler = BackgroundScheduler()
    scheduler.add_job(expired_appointments, 'interval', minutes=1)
    scheduler.start()