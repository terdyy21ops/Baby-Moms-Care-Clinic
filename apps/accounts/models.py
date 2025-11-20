from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image


class UserProfile(models.Model):
    USER_ROLES = (
        ('mother', 'Mother'),
        ('doctor', 'Doctor'),
        ('admin', 'Admin'),
    )
    
    ACCOUNT_STATUS = (
        ('active', 'Active'),
        ('deactivated', 'Deactivated'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=USER_ROLES, default='mother')
    account_status = models.CharField(max_length=15, choices=ACCOUNT_STATUS, default='active')
    phone = models.CharField(max_length=15, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    emergency_contact_name = models.CharField(max_length=100, blank=True)
    emergency_contact_phone = models.CharField(max_length=15, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Doctor specific fields
    license_number = models.CharField(max_length=50, blank=True)
    specialization = models.CharField(max_length=100, blank=True)
    years_experience = models.PositiveIntegerField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.get_full_name()} ({self.get_role_display()})"
    
    def is_account_active(self):
        return self.account_status == 'active' and self.user.is_active
    
    def get_absolute_url(self):
        return reverse('accounts:profile', kwargs={'pk': self.pk})
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        # Resize profile picture
        if self.profile_picture:
            img = Image.open(self.profile_picture.path)
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.profile_picture.path)


class DoctorApplication(models.Model):
    """Model for doctor applications - not actual accounts"""
    STATUS_CHOICES = (
        ('pending', 'Pending Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )
    
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    license_number = models.CharField(max_length=50, help_text='PRC/License ID')
    specialization = models.CharField(max_length=100)
    years_experience = models.PositiveIntegerField(default=0)
    clinic_affiliation = models.CharField(max_length=200, blank=True)
    valid_id = models.FileField(upload_to='doctor_applications/', help_text='Upload valid ID')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_applications')
    rejection_reason = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Dr. {self.first_name} {self.last_name} - {self.get_status_display()}"


class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('appointment', 'Appointment'),
        ('pregnancy', 'Pregnancy'),
        ('baby', 'Baby'),
        ('article', 'Article'),
        ('forum', 'Forum'),
        ('system', 'System'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=200)
    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.user.username}"
