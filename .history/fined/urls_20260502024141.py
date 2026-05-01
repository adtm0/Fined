"""
URL configuration for fined project.

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
from django.contrib.auth.views import LoginView
from django.urls import path, include
from tracker import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', views.register, name='register'),
    path()
    path('', include('django.contrib.auth.urls')),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('account/add/', views.add_account, name='add_account'),
    path('account/<int:account_id>/add-transaction/', views.add_transaction, name='add_transaction'),
    path('transaction/add/', views.add_transaction_modal, name='add_transaction_modal'),
    path('account/<int:account_id>/', views.account_detail, name='account_detail'),
    path('transaction/<int:transaction_id>/edit/', views.edit_transaction, name='edit_transaction'),
    path('transaction/<int:transaction_id>/delete/', views.delete_transaction, name='delete_transaction'),
    path('account/<int:account_id>/edit/', views.edit_account, name='edit_account'),
    path('account/<int:account_id>/delete/', views.delete_account, name='delete_account'),
    path('history/', views.history, name='history'),
]
