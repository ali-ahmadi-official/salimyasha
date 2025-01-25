from django.urls import path
from .views import (
    take_appointment, take_consultation, payment_callback_appointment, payment_callback_consultation, payment_error_page,
    cancle_appointment, cancle_consultation
)

urlpatterns = [
    path('take-appointment/<int:pk>/', take_appointment, name='take_appointment'),
    path('take-consultation/<int:pk>/', take_consultation, name='take_consultation'),
    path('payment-callback-appointment/', payment_callback_appointment, name='payment_callback_appointment'),
    path('payment-callback-consultation/', payment_callback_consultation, name='payment_callback_consultation'),
    path('payment-error-page', payment_error_page, name='payment_error_page'),
    path('cancle-appointment/<int:pk>/', cancle_appointment, name='cancle_appointment'),
    path('cancle-consultation/<int:pk>/', cancle_consultation, name='cancle_consultation'),
]