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
from django.urls import path, include
from EventApp import views as e_views
from .import settings
from django.conf.urls.static import static




urlpatterns = [
    path('admin/', admin.site.urls),
    path('', e_views.home, name='home'),
    path('signup/', e_views.signup, name='signup'),
    path('profile/', e_views.profile_view, name='profile'), 
    path('login/', e_views.user_login, name='login'),
    path('logout/', e_views.user_logout, name='logout'),
    path('cart/', e_views.cart, name='cart'),
    path('meet_the_team/', e_views.meet_the_team, name='meet_the_team'),
    path('product/', e_views.product, name='product'),
    path('product/<str:id>', e_views.product_details, name = 'product_details'),
    path('product/add_product/', e_views.add_product, name='add_product'),
    path('product/update_product/<str:id>', e_views.update_product, name='update_product'),
    path('product/delete_product/<str:id>', e_views.delete_product, name='delete_product'),
    path('meet_the_team/sajid/', e_views.profile_sajid, name='sajid_info'),
    path('meet_the_team/toma/', e_views.profile_toma, name='toma_info'),
    path('search/', e_views.search, name='search'),
    path('policy/', e_views.policy, name='policy'),
    path('event_list/', e_views.event_list, name='event_list'),
    path('event_list/<int:pk>/', e_views.event_details, name='event_detail'),



] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

