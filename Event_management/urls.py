"""
URL configuration for Event_management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from EventApp import views as e_views
from .import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', e_views.home, name='home'),
    path('login/', e_views.login, name='login'),
    path('C_profile/', e_views.C_profile, name='C_profile'),
    path('product/', e_views.product, name='product'),
    path('MeetTheTeam/', e_views.MeetTheTeam, name='MeetTheTeam'),
    path('Reviews/', e_views.Reviews, name='Reviews'),
    path('Portfolio/', e_views.Portfolio, name='Portfolio'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

