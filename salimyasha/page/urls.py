from django.urls import path
from .views import (
    home, ContactCreateView, ContactFaCreateView, services, about, DoctorListView, DoctorDetailView, AppointmentListView, ConsultationListView,
    comprehensive_rule, appointment_cancellation_rule, patient_rule, doctor_rule, question_answer
)

urlpatterns = [
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('services/', services, name='services'),
    path('contact/', ContactCreateView.as_view(), name='contact'),
    path('contact-fa/', ContactFaCreateView.as_view(), name='contact_fa'),
    path('doctors/', DoctorListView.as_view(), name='doctors'),
    path('doctors/<int:pk>/', DoctorDetailView.as_view(), name='doctor'),
    path('appointments/', AppointmentListView.as_view(), name='appointments'),
    path('consultations/', ConsultationListView.as_view(), name='consultations'),
    path('comprehensive-rule/', comprehensive_rule, name='comprehensive_rule'),
    path('appointment-cancellation-rule/', appointment_cancellation_rule, name='appointment_cancellation_rule'),
    path('patient-rule/', patient_rule, name='patient_rule'),
    path('doctor-rule/', doctor_rule, name='doctor_rule'),
    path('FAQ/', question_answer, name='FAQ'),
]