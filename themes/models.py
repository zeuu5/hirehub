from django.db import models
from django.shortcuts import render, redirect
from services.models import Services


# Create your models here.

class SiteSetting(models.Model):
    banner=models.ImageField(upload_to='media/site/')
    caption=models.TextField()



class TermsAndConditions(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()

    def __str__(self):
        return self.title

#
from django.db import models

class AboutUs(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    
    def __str__(self):
        return self.title
    
from django.db import models

from django.db import models

class ContactUs(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15, blank=True, null=True)  # Added phone field
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Contact from {self.name}"




