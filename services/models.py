from django.db import models
from django.contrib.auth.models import User

# Create your models here.

from django.db import models
from django.contrib.auth.models import User

class Services(models.Model):
    title = models.CharField(max_length=255)           
    description = models.TextField()
    price = models.FloatField()
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='service_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    average_rating = models.FloatField(default=0.0) 
    priority = models.IntegerField(default=0)
    city = models.CharField(max_length=100, null=True, blank=True) 
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    def update_average_rating(self):
        """Updates the service's average rating based on existing reviews."""
        reviews = self.reviews.all()  
        total_reviews = reviews.count()

        if total_reviews > 0:
            avg = sum(review.rating for review in reviews) / total_reviews
        else:
            avg = 0.0  # No reviews, default to 0.0
        
        self.average_rating = avg
        self.save()

    def __str__(self):
        return self.title


class Review(models.Model):
    service = models.ForeignKey(Services, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  # Rating from 1 to 5
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} for {self.service.title}"
