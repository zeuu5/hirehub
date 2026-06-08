from django.urls import path
from . import views
from django.urls import path

urlpatterns = [
    path('user_account',views.show_user_account,name='user_account'),
    path('logout',views.sign_out,name='logout'),
    path('user_profile',views.user_profile,name='user_profile'),
    path('worker_page',views.worker_page,name='worker_page'),
    path("provider-dashboard/", views.user_page, name="user_page"),
    path('worker/service/<int:service_id>/', views.service_detail_worker, name='service_detail_worker'),
    path('worker/service/<int:service_id>/delete/', views.delete_service, name='delete_service'),
   
    
    

]