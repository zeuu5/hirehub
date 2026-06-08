from django.urls import path
from . import views 

urlpatterns = [
    path('analyze/',views.analyze_damage, name='analyze_damage'),
    # path('api/chat/', views.chat_api, name='chat_api'),

]
