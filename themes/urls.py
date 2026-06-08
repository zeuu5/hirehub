from django.urls import path
from . import views

urlpatterns = [
    path('terms-and-conditions/', views.terms_and_conditions, name='terms_and_conditions'),
    path('about-us/', views.about_us, name='about_us'),
    path('contact/', views.contact_us, name='contact')

]
