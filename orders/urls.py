from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('ordershow_cart/', views.show_cart, name='show_cart'),  # Viewing the cart (No service_id needed)
    path('ordershow_cart/<int:service_id>/', views.show_cart, name='show_cart_with_id'),  # Adding service to cart
    path("order/add_to_cart/<int:service_id>/",views.add_to_cart, name="add_to_cart"),
    path("remove/<int:item_id>/", views.remove_item, name="remove_item"),

    
    path('payment_success/',views.payment_success, name='payment_success'),
path('orderorder/add_to_cart/<int:service_id>/', login_required(views.add_to_cart), name='add_to_cart'),
    path('create_order/', views.checkout_cart, name='create_order'),

    # path("create_order/<int:service_id>/",views.checkout_cart, name="create_order"),
    path("payment-success/",views.payment_success, name="payment_success"),
    path("provider-dashboard/", views.provider_dashboard, name="provider_dashboard"),
    path("service-delivered/<int:booking_id>/", views.service_delivered, name="service_delivered"),

    path("accept-booking/<int:booking_id>/", views.accept_booking, name="accept_booking"),
    path("reject-booking/<int:booking_id>/", views.reject_booking, name="reject_booking"),
    path("cancel-booking/<int:booking_id>/", views.cancel_booking, name="cancel_booking"),
]