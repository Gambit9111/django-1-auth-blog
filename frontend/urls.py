from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('home/', views.home, name='home'),
    path('create-post/', views.create_post, name='create-post'),
]