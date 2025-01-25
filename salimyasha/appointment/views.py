import requests
from functools import wraps
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from .models import Amount, Transaction, Appointment, Consultation

def login_required_decorator(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('patient_login')
        return function(request, *args, **kwargs)
    return wrap

@login_required_decorator
def take_appointment(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.method == 'POST' and appointment.status == 'آزاد' and request.user.user_type == 'بیمار' and request.user.patientprofile:
        inventory = request.user.patientprofile.inventory
        amount_model = Amount.objects.get(pk=1)
        amount = amount_model.amount
        if amount > inventory:
            api_key = settings.PAY_API_KEY
            redirect_url = 'http://localhost:8000/appointment-and-consultation/payment-callback-appointment/'
            url = "https://pay.ir/pg/send"

            data = {
                "api": api_key,
                "amount": amount - inventory,
                "redirect": redirect_url,
                "factorNumber": str(appointment.pk),
                "description": f"تراکنش {request.user.get_full_name()} برای نوبت {appointment.doctor.doctorprofile.get_expertise_display()} از دکتر {appointment.doctor.get_full_name()}",
            }

            response = requests.post(url, data=data)

            if response.status_code == 200:
                result = response.json()
                if result['status'] == 1:
                    token = result['token']
                    payment_url = f'https://pay.ir/pg/{token}'
                    return redirect(payment_url)
                else:
                    return render(request, 'appointment/take_appointment.html', {'appointment': appointment, 'error': 'خطا در اتصال به درگاه پرداخت'})
        else:
            appointment = Appointment.objects.get(pk=pk)
            appointment.patient = request.user
            appointment.status = 'رزرو شده'
            appointment.save()

            request.user.patientprofile.inventory = inventory - amount
            request.user.patientprofile.save()

            return redirect('patient_appointment_list')
    else:
        return render(request, 'appointment/take_appointment.html', {'appointment': appointment})

@login_required_decorator
def payment_callback_appointment(request):
    status = request.GET.get('status')
    token = request.GET.get('token')
    
    if status == '1':
        api_key = 'test'
        data = {
            'api': api_key,
            'token': token
        }
        
        response = requests.post('https://pay.ir/pg/verify', data=data)
        result = response.json()
        
        if result['status'] == 1:
            transaction = Transaction(
                status=result['status'],
                amount=result['amount'],
                transId=result['transId'],
                factorNumber=result['factorNumber'],
                mobile=request.user.phone_number,
                description=result['description'],
            )
            transaction.save()

            appointment = Appointment.objects.get(pk=int(result['factorNumber']))
            appointment.patient = request.user
            appointment.status = 'رزرو شده'
            appointment.save()

            request.user.patientprofile.inventory = 0
            request.user.patientprofile.save()

            return redirect('patient_appointment_list')
        else:
            return redirect('payment_error_page')
    
    return redirect('payment_error_page')

@login_required_decorator
def take_consultation(request, pk):
    consultation = get_object_or_404(Consultation, pk=pk)
    if request.method == 'POST' and consultation.status == 'آزاد' and request.user.user_type == 'بیمار' and request.user.patientprofile:
        inventory = request.user.patientprofile.inventory
        amount_model = Amount.objects.get(pk=1)
        amount = amount_model.amount
        if amount > inventory:
            api_key = settings.PAY_API_KEY
            redirect_url = 'http://localhost:8000/appointment-and-consultation/payment-callback-consultation/'
            url = "https://pay.ir/pg/send"

            data = {
                "api": api_key,
                "amount": amount - inventory,
                "redirect": redirect_url,
                "factorNumber": str(consultation.pk),
                "description": f"تراکنش {request.user.get_full_name()} برای مشاوره {consultation.doctor.doctorprofile.get_expertise_display()} از دکتر {consultation.doctor.get_full_name()}",
            }

            response = requests.post(url, data=data)

            if response.status_code == 200:
                result = response.json()
                if result['status'] == 1:
                    token = result['token']
                    payment_url = f'https://pay.ir/pg/{token}'
                    return redirect(payment_url)
                else:
                    return render(request, 'consultation/take_consultation.html', {'consultation': consultation, 'error': 'خطا در اتصال به درگاه پرداخت'})
        else:
            consultation = Consultation.objects.get(pk=pk)
            consultation.patient = request.user
            consultation.status = 'رزرو شده'
            consultation.save()

            request.user.patientprofile.inventory = inventory - amount
            request.user.patientprofile.save()
            return redirect('patient_consultation_list')
    else:
        return render(request, 'consultation/take_consultation.html', {'consultation': consultation})
    
@login_required_decorator
def payment_callback_consultation(request):
    status = request.GET.get('status')
    token = request.GET.get('token')
    
    if status == '1':
        api_key = 'test'
        data = {
            'api': api_key,
            'token': token
        }
        
        response = requests.post('https://pay.ir/pg/verify', data=data)
        result = response.json()
        
        if result['status'] == 1:
            transaction = Transaction(
                status=result['status'],
                amount=result['amount'],
                transId=result['transId'],
                factorNumber=result['factorNumber'],
                mobile=request.user.phone_number,
                description=result['description'],
            )
            transaction.save()

            consultation = Consultation.objects.get(pk=int(result['factorNumber']))
            consultation.patient = request.user
            consultation.status = 'رزرو شده'
            consultation.save()

            request.user.patientprofile.inventory = 0
            request.user.patientprofile.save()

            return redirect('patient_consultation_list')
        else:
            return redirect('payment_error_page')
    
    return redirect('payment_error_page')

def payment_error_page(request):
    return render(request, 'page/payment_error_page.html')

@login_required_decorator
def cancle_appointment(request, pk):
    appointment = Appointment.objects.get(pk=pk)
    amount = Amount.objects.get(pk=1)
    if appointment.patient == request.user and appointment.status == 'رزرو شده' and appointment.cancle:
        appointment.patient = None
        appointment.status = 'آزاد'
        appointment.save()
        request.user.patientprofile.inventory += amount.amount
        request.user.patientprofile.save()
        context = {
            'appointment': appointment
        }
        return render(request, 'account/cancle_appointment.html', context)
    else:
        return redirect('patient_appointment_list')

@login_required_decorator
def cancle_consultation(request, pk):
    consultation = Consultation.objects.get(pk=pk)
    amount = Amount.objects.get(pk=1)
    if consultation.patient == request.user and consultation.status == 'رزرو شده' and consultation.cancle:
        consultation.patient = None
        consultation.status = 'آزاد'
        consultation.save()
        request.user.patientprofile.inventory += amount.amount
        request.user.patientprofile.save()
        context = {
            'consultation': consultation
        }
        return render(request, 'account/cancle_consultation.html', context)
    else:
        return redirect('patient_consultation_list')
    