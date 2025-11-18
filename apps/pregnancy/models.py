from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta


class PregnancyLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pregnancy_logs')
    start_date = models.DateField(help_text="First day of last menstrual period")
    due_date = models.DateField()
    is_active = models.BooleanField(default=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.get_full_name()} - Due: {self.due_date}"
    
    def get_absolute_url(self):
        return reverse('pregnancy:detail', kwargs={'pk': self.pk})
    
    @property
    def current_week(self):
        """Calculate current week of pregnancy"""
        if not self.is_active:
            return None
        
        days_pregnant = (timezone.now().date() - self.start_date).days
        weeks = days_pregnant // 7
        return max(0, weeks)
    
    @property
    def days_remaining(self):
        """Calculate days until due date"""
        return (self.due_date - timezone.now().date()).days
    
    @property
    def trimester(self):
        """Determine current trimester"""
        week = self.current_week
        if week is None:
            return None
        
        if week <= 12:
            return 1
        elif week <= 27:
            return 2
        else:
            return 3
    
    @property
    def progress_percentage(self):
        """Calculate pregnancy progress as percentage"""
        if not self.is_active:
            return 100
        
        total_days = (self.due_date - self.start_date).days
        elapsed_days = (timezone.now().date() - self.start_date).days
        
        if elapsed_days < 0:
            return 0
        elif elapsed_days > total_days:
            return 100
        
        return min(100, (elapsed_days / total_days) * 100)


class PregnancyWeeklyLog(models.Model):
    pregnancy = models.ForeignKey(PregnancyLog, on_delete=models.CASCADE, related_name='weekly_logs')
    week_number = models.PositiveIntegerField()
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="Weight in kg")
    symptoms = models.TextField(blank=True)
    mood = models.CharField(max_length=50, blank=True)
    energy_level = models.IntegerField(choices=[(i, i) for i in range(1, 11)], null=True, blank=True, help_text="1-10 scale")
    notes = models.TextField(blank=True)
    photo = models.ImageField(upload_to='pregnancy_photos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['pregnancy', 'week_number']
        ordering = ['-week_number']
    
    def __str__(self):
        return f"Week {self.week_number} - {self.pregnancy.user.get_full_name()}"


class PregnancyMilestone(models.Model):
    MILESTONE_TYPES = (
        ('appointment', 'Medical Appointment'),
        ('ultrasound', 'Ultrasound'),
        ('test', 'Medical Test'),
        ('symptom', 'Symptom'),
        ('movement', 'Baby Movement'),
        ('other', 'Other'),
    )
    
    pregnancy = models.ForeignKey(PregnancyLog, on_delete=models.CASCADE, related_name='milestones')
    title = models.CharField(max_length=200)
    description = models.TextField()
    milestone_type = models.CharField(max_length=20, choices=MILESTONE_TYPES)
    date = models.DateField()
    week_number = models.PositiveIntegerField(null=True, blank=True)
    is_important = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.title} - Week {self.week_number}"


class PregnancyReminder(models.Model):
    REMINDER_TYPES = (
        ('prenatal_visit', 'Prenatal Visit'),
        ('vitamin', 'Prenatal Vitamin'),
        ('exercise', 'Exercise'),
        ('test', 'Medical Test'),
        ('appointment', 'Appointment'),
        ('custom', 'Custom'),
    )
    
    FREQUENCY_CHOICES = (
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('once', 'One Time'),
    )
    
    pregnancy = models.ForeignKey(PregnancyLog, on_delete=models.CASCADE, related_name='reminders')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    reminder_type = models.CharField(max_length=20, choices=REMINDER_TYPES)
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    time = models.TimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['start_date', 'time']
    
    def __str__(self):
        return f"{self.title} - {self.get_frequency_display()}"


class PregnancyTip(models.Model):
    TRIMESTER_CHOICES = (
        (1, 'First Trimester (1-12 weeks)'),
        (2, 'Second Trimester (13-27 weeks)'),
        (3, 'Third Trimester (28-40 weeks)'),
        (0, 'All Trimesters'),
    )
    
    title = models.CharField(max_length=200)
    content = models.TextField()
    trimester = models.IntegerField(choices=TRIMESTER_CHOICES, default=0)
    week_range_start = models.PositiveIntegerField(null=True, blank=True)
    week_range_end = models.PositiveIntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['trimester', 'week_range_start']
    
    def __str__(self):
        return self.title
