from django.contrib import admin
from appointment.models import TemplateAppointment
from .models import CustomUser, DoctorProfile, PatientProfile, Clinic, Ticket

class DoctorProfileInline(admin.StackedInline):
    model = DoctorProfile
    can_delete = False

class PatientProfileInline(admin.StackedInline):
    model = PatientProfile
    can_delete = False

class ClinicInline(admin.StackedInline):
    model = Clinic
    can_delete = False

class TemplateAppointmentInline(admin.StackedInline):
    model = TemplateAppointment
    extra = 0

class CustomUserAdmin(admin.ModelAdmin):
    inlines = (DoctorProfileInline, PatientProfileInline, ClinicInline, TemplateAppointmentInline)
    list_display = ["username", "user_type", "first_name", "last_name", "phone_number", "account_verification_display"]
    search_fields = ["first_name", "last_name"]
    list_filter = ["user_type"]

    def account_verification_display(self, obj):
        if hasattr(obj, 'doctorprofile'):
            return '✓' if obj.doctorprofile.account_verification else '✗'
        return 'تعریف نمی شود'

    account_verification_display.short_description = "تأیید حساب دکتر"

    def get_inline_instances(self, request, obj=None):
        inline_instances = []
        if obj is None:
            return inline_instances
        for inline_class in self.inlines:
            inline = inline_class(self.model, self.admin_site)
            if isinstance(inline, DoctorProfileInline) and obj.user_type != 'دکتر':
                continue
            if isinstance(inline, PatientProfileInline) and obj.user_type != 'بیمار':
                continue
            if isinstance(inline, TemplateAppointmentInline) and obj.user_type != 'دکتر':
                continue
            if isinstance(inline, ClinicInline) and obj.user_type != 'دکتر':
                continue
            inline_instances.append(inline)
        return inline_instances
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.exclude(id=1)

class TicketAdmin(admin.ModelAdmin):
    list_display = ['user', 'message', 'date']
    list_filter = ["user"]

    def has_add_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.unregister(CustomUser)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Ticket, TicketAdmin)