from django.db import models
from django.contrib.auth.models import User

# Create your models here.


from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    LIVE = 1
    DELETE = 0
    DELETE_CHOICES = ((LIVE, 'Live'), (DELETE, 'Delete'))

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer_profile')
    name = models.CharField(max_length=200)
    address = models.TextField()
    description = models.TextField()
    
    # Change phone from IntegerField to CharField (to avoid integer overflow)
    phone = models.CharField(max_length=20, null=True, blank=True)  

    delete_status = models.IntegerField(choices=DELETE_CHOICES, default=LIVE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Ensure proper DecimalField settings for latitude and longitude
    latitude = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)

    def __str__(self) -> str:
        return self.user.username



