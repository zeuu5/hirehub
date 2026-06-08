from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Customer

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'phone', 'address')  # Add phone & address
    search_fields = ('user__username', 'phone', 'address')  # Enable search by phone/address
    list_filter = ('address',)  # Optional: Filter by address

admin.site.register(Customer, CustomerAdmin)

