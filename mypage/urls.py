from django.urls import path, include
from .views import *

urlpatterns = [
    path('get-normal-user-info/', get_normal_user_info, name='get-normal-user-info'),          # 1번
    path('get-operator-user-info/', get_operator_user_info, name="get-operator-user-info"),    # 2번
    path('get-applied-list/', get_applied_list, name="get-applied-list"),                      # 3번                                                        
    path("get-liked-post/", get_liked_post, name="get-liked-post"),                            # 4번
    path("get-crews-posts/", get_crews_posts, name="get-crews-posts"),                         # 5번
    path('get-all-mypage-info/', get_all_mypage_info, name="get-all-mypage-info")              # 6번
]
