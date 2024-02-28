from django.urls import path
from .views import *

urlpatterns = [
    path('user-detail', get_user_detail),
    path('create-user', get_user_detail),
    path('', get_user_detail)
]
