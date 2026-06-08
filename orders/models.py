from django.db import models
from services.models import Services
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User





from django.db import models
from django.contrib.auth.models import User
from services.models import Services


from django.db import models
from django.contrib.auth.models import User
from services.models import Services


from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from services.models import Services

# class Order(models.Model):
#     CART_STAGE = 0
#     PROCESSING = 1
#     CONFIRMED = 2
#     REJECTED = 3
#     SERVICE_DELIVERED = 4
#     PENDING = 5

#     STATUS_CHOICES = [
#         (CART_STAGE, 'Cart'),
#         (PROCESSING, 'Processing'),
#         (CONFIRMED, 'Confirmed'),
#         (REJECTED, 'Rejected'),
#         (SERVICE_DELIVERED, 'Delivered'),
#         (PENDING, 'Pending'),
#     ]

#     service = models.ForeignKey(Services, on_delete=models.CASCADE)
#     customer = models.ForeignKey(User, related_name='customer_orders', on_delete=models.CASCADE)
#     provider = models.ForeignKey(User, related_name='provider_orders', on_delete=models.CASCADE)
#     status = models.IntegerField(choices=STATUS_CHOICES, default=PENDING)
#     paid_amount = models.FloatField(default=0.0)
#     payment_status = models.BooleanField(default=False)
#     razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)
#     service_time = models.DateTimeField(default=timezone.now)  # Field for service date
#     created_at = models.DateTimeField(auto_now_add=True)  # Field for booking date

#     def __str__(self):
#         return f"Order {self.id} - {self.service.title}"

# class OrderedItem(models.Model):
#     service = models.ForeignKey(Services, related_name='added_carts', on_delete=models.SET_NULL, null=True)
#     service_time = models.DateTimeField(default=timezone.now)
#     order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='added_items')

#     def __str__(self) -> str:
#         return f"Item-{self.id}-Order-{self.order.id if self.order else 'No Order'}"



class Order(models.Model):
    CART_STAGE = 0
    PROCESSING = 1
    CONFIRMED = 2
    REJECTED = 3
    SERVICE_DELIVERED = 4
    PENDING = 5

    STATUS_CHOICES = [
        (CART_STAGE, 'Cart'),
        (PROCESSING, 'Processing'),
        (CONFIRMED, 'Confirmed'),
        (REJECTED, 'Rejected'),
        (SERVICE_DELIVERED, 'Delivered'),
        (PENDING, 'Pending'),
    ]

    # service = models.ForeignKey(Services, on_delete=models.CASCADE,null=True, blank=True) 
    customer = models.ForeignKey(User, related_name='customer_orders', on_delete=models.CASCADE)
    provider = models.ForeignKey(User, related_name='provider_orders', on_delete=models.CASCADE)
    status = models.IntegerField(choices=STATUS_CHOICES, default=PENDING)
    paid_amount = models.FloatField(default=0.0)
    payment_status = models.BooleanField(default=False)
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)  # Booking date

    def __str__(self):
        return f"Order {self.id} - {self.customer.username} to {self.provider.username}"


class OrderedItem(models.Model):
    service = models.ForeignKey(Services, related_name='added_carts', on_delete=models.SET_NULL, null=True)
    service_time = models.DateTimeField(default=timezone.now)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='added_items')

    def __str__(self) -> str:
        return f"Item-{self.id}-Order-{self.order.id if self.order else 'No Order'}"
