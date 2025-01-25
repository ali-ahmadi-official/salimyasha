from django.apps import AppConfig


class AppointmentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'appointment'
    verbose_name = 'نوبت و مشاوره'

    def ready(self):
        from .utils import start_delete_expired_appointments
        start_delete_expired_appointments()
