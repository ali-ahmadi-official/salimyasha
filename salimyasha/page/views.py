from datetime import datetime, timedelta
from django.db.models import Q, Avg
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from CMS.models import (
    About, DemonstrationComment, ComprehensiveRule, AppointmentCancellationRule,
    DoctorRule, PatientRule, QuestionAnswer
)
from account.models import CustomUser
from account.cities import CITY_CHOICES
from account.expertise import EXPERTISE_CHOICES
from account.jalali import Gregorian
from appointment.models import Appointment, Consultation, AppointmentComment, ConsultationComment
from .models import Contact
from .mixins import DoctorRequiredMixin

def home(request):
    about_view = About.objects.get(id=1)
    demonstration_comments = DemonstrationComment.objects.all()
    some_doctors = CustomUser.objects.filter(user_type = 'دکتر', doctorprofile__account_verification=True)[:5]
    cities = dict(CITY_CHOICES)
    expertise_choices = dict(EXPERTISE_CHOICES)
    context = {
        'about_view': about_view,
        'demonstration_comments' : demonstration_comments,
        'some_doctors': some_doctors,
        'cities': cities,
        'expertise_choices': expertise_choices,
    }
    return render(request, 'page/home.html', context)

class ContactCreateView(CreateView):
    model = Contact
    template_name = 'page/cont.html'
    fields = ['name', 'email', 'subject', 'message']
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.date = timezone.now()

        return super().form_valid(form)

class ContactFaCreateView(CreateView):
    model = Contact
    template_name = 'page/cont_fa.html'
    fields = ['name', 'email', 'subject', 'message']
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.date = timezone.now()

        return super().form_valid(form)

def services(request):
    return render(request, 'page/services.html')

def about(request):
    about_view = About.objects.get(id=1)
    context = {
        'about_view': about_view,
    }
    return render(request, 'page/about.html', context)

class DoctorListView(ListView):
    model = CustomUser
    template_name = 'page/doctors.html'
    context_object_name = 'doctors'
    paginate_by = 15

    def get_queryset(self):
        queryset = super().get_queryset().filter(user_type='دکتر', doctorprofile__account_verification=True)
        search_query = self.request.GET.get('q')
        city = self.request.GET.get('city')
        specialty = self.request.GET.get('specialty')

        if search_query:
            queryset = queryset.filter(
                Q(first_name__icontains=search_query) | 
                Q(last_name__icontains=search_query)
            )
        if city:
            queryset = queryset.filter(doctorprofile__city=city)
        if specialty:
            queryset = queryset.filter(doctorprofile__expertise=specialty)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cities'] = dict(CITY_CHOICES)
        context['expertise_choices'] = dict(EXPERTISE_CHOICES)
    
        return context

class DoctorDetailView(DoctorRequiredMixin, DetailView):
    model = CustomUser
    template_name = 'page/doctor.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        today = datetime.now()
        dates = [(today + timedelta(days=i)) for i in range(7)]
        persian_dates = [Gregorian(d.year, d.month, d.day).persian_string('{0:04d}/{1:02d}/{2:02d}') for d in dates]

        context['today'] = Appointment.objects.filter(doctor=self.object, status='آزاد', date=persian_dates[0])
        context['tomorrow'] = Appointment.objects.filter(doctor=self.object, status='آزاد', date=persian_dates[1])
        context['tomorrow2'] = Appointment.objects.filter(doctor=self.object, status='آزاد', date=persian_dates[2])
        context['tomorrow3'] = Appointment.objects.filter(doctor=self.object, status='آزاد', date=persian_dates[3])
        context['tomorrow4'] = Appointment.objects.filter(doctor=self.object, status='آزاد', date=persian_dates[4])
        context['tomorrow5'] = Appointment.objects.filter(doctor=self.object, status='آزاد', date=persian_dates[5])
        context['tomorrow6'] = Appointment.objects.filter(doctor=self.object, status='آزاد', date=persian_dates[6])

        context['ctoday'] = Consultation.objects.filter(doctor=self.object, status='آزاد', date=persian_dates[0])
        context['ctomorrow'] = Consultation.objects.filter(doctor=self.object, status='آزاد', date=persian_dates[1])
        context['ctomorrow2'] = Consultation.objects.filter(doctor=self.object, status='آزاد', date=persian_dates[2])
        context['ctomorrow3'] = Consultation.objects.filter(doctor=self.object, status='آزاد', date=persian_dates[3])
        context['ctomorrow4'] = Consultation.objects.filter(doctor=self.object, status='آزاد', date=persian_dates[4])
        context['ctomorrow5'] = Consultation.objects.filter(doctor=self.object, status='آزاد', date=persian_dates[5])
        context['ctomorrow6'] = Consultation.objects.filter(doctor=self.object, status='آزاد', date=persian_dates[6])

        similar_doctors_by_expertise = CustomUser.objects.filter(doctorprofile__expertise=self.object.doctorprofile.expertise, doctorprofile__account_verification=True).exclude(id=self.object.id)[:5]
        context['similar_doctors_by_expertise'] = similar_doctors_by_expertise

        similar_doctors_by_city = CustomUser.objects.filter(doctorprofile__city=self.object.doctorprofile.city, doctorprofile__account_verification=True).exclude(id=self.object.id)[:5]
        context['similar_doctors_by_city'] = similar_doctors_by_city

        appointment_comments = AppointmentComment.objects.filter(appointment__doctor=self.object)
        appointment_comments_num = appointment_comments.count()
        context['appointment_comments'] = appointment_comments
        consultation_comments = ConsultationComment.objects.filter(consultation__doctor=self.object)
        consultation_comments_num = consultation_comments.count()
        context['consultation_comments'] = consultation_comments

        context['comments_num'] = appointment_comments_num + consultation_comments_num

        comment_list = []

        for appointment_comment in appointment_comments:
            star = appointment_comment.star
            comment_list.append(star)
        
        for consultation_comment in consultation_comments:
            star = consultation_comment.star
            comment_list.append(star)
        
        if comment_list:
            numbers = [int(x) for x in comment_list]
            average = round((sum(numbers) / len(numbers)), 1)
            context['average'] = average
        else:
            context['average'] = 0

        return context

