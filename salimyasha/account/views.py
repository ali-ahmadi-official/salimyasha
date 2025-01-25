import requests
from datetime import datetime
from django.utils import timezone
from django.utils.timezone import make_aware
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from appointment.models import Appointment, Consultation, Message
from .jalali import Persian
from .models import CustomUser, DoctorProfile, PatientProfile, Clinic, Ticket
from .forms import (
    PasswordResetForm, CustomPasswordChangeForm,
    PatientSignupForm, PatientLoginForm,
    DoctorSignupForm, DoctorLoginForm,
    DoctorProfileForm, DoctorProfileCreateForm,
    PatientProfileForm, PatientProfileCreateForm,
    DoctorBioForm, CliniceForm,
    AppointmentCommentForm, ConsultationCommentForm,
    TicketForm, ChatForm
)
from .mixins import NotAdminMixin, DoctorRequiredMixin, AccountTrueRequiredMixin, FreeRequiredMixin, SelfProfileMixin, SelfUserMixin, SelfClinicMixin

def password_reset_request(request):
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        
        if form.is_valid():
            username = form.cleaned_data['username']
            national_id = form.cleaned_data['national_id']
            
            existing_usernames = CustomUser.objects.values_list('username', flat=True)

            if username not in existing_usernames:
                form.add_error(None, "پزشکی با این مشخصات برای بازیابی رمز عبور یافت نشد")
            else:
                user = CustomUser.objects.get(username=username)
                
                if user.doctorprofile.national_id == national_id or user.patientprofile.national_id == national_id:
                    return redirect('password_change', user_id=user.id)
                else:
                    form.add_error(None, 'کد ملی برای این پزشک نادرست است')
    else:
        form = PasswordResetForm()
        
    return render(request, 'registration/password_reset.html', {'form': form})

