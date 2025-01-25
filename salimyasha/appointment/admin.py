from django.contrib import admin
from .models import Amount, Transaction, Appointment, Consultation, Message, AppointmentComment, ConsultationComment

class AmountAdmin(admin.ModelAdmin):
    def has_add_permission(self, request, obj=None):
        return False

class TransactionAdmin(admin.ModelAdmin):
    list_display = ['transId', 'status', 'amount', 'factorNumber', 'mobile', 'description']

    def has_add_permission(self, request, obj=None):
        return False

class AppointmentCommentInline(admin.StackedInline):
    model = AppointmentComment
    extra = 0

class ConsultationCommentInline(admin.StackedInline):
    model = ConsultationComment
    extra = 0

class AppointmentAdmin(admin.ModelAdmin):
    inlines = (AppointmentCommentInline, )
    list_display = ["persian_id", "doctor", "patient", "date_and_time", "method", "status"]

    def persian_id(self, obj):
        return obj.id
    
    persian_id.short_description = "شماره نوبت"

    def date_and_time(self, obj):
        return f'{obj.date} , در ساعت {obj.start_time}'
    
    date_and_time.short_description = "تاریخ و زمان"

class MessageAdmin(admin.TabularInline):
    model = Message
    extra = 0

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False

class ConsultationAdmin(admin.ModelAdmin):
    inlines = [MessageAdmin, ConsultationCommentInline]
    list_display = ["persian_id", "doctor", "patient", "date_and_time", "status"]

    def persian_id(self, obj):
        return obj.id
    
    persian_id.short_description = "شماره مشاوره"

    def date_and_time(self, obj):
        return f'{obj.date} , از ساعت {obj.start_time} تا ساعت {obj.end_time}'
    
    date_and_time.short_description = "تاریخ و زمان"    

admin.site.register(Amount, AmountAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Consultation, ConsultationAdmin)
admin.site.register(Appointment, AppointmentAdmin)
