from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register_user, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),

    path('admin-view/', views.admin_only_view, name='admin_only'),
    path('premium-view/', views.premium_only_view, name='premium_only'),
    path('staff-view/', views.staff_only_view, name='staff_only'),
    path('cliente-view/', views.cliente_only_view, name='cliente_only'),
    path('', views.home, name='home'),

]