def password_change(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if request.method == "POST":
        form = CustomPasswordChangeForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password1']
            user.set_password(new_password)
            user.save()
            return redirect('password_change_done')
    else:
        form = CustomPasswordChangeForm()
    return render(request, 'registration/password_change.html', {'form': form, 'user': user})

def password_change_done(request):
    return render(request, 'registration/password_change_done.html')

def patient_signup_view(request):
    if request.method == 'POST':
        form = PatientSignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.user_type = 'بیمار'
            user.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = PatientSignupForm()
    return render(request, 'registration/patient_signup.html', {'form': form})

def doctor_signup_view(request):
    if request.method == 'POST':
        form = DoctorSignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.user_type = 'دکتر'
            user.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = DoctorSignupForm()
    return render(request, 'registration/doctor_signup.html', {'form': form})

def patient_login_view(request):
    form = PatientLoginForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None and user.user_type == 'بیمار':
                login(request, user)
                return redirect('dashboard')
            else:
                form.add_error(None, 'نام کاربری یا رمز عبور برای این بیمار نادرست است')
    return render(request, 'registration/patient_login.html', {'form': form})

def doctor_login_view(request):
    form = DoctorLoginForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None and user.user_type == 'دکتر':
                login(request, user)
                return redirect('dashboard')
            else:
                form.add_error(None, 'نام کاربری یا رمز عبور برای این دکتر نادرست است')
    return render(request, 'registration/doctor_login.html', {'form': form})

class UserDashboardView(LoginRequiredMixin, NotAdminMixin, TemplateView):
    template_name = 'account/dashboard.html'

    def get_login_url(self):
        return reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        patient_appointments = Appointment.objects.filter(patient=self.request.user).order_by('-id')[:3]
        patient_consultations = Consultation.objects.filter(patient=self.request.user).order_by('-id')[:3]
        doctor_appointments = Appointment.objects.filter(doctor=self.request.user).order_by('-id')[:3]
        doctor_consultations = Consultation.objects.filter(doctor=self.request.user).order_by('-id')[:3]

        context['user'] = self.request.user
        context['patient_appointments'] = patient_appointments
        context['patient_consultations'] = patient_consultations
        context['doctor_appointments'] = doctor_appointments
        context['doctor_consultations'] = doctor_consultations
        return context

class DoctorProfileDetailView(LoginRequiredMixin, NotAdminMixin, SelfProfileMixin, DetailView):
    model = DoctorProfile
    template_name = 'account/doctor_profile_detail.html'

    def get_login_url(self):
        return reverse_lazy('doctor_login')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = CustomUser.objects.get(id=self.request.user.id)
        return context

class DoctorProfileCreateView(LoginRequiredMixin, CreateView):
    model = DoctorProfile
    template_name = 'account/doctor_create_profile.html'
    form_class = DoctorProfileCreateForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = DoctorProfile(user=self.request.user)
        return kwargs

    def get_success_url(self):
        return reverse_lazy('doctor_profile', args=[self.request.user.doctorprofile.id])

    def form_valid(self, form):
        national_code = form.cleaned_data.get('national_id')
        response = requests.post(f'https://api.codebazan.ir/codemelli/?code={national_code}')

        if response.status_code == 200 and response.json().get('Ok'):
            self.object = form.save(commit=False)
            self.object.user = self.request.user
            self.object.user.phone_number_verification = True
            self.object.save()
            return super().form_valid(form)
        else:
            form.add_error('national_id', 'کد ملی نامعتبر است. لطفا دوباره تلاش کنید.')
            return self.form_invalid(form)

    def get_login_url(self):
        return reverse_lazy('doctor_login')

class EditProfileView(LoginRequiredMixin, NotAdminMixin, SelfProfileMixin, View):
    template_name = 'account/edit_profile.html'
    form_class = DoctorProfileForm

    def get_login_url(self):
        return reverse_lazy('doctor_login')

    def get_object(self):
        return get_object_or_404(DoctorProfile, user=self.request.user)

    def get(self, request, *args, **kwargs):
        user_profile = self.get_object()
        form = self.form_class(instance=user_profile)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        user_profile = self.get_object()
        form = self.form_class(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            if 'profile_image' not in request.FILES:
                request.user.profile_image = request.user.profile_image
            form.save()
            return redirect(reverse_lazy('doctor_profile', args=[self.request.user.doctorprofile.id]))
        return render(request, self.template_name, {'form': form})

class DoctorEditBio(LoginRequiredMixin, NotAdminMixin, SelfProfileMixin, UpdateView):
    model = DoctorProfile
    form_class = DoctorBioForm
    template_name = 'account/edit_bio.html'

    def get_success_url(self):
        return reverse_lazy('doctor_profile', args=[self.object.id])
    
    def get_login_url(self):
        return reverse_lazy('doctor_login')

class UserUpdateView(LoginRequiredMixin, NotAdminMixin, SelfUserMixin, UpdateView):
    model = CustomUser
    template_name = 'account/edit_user.html'
    fields = ['username', 'phone_number', 'email']
    
    def get_object(self):
        return get_object_or_404(CustomUser, id=self.kwargs['pk'])

    def get_success_url(self):
        return reverse_lazy(
            'doctor_profile' if self.object.user_type == 'دکتر' else 'patient_profile',
            args=[self.object.doctorprofile.id if self.object.user_type == 'دکتر' else self.object.patientprofile.id]
        )

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        if self.request.user.phone_number_verification:
            form.fields.pop('phone_number')
        return form

    def get_login_url(self):
        return reverse_lazy('doctor_login' if self.object.user_type == 'دکتر' else 'patient_login')

class DoctorAppointmentListView(LoginRequiredMixin, NotAdminMixin, ListView):
    model = Appointment
    template_name = 'account/doctor_appointment_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        status = self.request.GET.get('status')

        queryset = Appointment.objects.filter(doctor=self.request.user)

        if status:
            queryset = queryset.filter(status=status)

        context['doctor_appointments'] = queryset.order_by('-id')
        return context

    def get_login_url(self):
        return reverse_lazy('doctor_login')

class AddAppointmentCreateView(LoginRequiredMixin, NotAdminMixin, AccountTrueRequiredMixin, CreateView):
    model = Appointment
    template_name = 'account/add_appointment.html'
    fields = ['date', 'start_time']
    success_url = reverse_lazy('doctor_appointment_list')

    def get_login_url(self):
        return reverse_lazy('doctor_login')

    def form_valid(self, form):
        geo_date = Persian(form.cleaned_data['date']).gregorian_datetime()
        start_datetime = datetime.combine(geo_date, form.cleaned_data['start_time'])
        start_datetime = make_aware(start_datetime)

        appointments = Appointment.objects.filter(doctor=self.request.user, status='آزاد')
        date = form.cleaned_data['date']
        time = form.cleaned_data['start_time']

        for appointment in appointments:
            if appointment.date == date and appointment.start_time == time:
                form.add_error(None, 'نوبت با این مشخصات زمانی از قبل وجود دارد.')
                return self.form_invalid(form)

        if start_datetime < timezone.now():
            form.add_error(None, 'تاریخ و ساعت نمی‌تواند گذشته باشد.')
            return self.form_invalid(form)

        form.instance.doctor = self.request.user
        form.instance.method = '2'

        return super().form_valid(form)

class AppointmentUpdateView(LoginRequiredMixin, NotAdminMixin, DoctorRequiredMixin, FreeRequiredMixin, UpdateView):
    model = Appointment
    template_name = 'account/edit_appointment.html'
    fields = ['date', 'start_time']
    success_url = reverse_lazy('doctor_appointment_list')

    def get_login_url(self):
        return reverse_lazy('doctor_login')
    
    def form_valid(self, form):
        geo_date = Persian(form.cleaned_data['date']).gregorian_datetime()
        start_datetime = datetime.combine(geo_date, form.cleaned_data['start_time'])
        start_datetime = make_aware(start_datetime)

        appointments = Appointment.objects.filter(doctor=self.request.user, status='آزاد')
        date = form.cleaned_data['date']
        time = form.cleaned_data['start_time']

        for appointment in appointments:
            if appointment.date == date and appointment.start_time == time:
                form.add_error(None, 'نوبت با این مشخصات زمانی از قبل وجود دارد.')
                return self.form_invalid(form)

        if start_datetime < timezone.now():
            form.add_error(None, 'تاریخ و ساعت نمی‌تواند گذشته باشد.')
            return self.form_invalid(form)

        return super().form_valid(form)

class AppointmentDeleteView(LoginRequiredMixin, NotAdminMixin, DoctorRequiredMixin, FreeRequiredMixin, DeleteView):
    model = Appointment
    template_name = 'account/delete_appointment.html'
    success_url = reverse_lazy('doctor_appointment_list')

    def get_login_url(self):
        return reverse_lazy('doctor_login')

class DoctorConsultationListView(LoginRequiredMixin, NotAdminMixin, ListView):
    model = Consultation
    template_name = 'account/doctor_consultation_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        status = self.request.GET.get('status')

        queryset = Consultation.objects.filter(doctor=self.request.user)

        if status:
            queryset = queryset.filter(status=status)

        context['doctor_consultations'] = queryset.order_by('-id')
        return context

    def get_login_url(self):
        return reverse_lazy('doctor_login')
    
class ConsultationCreateView(LoginRequiredMixin, NotAdminMixin, AccountTrueRequiredMixin, CreateView):
    model = Consultation
    template_name = 'account/add_consultation.html'
    fields = ['date', 'start_time', 'end_time']
    success_url = reverse_lazy('doctor_consultation_list')

    def get_login_url(self):
        return reverse_lazy('doctor_login')

    def form_valid(self, form):
        geo_date = Persian(form.cleaned_data['date']).gregorian_datetime()
        start_datetime = datetime.combine(geo_date, form.cleaned_data['start_time'])
        start_datetime = make_aware(start_datetime)

        consultations = Consultation.objects.filter(doctor=self.request.user, status='آزاد')
        date = form.cleaned_data['date']
        time = form.cleaned_data['start_time']
        end = form.cleaned_data['end_time']

        for consultation in consultations:
            if consultation.date == date and consultation.start_time == time:
                form.add_error(None, 'مشاوره با این مشخصات زمانی از قبل وجود دارد.')
                return self.form_invalid(form)

        if start_datetime < timezone.now():
            form.add_error(None, 'تاریخ و ساعت نمی‌تواند گذشته باشد.')
            return self.form_invalid(form)
        
        if time >= end:
            form.add_error(None, 'ساعت پایان نمی‌تواند از ساعت شروع قدیمی تر باشد')
            return self.form_invalid(form)

        form.instance.doctor = self.request.user
        form.instance.method = '2'

        return super().form_valid(form)

class ConsultationUpdateView(LoginRequiredMixin, NotAdminMixin, DoctorRequiredMixin, FreeRequiredMixin, UpdateView):
    model = Consultation
    template_name = 'account/edit_consultation.html'
    fields = ['date', 'start_time', 'end_time']
    success_url = reverse_lazy('doctor_consultation_list')

    def get_login_url(self):
        return reverse_lazy('doctor_login')
    
    def form_valid(self, form):
        geo_date = Persian(form.cleaned_data['date']).gregorian_datetime()
        start_datetime = datetime.combine(geo_date, form.cleaned_data['start_time'])
        start_datetime = make_aware(start_datetime)

        consultations = Consultation.objects.filter(doctor=self.request.user, status='آزاد')
        date = form.cleaned_data['date']
        time = form.cleaned_data['start_time']
        end = form.cleaned_data['end_time']

        for consultation in consultations:
            if consultation.date == date and consultation.start_time == time:
                form.add_error(None, 'مشاوره با این مشخصات زمانی از قبل وجود دارد.')
                return self.form_invalid(form)

        if start_datetime < timezone.now():
            form.add_error(None, 'تاریخ و ساعت نمی‌تواند گذشته باشد.')
            return self.form_invalid(form)
        
        if time >= end:
            form.add_error(None, 'ساعت پایان نمی‌تواند از ساعت شروع قدیمی تر باشد')
            return self.form_invalid(form)

        return super().form_valid(form)
    
class ConsultationDeleteView(LoginRequiredMixin, NotAdminMixin, DoctorRequiredMixin, FreeRequiredMixin, DeleteView):
    model = Consultation
    template_name = 'account/delete_consultation.html'
    success_url = reverse_lazy('doctor_consultation_list')

    def get_login_url(self):
        return reverse_lazy('doctor_login')

class ClinicCreateView(LoginRequiredMixin, NotAdminMixin, CreateView):
    model = Clinic
    form_class = CliniceForm
    template_name = 'account/add_clinic.html'

    def get_login_url(self):
        return reverse_lazy('doctor_login')
    
    def get_success_url(self):
        return reverse_lazy('doctor_profile', args=[self.request.user.doctorprofile.id])
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.doctor = self.request.user
        self.object.save()
        return super().form_valid(form)

class ClinicUpdateView(LoginRequiredMixin, NotAdminMixin, SelfClinicMixin, UpdateView):
    model = Clinic
    form_class = CliniceForm
    template_name = 'account/edit_clinic.html'

    def get_login_url(self):
        return reverse_lazy('doctor_login')
    
    def get_success_url(self):
        return reverse_lazy('doctor_profile', args=[self.request.user.doctorprofile.id])
    
class PatientProfileDetailView(LoginRequiredMixin, NotAdminMixin, SelfProfileMixin, DetailView):
    model = PatientProfile
    template_name = 'account/patient_profile_detail.html'

    def get_login_url(self):
        return reverse_lazy('patient_login')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = CustomUser.objects.get(id=self.request.user.id)
        return context
    
class PatientProfileCreateView(LoginRequiredMixin, CreateView):
    model = PatientProfile
    template_name = 'account/patient_create_profile.html'
    form_class = PatientProfileCreateForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = PatientProfile(user=self.request.user)
        return kwargs

    def get_success_url(self):
        return reverse_lazy('patient_profile', args=[self.request.user.patientprofile.id])

    def form_valid(self, form):
        national_code = form.cleaned_data.get('national_id')
        response = requests.post(f'https://api.codebazan.ir/codemelli/?code={national_code}')

        if response.status_code == 200 and response.json().get('Ok'):
            self.object = form.save(commit=False)
            self.object.user = self.request.user
            self.object.user.phone_number_verification = True
            self.object.save()
            return super().form_valid(form)
        else:
            form.add_error('national_id', 'کد ملی نامعتبر است. لطفا دوباره تلاش کنید.')
            return self.form_invalid(form)

    def get_login_url(self):
        return reverse_lazy('patient_login')

class EditProfileView2(LoginRequiredMixin, NotAdminMixin, SelfProfileMixin, View):
    template_name = 'account/edit_profile2.html'
    form_class = PatientProfileForm

    def get_login_url(self):
        return reverse_lazy('patient_login')

    def get_object(self):
        return get_object_or_404(PatientProfile, user=self.request.user)

    def get(self, request, *args, **kwargs):
        user_profile = self.get_object()
        form = self.form_class(instance=user_profile)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        user_profile = self.get_object()
        form = self.form_class(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            if 'profile_image' not in request.FILES:
                request.user.profile_image = request.user.profile_image
            form.save()
            return redirect(reverse_lazy('patient_profile', args=[self.request.user.patientprofile.id]))
        return render(request, self.template_name, {'form': form})

class PatientAppointmentListView(LoginRequiredMixin, NotAdminMixin, ListView):
    model = Appointment
    template_name = 'account/patient_appointment_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        queryset = Appointment.objects.filter(patient=self.request.user)

        context['patient_appointments'] = queryset.order_by('-id')
        return context

    def get_login_url(self):
        return reverse_lazy('patient_login')

class PatientConsultationListView(LoginRequiredMixin, NotAdminMixin, ListView):
    model = Consultation
    template_name = 'account/patient_consultation_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        queryset = Consultation.objects.filter(patient=self.request.user)

        context['patient_consultations'] = queryset.order_by('-id')

        for patient_consultation in queryset:
            geo_date = Persian(patient_consultation.date).gregorian_datetime()
            start_datetime = datetime.combine(geo_date, patient_consultation.start_time)
            start_datetime = make_aware(start_datetime)
            end_datetime = datetime.combine(geo_date, patient_consultation.end_time)
            end_datetime = make_aware(end_datetime)

        return context

    def get_login_url(self):
        return reverse_lazy('patient_login')
    
def add_appointmen_comment(request, pk):
    if request.method == 'POST':
        appointment = Appointment.objects.get(pk=pk)
        form = AppointmentCommentForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.appointment = appointment
            instance.save()
            return redirect('patient_appointment_list')
    else:
        appointment = Appointment.objects.get(pk=pk)
        form = AppointmentCommentForm()
    context = {
        'form': form,
        'appointment': appointment,
    }
    return render(request, 'account/appointment_comment_form.html', context)

def add_consultation_comment(request, pk):
    if request.method == 'POST':
        consultation = Consultation.objects.get(pk=pk)
        form = ConsultationCommentForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.consultation = consultation
            instance.save()
            return redirect('patient_consultation_list')
    else:
        consultation = Consultation.objects.get(pk=pk)
        form = ConsultationCommentForm()
    context = {
        'form': form,
        'consultation': consultation,
    }
    return render(request, 'account/consultation_comment_form.html', context)

@login_required
def ticket_list_create(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            return redirect('ticket_list_create')
    else:
        form = TicketForm()
    
    tickets = Ticket.objects.filter(user=request.user)
    return render(request, 'account/ticket_list_create.html', {'form': form, 'tickets': tickets})

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def chat(request, pk):
    consultation = Consultation.objects.get(pk=pk)

    if consultation.doctor == request.user or consultation.patient == request.user:
        messages = Message.objects.filter(consultation=consultation)
        geo_date = Persian(consultation.date).gregorian_datetime()
        start_datetime = datetime.combine(geo_date, consultation.start_time)
        start_datetime = make_aware(start_datetime)
        end_datetime = datetime.combine(geo_date, consultation.end_time)
        end_datetime = make_aware(end_datetime)

        if request.method == 'POST':
            form = ChatForm(request.POST, request.FILES)
            if form.is_valid():
                form.instance.consultation = consultation
                form.instance.author = request.user
                form.save()
                return redirect('chat', pk)
        else:
            form = ChatForm()

        if start_datetime <= timezone.now() and timezone.now() <= end_datetime:
            context = {
                'messages': messages,
                'form': form,
                'allowed': True
            }
        else:
            context = {
                'messages': messages,
                'form': form,
                'allowed': False
            }

        return render(request, 'account/chat.html', context=context)
    else:
        return redirect('dashboard')
    
def update_chat(request, pk):
    consultation = Consultation.objects.get(pk=pk)
    messages = Message.objects.filter(consultation=consultation)

    context = {
        'messages': messages,
    }

    return render(request, 'account/update_chat.html', context=context)
