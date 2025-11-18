from django.contrib import admin
from .models import DoctorAvailability, Appointment, AppointmentReminder


@admin.register(DoctorAvailability)
class DoctorAvailabilityAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'get_day_display', 'start_time', 'end_time', 'is_active')
    list_filter = ('day_of_week', 'is_active', 'doctor__userprofile__specialization')
    search_fields = ('doctor__first_name', 'doctor__last_name', 'doctor__userprofile__specialization')
    ordering = ('doctor', 'day_of_week', 'start_time')
    
    def get_day_display(self, obj):
        return obj.get_day_of_week_display()
    get_day_display.short_description = 'Day'


class AppointmentReminderInline(admin.TabularInline):
    model = AppointmentReminder
    extra = 1


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'date', 'time', 'appointment_type', 'status', 'created_at')
    list_filter = ('status', 'appointment_type', 'date', 'doctor__userprofile__specialization')
    search_fields = ('patient__first_name', 'patient__last_name', 'doctor__first_name', 'doctor__last_name', 'reason')
    date_hierarchy = 'date'
    ordering = ('-date', '-time')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [AppointmentReminderInline]
    
    fieldsets = (
        ('Appointment Details', {
            'fields': ('patient', 'doctor', 'date', 'time', 'appointment_type', 'duration_minutes')
        }),
        ('Status & Information', {
            'fields': ('status', 'reason', 'notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(AppointmentReminder)
class AppointmentReminderAdmin(admin.ModelAdmin):
    list_display = ('appointment', 'reminder_type', 'hours_before', 'is_sent', 'sent_at')
    list_filter = ('reminder_type', 'is_sent', 'hours_before')
    search_fields = ('appointment__patient__first_name', 'appointment__patient__last_name')
    readonly_fields = ('sent_at',)
