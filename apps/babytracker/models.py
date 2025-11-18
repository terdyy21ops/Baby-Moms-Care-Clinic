from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta


class Baby(models.Model):
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    )
    
    parent = models.ForeignKey(User, on_delete=models.CASCADE, related_name='babies')
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    birth_date = models.DateField()
    birth_weight = models.DecimalField(max_digits=5, decimal_places=2, help_text="Weight in kg")
    birth_height = models.DecimalField(max_digits=5, decimal_places=2, help_text="Height in cm")
    photo = models.ImageField(upload_to='baby_photos/', blank=True, null=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-birth_date']
        verbose_name_plural = 'Babies'
    
    def __str__(self):
        return f"{self.name} ({self.parent.get_full_name()})"
    
    def get_absolute_url(self):
        return reverse('babytracker:detail', kwargs={'pk': self.pk})
    
    @property
    def age_in_days(self):
        """Calculate baby's age in days"""
        return (timezone.now().date() - self.birth_date).days
    
    @property
    def age_in_weeks(self):
        """Calculate baby's age in weeks"""
        return self.age_in_days // 7
    
    @property
    def age_in_months(self):
        """Calculate baby's age in months (approximate)"""
        return self.age_in_days // 30
    
    @property
    def age_display(self):
        """Display age in appropriate format"""
        days = self.age_in_days
        
        if days < 0:
            return "Not born yet"
        elif days < 7:
            return f"{days} day{'s' if days != 1 else ''}"
        elif days < 60:  # Less than 2 months
            weeks = days // 7
            remaining_days = days % 7
            if remaining_days == 0:
                return f"{weeks} week{'s' if weeks != 1 else ''}"
            else:
                return f"{weeks} week{'s' if weeks != 1 else ''}, {remaining_days} day{'s' if remaining_days != 1 else ''}"
        else:
            months = days // 30
            return f"{months} month{'s' if months != 1 else ''}"


class GrowthRecord(models.Model):
    baby = models.ForeignKey(Baby, on_delete=models.CASCADE, related_name='growth_records')
    date = models.DateField()
    weight = models.DecimalField(max_digits=5, decimal_places=2, help_text="Weight in kg")
    height = models.DecimalField(max_digits=5, decimal_places=2, help_text="Height in cm")
    head_circumference = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="Head circumference in cm")
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date']
        unique_together = ['baby', 'date']
    
    def __str__(self):
        return f"{self.baby.name} - {self.date}"
    
    @property
    def age_at_record(self):
        """Calculate baby's age at the time of this record"""
        return (self.date - self.baby.birth_date).days


class FeedingRecord(models.Model):
    FEEDING_TYPES = (
        ('breastfeeding', 'Breastfeeding'),
        ('bottle', 'Bottle'),
        ('solid', 'Solid Food'),
        ('mixed', 'Mixed'),
    )
    
    baby = models.ForeignKey(Baby, on_delete=models.CASCADE, related_name='feeding_records')
    date = models.DateField()
    time = models.TimeField()
    feeding_type = models.CharField(max_length=20, choices=FEEDING_TYPES)
    duration_minutes = models.PositiveIntegerField(null=True, blank=True, help_text="Duration in minutes (for breastfeeding)")
    amount_ml = models.PositiveIntegerField(null=True, blank=True, help_text="Amount in ml (for bottle feeding)")
    food_description = models.TextField(blank=True, help_text="Description of solid food")
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date', '-time']
    
    def __str__(self):
        return f"{self.baby.name} - {self.get_feeding_type_display()} on {self.date} at {self.time}"


class SleepRecord(models.Model):
    baby = models.ForeignKey(Baby, on_delete=models.CASCADE, related_name='sleep_records')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField(null=True, blank=True)
    duration_minutes = models.PositiveIntegerField(null=True, blank=True)
    sleep_quality = models.IntegerField(choices=[(i, i) for i in range(1, 6)], null=True, blank=True, help_text="1-5 scale")
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date', '-start_time']
    
    def __str__(self):
        return f"{self.baby.name} - Sleep on {self.date} at {self.start_time}"
    
    def save(self, *args, **kwargs):
        # Calculate duration if end_time is provided
        if self.start_time and self.end_time:
            start_datetime = timezone.datetime.combine(self.date, self.start_time)
            end_datetime = timezone.datetime.combine(self.date, self.end_time)
            
            # Handle overnight sleep
            if self.end_time < self.start_time:
                end_datetime += timedelta(days=1)
            
            duration = end_datetime - start_datetime
            self.duration_minutes = int(duration.total_seconds() / 60)
        
        super().save(*args, **kwargs)


class DiaperRecord(models.Model):
    DIAPER_TYPES = (
        ('wet', 'Wet'),
        ('dirty', 'Dirty'),
        ('both', 'Both'),
        ('dry', 'Dry'),
    )
    
    baby = models.ForeignKey(Baby, on_delete=models.CASCADE, related_name='diaper_records')
    date = models.DateField()
    time = models.TimeField()
    diaper_type = models.CharField(max_length=10, choices=DIAPER_TYPES)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date', '-time']
    
    def __str__(self):
        return f"{self.baby.name} - {self.get_diaper_type_display()} on {self.date} at {self.time}"


class Vaccination(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    recommended_age_weeks = models.PositiveIntegerField(help_text="Recommended age in weeks")
    is_required = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['recommended_age_weeks']
    
    def __str__(self):
        return f"{self.name} (Week {self.recommended_age_weeks})"


class VaccinationRecord(models.Model):
    baby = models.ForeignKey(Baby, on_delete=models.CASCADE, related_name='vaccination_records')
    vaccination = models.ForeignKey(Vaccination, on_delete=models.CASCADE)
    date_given = models.DateField()
    doctor_name = models.CharField(max_length=100, blank=True)
    clinic_name = models.CharField(max_length=100, blank=True)
    batch_number = models.CharField(max_length=50, blank=True)
    next_due_date = models.DateField(null=True, blank=True)
    side_effects = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date_given']
        unique_together = ['baby', 'vaccination']
    
    def __str__(self):
        return f"{self.baby.name} - {self.vaccination.name} on {self.date_given}"


class Milestone(models.Model):
    MILESTONE_CATEGORIES = (
        ('physical', 'Physical Development'),
        ('cognitive', 'Cognitive Development'),
        ('social', 'Social & Emotional'),
        ('language', 'Language & Communication'),
        ('motor', 'Motor Skills'),
    )
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=MILESTONE_CATEGORIES)
    typical_age_weeks = models.PositiveIntegerField(help_text="Typical age in weeks when milestone is reached")
    age_range_start = models.PositiveIntegerField(help_text="Earliest typical age in weeks")
    age_range_end = models.PositiveIntegerField(help_text="Latest typical age in weeks")
    is_important = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['typical_age_weeks']
    
    def __str__(self):
        return f"{self.title} (Week {self.typical_age_weeks})"


class BabyMilestoneRecord(models.Model):
    baby = models.ForeignKey(Baby, on_delete=models.CASCADE, related_name='milestone_records')
    milestone = models.ForeignKey(Milestone, on_delete=models.CASCADE)
    date_achieved = models.DateField()
    notes = models.TextField(blank=True)
    photo = models.ImageField(upload_to='milestone_photos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date_achieved']
        unique_together = ['baby', 'milestone']
    
    def __str__(self):
        return f"{self.baby.name} - {self.milestone.title} on {self.date_achieved}"
    
    @property
    def age_at_milestone(self):
        """Calculate baby's age when milestone was achieved"""
        return (self.date_achieved - self.baby.birth_date).days
