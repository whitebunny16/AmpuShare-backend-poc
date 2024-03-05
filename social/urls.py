from django.urls import path

from .views import *

urlpatterns = [
    # Post
    path('posts', posts),
    path('posts/<str:post_id>', post_detail),

    # Like
    path('posts/<str:post_id>/like', like_post),
    path('posts/<str:post_id>/like', unlike_post),

    # Comment
    path('posts/<str:post_id>/comment', add_comment),
    path('posts/<str:post_id>/comment', delete_comment),
]
