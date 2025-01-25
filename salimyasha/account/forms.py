from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator
from appointment.models import AppointmentComment, ConsultationComment, Message
from .models import CustomUser, DoctorProfile, PatientProfile, Clinic, Ticket
from .cities import CITY_CHOICES
from .expertise import EXPERTISE_CHOICES

class PasswordResetForm(forms.Form):
    username = forms.CharField(label='نام کاربری', max_length=100, widget=forms.TextInput(attrs={'class': 'input'}))
    national_id = forms.CharField(label='کد ملی', max_length=10, widget=forms.TextInput(attrs={'class': 'input'}))

class CustomPasswordChangeForm(forms.Form):
    new_password1 = forms.CharField(
        label='رمز جدید',
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'input'}),
    )
    new_password2 = forms.CharField(
        label='تایید رمز جدید',
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'input'}),
    )

    def save(self, user):
        if self.cleaned_data['new_password1']:
            user.set_password(self.cleaned_data['new_password1'])
            user.save()
        return user

class PatientSignupForm(UserCreationForm):
    username = forms.CharField(label='نام کاربری', max_length=100, widget=forms.TextInput(attrs={'class': 'input'}))
    email = forms.EmailField(label='ایمیل (اختیاری)', widget=forms.EmailInput(attrs={'class': 'input'}), required=False)
    password1 = forms.CharField(label='رمز عبور', widget=forms.PasswordInput(attrs={'class': 'input'}))
    password2 = forms.CharField(label='تکرار رمز عبور', widget=forms.PasswordInput(attrs={'class': 'input'}))
    phone_number = forms.CharField(label='شماره موبایل', max_length=10, validators=[RegexValidator(r'^\d{10}$', message='شماره موبایل باید 10 رقمی باشد')], widget=forms.NumberInput(attrs={'class': 'input', 'placeholder': 'به عنوان مثال : 9123456789'}), error_messages={'invalid': 'شماره موبایل باید 10 رقمی باشد'})

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'phone_number']

class DoctorSignupForm(UserCreationForm):
    username = forms.CharField(label='نام کاربری', max_length=100, widget=forms.TextInput(attrs={'class': 'input'}))
    email = forms.EmailField(label='ایمیل (اختیاری)', widget=forms.EmailInput(attrs={'class': 'input'}), required=False)
    password1 = forms.CharField(label='رمز عبور', widget=forms.PasswordInput(attrs={'class': 'input'}))
    password2 = forms.CharField(label='تکرار رمز عبور', widget=forms.PasswordInput(attrs={'class': 'input'}))
    phone_number = forms.CharField(label='شماره موبایل', max_length=10, validators=[RegexValidator(r'^\d{10}$', message='شماره موبایل باید 10 رقمی باشد')], widget=forms.NumberInput(attrs={'class': 'input', 'placeholder': 'به عنوان مثال : 9123456789'}), error_messages={'invalid': 'شماره موبایل باید 10 رقمی باشد'})

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'phone_number']

class PatientLoginForm(forms.Form):
    username = forms.CharField(label='نام کاربری', max_length=100, widget=forms.TextInput(attrs={'class': 'input'}))
    password = forms.CharField(label='رمز عبور', widget=forms.PasswordInput(attrs={'class': 'input'}))

class DoctorLoginForm(forms.Form):
    username = forms.CharField(label='نام کاربری', max_length=100, widget=forms.TextInput(attrs={'class': 'input'}))
    password = forms.CharField(label='رمز عبور', widget=forms.PasswordInput(attrs={'class': 'input'}))

class DoctorProfileForm(forms.ModelForm):
    profile_image = forms.ImageField(label='تصویر پروفایل', required=False)
    first_name = forms.CharField(label='نام', max_length=100, widget=forms.TextInput(attrs={'class': 'text'}))
    last_name = forms.CharField(label='نام خانوادگی', max_length=100, widget=forms.TextInput(attrs={'class': 'text'}))
    father_name = forms.CharField(label='نام پدر', max_length=100, widget=forms.TextInput(attrs={'class': 'text'}))
    medical_system_number = forms.CharField(label='شماره نظام پزشکی', max_length=10, widget=forms.TextInput(attrs={'class': 'text'}))
    city = forms.ChoiceField(label='شهر', choices=CITY_CHOICES, widget=forms.Select(attrs={'class': 'text'}))

    class Meta:
        model = DoctorProfile
        fields = ['profile_image', 'first_name', 'last_name', 'father_name', 'city', 'birth_date', 'medical_system_number']

    def __init__(self, *args, **kwargs):
        user = kwargs['instance'].user if 'instance' in kwargs else None
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        
        if user:
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name

    def save(self, commit=True):
        doctor_profile = super().save(commit=False)
        user = doctor_profile.user

        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        if self.cleaned_data['profile_image']:
            user.profile_image = self.cleaned_data['profile_image']
        
        if commit:
            user.save()
            doctor_profile.save()
        
        return doctor_profile

