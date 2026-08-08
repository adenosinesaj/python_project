"""
URL configuration for Event_management project.
"""
from django.contrib import admin
from django.urls import path
from EventApp import views as e_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Administrative & Authentication Routes
    path('admin/', admin.site.urls),
    path('', e_views.home, name='home'),
    path('signup/', e_views.signup, name='signup'),
    path('login/', e_views.user_login, name='login'),
    path('logout/', e_views.user_logout, name='logout'),
    path('profile/', e_views.profile_view, name='profile_view'),

    # Product & Marketplace Management Routes
    path('products/', e_views.product_list, name='product_list'), # Added plural route
    path('product/', e_views.product_list),                       # Retained singular route for backwards compatibility
    path('product/<int:id>/', e_views.product_details, name='product_detail'), # Updated name to 'product_detail'
    path('product/add_product/', e_views.add_product, name='add_product'),
    path('product/update_product/<int:id>/', e_views.update_product, name='update_product'),
    path('product/delete_product/<int:id>/', e_views.delete_product, name='delete_product'),

    # Vendor Directory Routes
    path('vendors/', e_views.vendor_list, name='vendor_list'),
    path('vendor/<int:user_id>/', e_views.vendor_profile, name='vendor_profile'),

    # Shopping Cart & Checkout Routes
    path('cart/', e_views.view_cart, name='view_cart'),
    path('cart/add/<int:product_id>/', e_views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:item_id>/', e_views.update_cart_quantity, name='update_cart_quantity'), # Added AJAX quantity update route
    path('cart/remove/<int:item_id>/', e_views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', e_views.checkout, name='checkout'),
    path('orders/', e_views.order_history, name='order_history'),

    # ==========================================
    # INTERACTIVE EVENT PLANNING ROUTES
    # ==========================================
    path('planner/', e_views.planner_dashboard, name='planner_dashboard'),
    path('planner/task/add/', e_views.add_checklist_task, name='add_checklist_task'),
    path('planner/task/toggle/<int:pk>/', e_views.toggle_checklist_task, name='toggle_checklist_task'),
    path('planner/task/delete/<int:pk>/', e_views.delete_checklist_task, name='delete_checklist_task'),
    path('planner/budget/add/', e_views.add_budget_item, name='add_budget_item'),
    path('planner/budget/delete/<int:pk>/', e_views.delete_budget_item, name='delete_budget_item'),

    # Event Portfolios & Search
    path('event_list/', e_views.event_list, name='event_list'),
    path('event_list/<int:pk>/', e_views.event_details, name='event_detail'),
    path('search/', e_views.search, name='search'),

    # Static & Support Pages
    path('policy/', e_views.policy, name='policy'),
    path('help/', e_views.help_page, name='help'),

    # Team Profiles
    path('meet_the_team/', e_views.meet_the_team, name='meet_the_team'),
    
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)