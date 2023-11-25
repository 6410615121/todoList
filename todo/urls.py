from user.views import resetpass ,login_view,forgetpass,register
import os
import shutil

"""
URL configuration for todo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path , include
from django.shortcuts import redirect
from .views import homepage
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', homepage, name="index"),
    path('<uuid:requestID>/resetpass/', resetpass, name='resetpass'),
    path('login/', login_view, name='login'),
    path('register/', register, name='register'),
    path('forgetpassword/', forgetpass, name='forgetpass'),
    path('admin/', admin.site.urls),
    path("project/", include('project.urls')),
    path("task/", include('task.urls')),
    path("user/", include('user.urls')),
    
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


