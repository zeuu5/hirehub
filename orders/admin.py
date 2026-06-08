from django.contrib import admin
from orders.models import Order,OrderedItem
# Register your models here.
class OrderAdmin(admin.ModelAdmin):
   class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'provider', 'status', 'paid_amount', 'payment_status']
    list_filter = ('status', 'payment_status')  # Remove 'owner' and 'order_status'


admin.site.register(Order,OrderAdmin)