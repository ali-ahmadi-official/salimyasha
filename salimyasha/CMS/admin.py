from django.contrib import admin
from .models import (
    About, DemonstrationComment, ComprehensiveRule, AppointmentCancellationRule,
    DoctorRule, PatientRule,
    ParagraphAppointmentCancellationRule, ParagraphComprehensiveRule,
    ParagraphDoctorRule, ParagraphPatientRule, QuestionAnswer
)

class AboutAdmin(admin.ModelAdmin):
    def has_add_permission(self, request, obj=None):
        return False

class ParagraphComprehensiveRuleAdmin(admin.TabularInline):
    model = ParagraphComprehensiveRule
    extra = 0

class ParagraphAppointmentCancellationRuleAdmin(admin.TabularInline):
    model = ParagraphAppointmentCancellationRule
    extra = 0

class ParagraphDoctorRuleAdmin(admin.TabularInline):
    model = ParagraphDoctorRule
    extra = 0

class ParagraphPatientRuleAdmin(admin.TabularInline):
    model = ParagraphPatientRule
    extra = 0

class ComprehensiveRuleAdmin(admin.ModelAdmin):
    inlines = [ParagraphComprehensiveRuleAdmin]

class AppointmentCancellationRuleAdmin(admin.ModelAdmin):
    inlines = [ParagraphAppointmentCancellationRuleAdmin]

class DoctorRuleAdmin(admin.ModelAdmin):
    inlines = [ParagraphDoctorRuleAdmin]

class PatientRuleAdmin(admin.ModelAdmin):
    inlines = [ParagraphPatientRuleAdmin]

admin.site.register(About, AboutAdmin)
admin.site.register(DemonstrationComment)
admin.site.register(ComprehensiveRule, ComprehensiveRuleAdmin)
admin.site.register(AppointmentCancellationRule, AppointmentCancellationRuleAdmin)
admin.site.register(DoctorRule, DoctorRuleAdmin)
admin.site.register(PatientRule, PatientRuleAdmin)
admin.site.register(QuestionAnswer)