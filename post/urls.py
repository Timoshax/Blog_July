from django.urls import path
from .views import post_list , post_details, add_post, edit_post, delete_post

urlpatterns = [
    path('', post_list, name='post_list'),
    path('post/<int:pid>/', post_details, name='post_details'),
    path('post/new-post/', add_post, name='new-post'),
    path('post/<int:pid>/edit/', edit_post, name = 'edit-post'),
    path('post/<int:pid>/delete/', delete_post, name = 'delete-post'),
]