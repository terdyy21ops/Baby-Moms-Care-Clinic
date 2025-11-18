from django.contrib import admin
from .models import PregnancyLog, PregnancyWeeklyLog, PregnancyMilestone, PregnancyReminder, PregnancyTip


class PregnancyWeeklyLogInline(admin.TabularInline):
    model = PregnancyWeeklyLog
    extra = 0
    readonly_fields = ('created_at', 'updated_at')


class PregnancyMilestoneInline(admin.TabularInline):
    model = PregnancyMilestone
    extra = 0
    readonly_fields = ('created_at',)


@admin.register(PregnancyLog)
class PregnancyLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'start_date', 'due_date', 'current_week', 'trimester', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at', 'due_date')
    search_fields = ('user__first_name', 'user__last_name', 'user__email')
    readonly_fields = ('created_at', 'updated_at', 'current_week', 'trimester', 'progress_percentage')
    inlines = [PregnancyWeeklyLogInline, PregnancyMilestoneInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'start_date', 'due_date', 'is_active')
        }),
        ('Progress', {
            'fields': ('current_week', 'trimester', 'progress_percentage'),
            'classes': ('collapse',)
        }),
        ('Notes', {
            'fields': ('notes',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(PregnancyWeeklyLog)
class PregnancyWeeklyLogAdmin(admin.ModelAdmin):
    list_display = ('pregnancy', 'week_number', 'weight', 'energy_level', 'created_at')
    list_filter = ('week_number', 'energy_level', 'created_at')
    search_fields = ('pregnancy__user__first_name', 'pregnancy__user__last_name', 'symptoms', 'mood')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(PregnancyMilestone)
class PregnancyMilestoneAdmin(admin.ModelAdmin):
    list_display = ('title', 'pregnancy', 'milestone_type', 'date', 'week_number', 'is_important')
    list_filter = ('milestone_type', 'is_important', 'date')
    search_fields = ('title', 'description', 'pregnancy__user__first_name', 'pregnancy__user__last_name')
    readonly_fields = ('created_at',)


@admin.register(PregnancyReminder)
class PregnancyReminderAdmin(admin.ModelAdmin):
    list_display = ('title', 'pregnancy', 'reminder_type', 'frequency', 'start_date', 'is_active')
    list_filter = ('reminder_type', 'frequency', 'is_active', 'start_date')
    search_fields = ('title', 'description', 'pregnancy__user__first_name', 'pregnancy__user__last_name')
    readonly_fields = ('created_at',)


@admin.register(PregnancyTip)
class PregnancyTipAdmin(admin.ModelAdmin):
    list_display = ('title', 'trimester', 'week_range_start', 'week_range_end', 'is_active')
    list_filter = ('trimester', 'is_active', 'created_at')
    search_fields = ('title', 'content')
    readonly_fields = ('created_at',)
