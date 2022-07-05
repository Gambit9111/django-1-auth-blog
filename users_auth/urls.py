from django.urls import path, include
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('moderator/', views.moderator, name='moderator'),
    path('create-admin/', views.create_admin, name='create_admin'),
    path('create-mod/', views.create_mod, name='create_mod'),
    path('posts/<int:user_id>', views.posts, name='posts'),
]