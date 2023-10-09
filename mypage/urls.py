from django.urls import path, include
from .views import *

urlpatterns = [
    path('get-user-info/', get_user_info, name='get-user-info'),                 # 1번
]
