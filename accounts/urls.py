from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import UserRegisterView, CustomTokenObtainPairView, sogang_mail_check, verification_code_check, get_normal_user_info, get_operator_user_info, get_applied_list, get_liked_post, get_crews_posts, get_all_mypage_info

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='user-register'), # 1번
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'), # 2번
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'), # 3번

    path('sogang-mail/', sogang_mail_check, name='sogang-mail-check'), # 4번
    path('verification-code/', verification_code_check, name='verification-code-check'),  # 5번
    
    # mypage
    path('normal-user/', get_normal_user_info, name='get-normal-user-info'),          # 6번
    path('operator-user/', get_operator_user_info, name="get-operator-user-info"),    # 7번
    path('applications/', get_applied_list, name="get-applied-list"),                      # 8번                                                        
    path("liked-posts/", get_liked_post, name="get-liked-post"),                            # 9번
    path("posts/", get_crews_posts, name="get-crews-posts"),                         # 10번
    path('all/', get_all_mypage_info, name="get-all-mypage-info")              # 11번
]
