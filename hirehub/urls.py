"""
URL configuration for hirehub project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from django.conf import settings
from django.conf.urls.static import static  


from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('services.urls')),  # Homepage
    path('customer/', include('customers.urls')),  # Add trailing slash
    path('order/', include('orders.urls')),        # Add trailing slash
    path('admins/', include('admins.urls')),       # Add trailing slash
    path('ai_service/', include('ai_service.urls')),
    path('themes/', include('themes.urls')),       # Add trailing slash
    path('messageroom/', include('messageroom.urls')),  # Add trailing slash
]

# Serve media files in development
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

