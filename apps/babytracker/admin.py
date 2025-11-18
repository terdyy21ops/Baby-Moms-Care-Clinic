from django.contrib import admin
from .models import (
    Baby, GrowthRecord, FeedingRecord, SleepRecord, 
    DiaperRecord, Vaccination, VaccinationRecord, 
    Milestone, BabyMilestoneRecord
)


class GrowthRecordInline(admin.TabularInline):
    model = GrowthRecord
    extra = 0
    readonly_fields = ('created_at', 'age_at_record')


class VaccinationRecordInline(admin.TabularInline):
    model = VaccinationRecord
    extra = 0
    readonly_fields = ('created_at',)


@admin.register(Baby)
class BabyAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'gender', 'birth_date', 'age_display', 'created_at')
    list_filter = ('gender', 'birth_date', 'created_at')
    search_fields = ('name', 'parent__first_name', 'parent__last_name', 'parent__email')
    readonly_fields = ('created_at', 'updated_at', 'age_in_days', 'age_in_weeks', 'age_in_months')
    inlines = [GrowthRecordInline, VaccinationRecordInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('parent', 'name', 'gender', 'birth_date')
        }),
        ('Birth Details', {
            'fields': ('birth_weight', 'birth_height', 'photo')
        }),
        ('Age Information', {
            'fields': ('age_in_days', 'age_in_weeks', 'age_in_months'),
            'classes': ('collapse',)
        }),
        ('Additional Information', {
            'fields': ('notes',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(GrowthRecord)
class GrowthRecordAdmin(admin.ModelAdmin):
    list_display = ('baby', 'date', 'weight', 'height', 'age_at_record', 'created_at')
    list_filter = ('date', 'created_at')
    search_fields = ('baby__name', 'baby__parent__first_name', 'baby__parent__last_name')
    readonly_fields = ('created_at', 'age_at_record')


@admin.register(FeedingRecord)
class FeedingRecordAdmin(admin.ModelAdmin):
    list_display = ('baby', 'date', 'time', 'feeding_type', 'duration_minutes', 'amount_ml')
    list_filter = ('feeding_type', 'date', 'created_at')
    search_fields = ('baby__name', 'baby__parent__first_name', 'baby__parent__last_name')
    readonly_fields = ('created_at',)


@admin.register(SleepRecord)
class SleepRecordAdmin(admin.ModelAdmin):
    list_display = ('baby', 'date', 'start_time', 'end_time', 'duration_minutes', 'sleep_quality')
    list_filter = ('sleep_quality', 'date', 'created_at')
    search_fields = ('baby__name', 'baby__parent__first_name', 'baby__parent__last_name')
    readonly_fields = ('created_at',)


@admin.register(DiaperRecord)
class DiaperRecordAdmin(admin.ModelAdmin):
    list_display = ('baby', 'date', 'time', 'diaper_type', 'created_at')
    list_filter = ('diaper_type', 'date', 'created_at')
    search_fields = ('baby__name', 'baby__parent__first_name', 'baby__parent__last_name')
    readonly_fields = ('created_at',)


@admin.register(Vaccination)
class VaccinationAdmin(admin.ModelAdmin):
    list_display = ('name', 'recommended_age_weeks', 'is_required', 'created_at')
    list_filter = ('is_required', 'recommended_age_weeks')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at',)


@admin.register(VaccinationRecord)
class VaccinationRecordAdmin(admin.ModelAdmin):
    list_display = ('baby', 'vaccination', 'date_given', 'doctor_name', 'next_due_date')
    list_filter = ('date_given', 'vaccination', 'created_at')
    search_fields = ('baby__name', 'vaccination__name', 'doctor_name', 'clinic_name')
    readonly_fields = ('created_at',)


@admin.register(Milestone)
class MilestoneAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'typical_age_weeks', 'age_range_start', 'age_range_end', 'is_important')
    list_filter = ('category', 'is_important', 'typical_age_weeks')
    search_fields = ('title', 'description')
    readonly_fields = ('created_at',)


@admin.register(BabyMilestoneRecord)
class BabyMilestoneRecordAdmin(admin.ModelAdmin):
    list_display = ('baby', 'milestone', 'date_achieved', 'age_at_milestone', 'created_at')
    list_filter = ('milestone__category', 'date_achieved', 'created_at')
    search_fields = ('baby__name', 'milestone__title')
    readonly_fields = ('created_at', 'age_at_milestone')
