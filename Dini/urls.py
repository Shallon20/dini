"""
URL configuration for Dini project.

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
from django.urls import path

from my_app import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about', views.about, name='about'),
    path('services', views.services, name='services'),
    path('contact-us', views.contact, name='contact'),
    path('gallery', views.gallery, name='gallery'),
    path('login', views.login_user, name='login'),
    path('register', views.register, name='register'),
    path('logout', views.logout, name='logout'),
    path('update_user', views.update_user, name='update_user'),
    path('update_info', views.update_info, name='update_info'),
    path('update_password', views.update_password, name='update_password'),
    path('interpreters', views.interpreters, name='interpreters'),
    path('appointment', views.appointment, name='appointment'),
    path('job_application', views.job_application, name='job_application'),
    path('job_application_success', views.job_application_success, name='job_application_success'),
    path('event_detail/<int:event_id>/', views.event_detail, name='event_detail'),
    path('admin/', admin.site.urls),
]
