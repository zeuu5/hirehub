from django.urls import path
from . import views

urlpatterns = [
    path('feedback/', views.save_feedback, name='save_feedback'),
]
    
