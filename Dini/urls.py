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
from django.conf.urls.static import static
from django.urls import path
from . import settings
from my_app import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about', views.about, name='about'),
    path('contact-us', views.contact, name='contact'),
    path('login', views.login_applicant, name='login'),
    path('register', views.register_applicant, name='register'),
    path('logout', views.user_logout, name='logout'),
    path('interpreters', views.interpreters, name='interpreters'),
    path('appointment', views.appointment, name='appointment'),
    path('interpretation', views.interpretation, name='interpretation'),
    path('job_application', views.job_application, name='job_application'),
    path('job_application_success', views.job_application_success, name='job_application_success'),
path('edit-profile', views.edit_interpreter_profile, name='edit_interpreter_profile'),
    path('event_detail/<int:event_id>/', views.event_detail, name='event_detail'),
    path('past_events', views.past_events, name='past_events'),
    path('educational-resources', views.educational_resources, name='educational_resources'),
    path('dashboard', views.applicant_dashboard, name='dashboard'),
    path('admin/', admin.site.urls),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
