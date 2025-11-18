from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class EmergencyContact(models.Model):
    CONTACT_TYPES = (
        ('hospital', 'Hospital'),
        ('clinic', 'Clinic'),
        ('doctor', 'Doctor'),
        ('midwife', 'Midwife'),
        ('pharmacy', 'Pharmacy'),
        ('emergency', 'Emergency Services'),
        ('family', 'Family'),
        ('friend', 'Friend'),
        ('other', 'Other'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='emergency_contacts')
    name = models.CharField(max_length=100)
    contact_type = models.CharField(max_length=20, choices=CONTACT_TYPES)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    is_primary = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-is_primary', 'contact_type', 'name']
    
    def __str__(self):
        return f"{self.name} ({self.get_contact_type_display()})"
    
    def get_absolute_url(self):
        return reverse('support:contact_detail', kwargs={'pk': self.pk})


class SupportTicket(models.Model):
    STATUS_CHOICES = (
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    )
    
    PRIORITY_CHOICES = (
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    )
    
    CATEGORY_CHOICES = (
        ('technical', 'Technical Issue'),
        ('account', 'Account Issue'),
        ('medical', 'Medical Question'),
        ('feature', 'Feature Request'),
        ('bug', 'Bug Report'),
        ('other', 'Other'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='support_tickets')
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tickets')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Ticket #{self.pk}: {self.title}"
    
    def get_absolute_url(self):
        return reverse('support:ticket_detail', kwargs={'pk': self.pk})


class SupportMessage(models.Model):
    ticket = models.ForeignKey(SupportTicket, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    is_staff_reply = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"Message from {self.sender.username} on Ticket #{self.ticket.pk}"


class FAQ(models.Model):
    CATEGORIES = (
        ('account', 'Account & Profile'),
        ('appointments', 'Appointments'),
        ('pregnancy', 'Pregnancy Tracking'),
        ('baby', 'Baby Care'),
        ('technical', 'Technical Support'),
        ('general', 'General'),
    )
    
    question = models.CharField(max_length=300)
    answer = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORIES)
    order = models.PositiveIntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    views_count = models.PositiveIntegerField(default=0)
    helpful_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['category', 'order', 'question']
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQs'
    
    def __str__(self):
        return self.question


class HelpfulVote(models.Model):
    faq = models.ForeignKey(FAQ, on_delete=models.CASCADE, related_name='votes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_helpful = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['faq', 'user']
    
    def __str__(self):
        return f"{self.user.username} voted {'helpful' if self.is_helpful else 'not helpful'} for FAQ #{self.faq.pk}"


class ResourceLink(models.Model):
    LINK_TYPES = (
        ('website', 'Website'),
        ('hotline', 'Hotline'),
        ('app', 'Mobile App'),
        ('document', 'Document'),
        ('video', 'Video'),
        ('other', 'Other'),
    )
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    url = models.URLField()
    link_type = models.CharField(max_length=20, choices=LINK_TYPES)
    is_emergency = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-is_emergency', '-is_featured', 'order', 'title']
    
    def __str__(self):
        return self.title


class ChatMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_messages')
    message = models.TextField()
    is_bot_response = models.BooleanField(default=False)
    session_id = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        sender = "Bot" if self.is_bot_response else self.user.username
        return f"{sender}: {self.message[:50]}..."
