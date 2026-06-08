from django.db import models

# Create your models here.

class Feedback(models.Model):
    name=models.CharField(max_length=20)
    email=models.EmailField()
    your_feedback=models.CharField(max_length=500)