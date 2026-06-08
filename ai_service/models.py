from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class DamageReport(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=[
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved')
    ], default='new')
    
    # Damage details
    damage_type = models.CharField(max_length=50, choices=[
        ('plumbing', 'Plumbing'),
        ('electrical', 'Electrical'),
        ('structural', 'Structural'),
        ('appliance', 'Appliance'),
        ('other', 'Other')
    ])
    description = models.TextField()
    severity = models.CharField(max_length=20, choices=[
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('emergency', 'Emergency')
    ])
    
    # Service suggestion
    suggested_service = models.CharField(max_length=100, blank=True)
    service_provider = models.CharField(max_length=100, blank=True)
    
class ChatMessage(models.Model):
    report = models.ForeignKey(DamageReport, on_delete=models.CASCADE, null=True, blank=True)
    sender = models.CharField(max_length=10, choices=[('user', 'User'), ('bot', 'Bot')])
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    intent = models.CharField(max_length=50, blank=True)  # For NLP classification