class AppointmentListView(LoginRequiredMixin, ListView):
    model = Appointment
    template_name = 'page/appointment.html'
    context_object_name = 'appointments'
    login_url = 'patient_login'
    paginate_by = 15

    def get_queryset(self):
        queryset = super().get_queryset().filter(status='آزاد').order_by('date')
        search_query = self.request.GET.get('q')
        city = self.request.GET.get('city')
        specialty = self.request.GET.get('specialty')
        date = self.request.GET.get('date')

        if search_query:
            queryset = queryset.filter(
                Q(doctor__first_name__icontains=search_query) | 
                Q(doctor__last_name__icontains=search_query)
            )
        if city:
            queryset = queryset.filter(doctor__doctorprofile__city=city)
        if specialty:
            queryset = queryset.filter(doctor__doctorprofile__expertise=specialty)
        if date:
            queryset = queryset.filter(date=date)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cities'] = dict(CITY_CHOICES)
        context['expertise_choices'] = dict(EXPERTISE_CHOICES)
        return context

class ConsultationListView(LoginRequiredMixin, ListView):
    model = Consultation
    template_name = 'page/consultation.html'
    context_object_name = 'consultations'
    login_url = 'patient_login'
    paginate_by = 15

    def get_queryset(self):
        queryset = super().get_queryset().filter(status='آزاد').order_by('date')
        search_query = self.request.GET.get('q')
        specialty = self.request.GET.get('specialty')
        date = self.request.GET.get('date')

        if search_query:
            queryset = queryset.filter(
                Q(doctor__first_name__icontains=search_query) | 
                Q(doctor__last_name__icontains=search_query)
            )
        if specialty:
            queryset = queryset.filter(doctor__doctorprofile__expertise=specialty)
        if date:
            queryset = queryset.filter(date=date)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['expertise_choices'] = dict(EXPERTISE_CHOICES)
        return context

def comprehensive_rule(request):
    comprehensive_rule_view = ComprehensiveRule.objects.all()
    context = {
        'comprehensive_rules': comprehensive_rule_view,
    }
    return render(request, 'page/comprehensive_rule.html', context)

def appointment_cancellation_rule(request):
    appointment_cancellation_rule_view = AppointmentCancellationRule.objects.all()
    context = {
        'appointment_cancellation_rules': appointment_cancellation_rule_view,
    }
    return render(request, 'page/appointment_cancellation_rule.html', context)

def patient_rule(request):
    patient_rule_view = PatientRule.objects.all()
    context = {
        'patient_rules': patient_rule_view,
    }
    return render(request, 'page/patient_rule.html', context)

def doctor_rule(request):
    doctor_rule_view = DoctorRule.objects.all()
    context = {
        'doctor_rules': doctor_rule_view,
    }
    return render(request, 'page/doctor_rule.html', context)

def question_answer(request):
    question_answer_patient = QuestionAnswer.objects.filter(audience='بیمار')
    question_answer_doctor = QuestionAnswer.objects.filter(audience='دکتر')
    context = {
        'question_answer_patients': question_answer_patient,
        'question_answer_doctors': question_answer_doctor,
    }
    return render(request, 'page/question_answer.html', context)