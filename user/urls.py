from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

from .views import *

urlpatterns = [
    # Profile
    path('users/profile/', own_profile),
    path('users/<str:user_id>/profile/', user_profile),

    # Buddy
    path('users/<str:user_id>/follow/', follow_user),
    path('users/<str:user_id>/unfollow/', unfollow_user),
    path('users/<str:user_id>/followers/', followers_list),
    path('users/<str:user_id>/following/', following_list),

    # Auth
    # path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/', user_login),
    path('register/', user_register),
    path('password/reset/', password_reset),
    path('password/reset/confirm/', password_reset_confirm),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
