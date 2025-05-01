from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('cart/', views.cart, name='cart'),
    path('policy/', views.policy, name='policy'),
    path('event_list/', views.event_list, name='event_list'),
    path('event_list/<int:pk>/', views.event_details, name='event_detail'),


]  