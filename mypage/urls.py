from django.urls import path, include
from .views import *

urlpatterns = [
    path('get-user-info/', get_user_info, name='get-user-info'),                 # 1번
    # path                                                                       # 2번
    path("get-liked-post/", get_liked_post, name="get-liked-post"),              # 3번
]
