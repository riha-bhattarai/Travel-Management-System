"""
URL configuration for TravelManagementSystem project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from travel import views


from django.contrib import admin
from django.urls import path
from travel import views


urlpatterns = [

    path('admin/', admin.site.urls),

    path('', views.home, name='home'),

    path('dashboard/', views.dashboard, name='dashboard'),

    path('packages/', views.packages, name='packages'),

    path('booking/<int:package_id>/', views.booking, name='booking'),

    path('register/', views.register, name='register'),

    path('login/', views.user_login, name='login'),

    path('logout/', views.user_logout, name='logout'),

    path('my-bookings/', views.my_bookings, name='my_bookings'),

    path('payment/<int:booking_id>/', views.payment, name='payment'),
  
    path('admin-login/', views.admin_login, name='admin_login'),
    
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),

    

]