class DoctorProfileCreateForm(forms.ModelForm):
    profile_image = forms.ImageField(label='تصویر پروفایل', required=False)
    first_name = forms.CharField(label='نام', max_length=100, widget=forms.TextInput(attrs={'class': 'text'}))
    last_name = forms.CharField(label='نام خانوادگی', max_length=100, widget=forms.TextInput(attrs={'class': 'text'}))
    father_name = forms.CharField(label='نام پدر', max_length=100, widget=forms.TextInput(attrs={'class': 'text'}))
    national_id = forms.CharField(label='کد ملی', max_length=10, widget=forms.TextInput(attrs={'class': 'text'}))
    medical_system_number = forms.CharField(label='شماره نظام پزشکی', max_length=10, widget=forms.TextInput(attrs={'class': 'text'}))
    city = forms.ChoiceField(label='شهر', choices=CITY_CHOICES, widget=forms.Select(attrs={'class': 'text'}))

    class Meta:
        model = DoctorProfile
        fields = ['profile_image', 'first_name', 'last_name', 'father_name', 'city', 'birth_date', 'national_id', 'medical_system_number']

    def __init__(self, *args, **kwargs):
        user = kwargs['instance'].user if 'instance' in kwargs else None
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        
        if user:
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name

    def save(self, commit=True):
        doctor_profile = super().save(commit=False)
        user = doctor_profile.user

        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        if self.cleaned_data['profile_image']:
            user.profile_image = self.cleaned_data['profile_image']
        
        if commit:
            user.save()
            doctor_profile.save()
        
        return doctor_profile

class PatientProfileForm(forms.ModelForm):
    profile_image = forms.ImageField(label='تصویر پروفایل', required=False)
    first_name = forms.CharField(label='نام', max_length=100, widget=forms.TextInput(attrs={'class': 'text'}))
    last_name = forms.CharField(label='نام خانوادگی', max_length=100, widget=forms.TextInput(attrs={'class': 'text'}))

    class Meta:
        model = PatientProfile
        fields = ['profile_image', 'first_name', 'last_name', 'birth_date']

    def __init__(self, *args, **kwargs):
        user = kwargs['instance'].user if 'instance' in kwargs else None
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        
        if user:
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name

    def save(self, commit=True):
        doctor_profile = super().save(commit=False)
        user = doctor_profile.user

        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        if self.cleaned_data['profile_image']:
            user.profile_image = self.cleaned_data['profile_image']
        
        if commit:
            user.save()
            doctor_profile.save()
        
        return doctor_profile
    
class PatientProfileCreateForm(forms.ModelForm):
    profile_image = forms.ImageField(label='تصویر پروفایل', required=False)
    first_name = forms.CharField(label='نام', max_length=100, widget=forms.TextInput(attrs={'class': 'text'}))
    last_name = forms.CharField(label='نام خانوادگی', max_length=100, widget=forms.TextInput(attrs={'class': 'text'}))
    national_id = forms.CharField(label='کد ملی', max_length=10, widget=forms.TextInput(attrs={'class': 'text'}))

    class Meta:
        model = PatientProfile
        fields = ['profile_image', 'first_name', 'last_name', 'birth_date', 'national_id']

    def __init__(self, *args, **kwargs):
        user = kwargs['instance'].user if 'instance' in kwargs else None
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        
        if user:
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name

    def save(self, commit=True):
        patient_profile = super().save(commit=False)
        user = patient_profile.user

        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        if self.cleaned_data['profile_image']:
            user.profile_image = self.cleaned_data['profile_image']
        
        if commit:
            user.save()
            patient_profile.save()
        
        return patient_profile

class DoctorBioForm(forms.ModelForm):
    bio = forms.CharField(label='معرفی پزشک', max_length=3000, widget=forms.Textarea(attrs={'class': 'text'}))
    expertise = forms.ChoiceField(label='تخصص', choices=EXPERTISE_CHOICES, widget=forms.Select(attrs={'class': 'text'}))

    class Meta:
        model = DoctorProfile
        fields = ['bio', 'expertise']

class CliniceForm(forms.ModelForm):
    class Meta:
        model = Clinic
        fields = ['name', 'location', 'address']

class AppointmentCommentForm(forms.ModelForm):
    class Meta:
        model = AppointmentComment
        fields = ['content', 'star']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'text', 'rows': 4}),
        }

class ConsultationCommentForm(forms.ModelForm):
    class Meta:
        model = ConsultationComment
        fields = ['content', 'star']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'text', 'rows': 4}),
        }

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={'class': 'text', 'rows': 4}),
        }

class ChatForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['text', 'file']