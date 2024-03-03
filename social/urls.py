from django.urls import path

from .views import *

urlpatterns = [
    # Post
    path('posts', posts),
    path('posts/<str:post_id>', post_detail),

    # Like
    path('post/<str:post_id>/like/', like_post),
    path('post/<str:post_id>/like/', unlike_post),

    # Comment
    path('post/<str:post_id>/comment/', add_comment),
    path('post/<str:post_id>/comment/', delete_comment),
]
