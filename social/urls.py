from django.urls import path

from .views import *

urlpatterns = [
    path('post-detail', get_post_detail),
    path('create-post', create_post),
]
