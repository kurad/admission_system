from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index),
    path('signup', views.register),
    path('profile/', views.profile),
    path('addprofile', views.add_profile),
    path('dashboard', views.dashboard),
    path('login', views.login),
    path('logout', views.logout),
    path('applications', views.applications),
    path('save_application', views.application_save),
]
