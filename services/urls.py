
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('', views.index,name='Home'),
    path('service_list',views.list_service,name='list_service'),
    path('add_service',views.add_service,name='add_service'),
    path('service_details/<int:service_id>/', views.detail_service, name='detail_service'),
    path('select-category/',views.select_category, name='select_category'),
    path("service/<int:service_id>/review/", views.add_review, name="add_review"),
    path("select-city/",views.select_city, name="select_city"),
    
    
    
    
]

    



  

