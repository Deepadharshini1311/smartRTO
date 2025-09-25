from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    #path('login/', auth_views.LoginView.as_view(template_name='rtoapp/login.html'), name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('apply-license/', views.apply_license, name='apply_license'),
    path('apply-vehicle/', views.apply_vehicle, name='apply_vehicle'),
    path('officer/', views.officer_dashboard, name='officer_dashboard'),
    path('approve/<int:app_id>/', views.approve_application, name='approve_application'),
    path('reject/<int:app_id>/', views.reject_application, name='reject_application'),
    #path('logout/', auth_views.LogoutView.as_view(template_name='rtoapp/logout.html'), name='logout'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
