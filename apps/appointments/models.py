from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone


class DoctorAvailability(models.Model):
    DAYS_OF_WEEK = (
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    )
    
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='availabilities')
    day_of_week = models.IntegerField(choices=DAYS_OF_WEEK)
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_active = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ['doctor', 'day_of_week', 'start_time']
        ordering = ['day_of_week', 'start_time']
    
    def __str__(self):
        return f"Dr. {self.doctor.get_full_name()} - {self.get_day_of_week_display()} {self.start_time}-{self.end_time}"


class Appointment(models.Model):
    STATUS_CHOICES = (
        ('scheduled', 'Scheduled'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('no_show', 'No Show'),
    )
    
    APPOINTMENT_TYPES = (
        ('consultation', 'Consultation'),
        ('checkup', 'Regular Checkup'),
        ('prenatal', 'Prenatal Visit'),
        ('postnatal', 'Postnatal Visit'),
        ('emergency', 'Emergency'),
        ('follow_up', 'Follow-up'),
    )
    
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='patient_appointments')
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='doctor_appointments')
    date = models.DateField()
    time = models.TimeField()
    appointment_type = models.CharField(max_length=20, choices=APPOINTMENT_TYPES, default='consultation')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    reason = models.TextField()
    notes = models.TextField(blank=True, help_text="Doctor's notes after appointment")
    duration_minutes = models.PositiveIntegerField(default=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['date', 'time']
        unique_together = ['doctor', 'date', 'time']
    
    def __str__(self):
        return f"{self.patient.get_full_name()} with Dr. {self.doctor.get_full_name()} on {self.date} at {self.time}"
    
    def get_absolute_url(self):
        return reverse('appointments:detail', kwargs={'pk': self.pk})
    
    @property
    def is_past(self):
        appointment_datetime = timezone.datetime.combine(self.date, self.time)
        return appointment_datetime < timezone.now()
    
    @property
    def is_today(self):
        return self.date == timezone.now().date()
    
    @property
    def can_be_cancelled(self):
        # Can only cancel if appointment is in the future and not already cancelled/completed
        return not self.is_past and self.status in ['scheduled', 'confirmed']


class AppointmentReminder(models.Model):
    REMINDER_TYPES = (
        ('email', 'Email'),
        ('sms', 'SMS'),
        ('notification', 'In-App Notification'),
    )
    
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name='reminders')
    reminder_type = models.CharField(max_length=20, choices=REMINDER_TYPES)
    hours_before = models.PositiveIntegerField(default=24)
    is_sent = models.BooleanField(default=False)
    sent_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['appointment', 'reminder_type', 'hours_before']
    
    def __str__(self):
        return f"Reminder for {self.appointment} - {self.hours_before}h before"
