from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='user-register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('sogang-mail-check/', sogang_mail_check, name='sogang-mail-check'), # 4번
    path('verification-code-check/', verification_code_check, name='verification-code-check'),  # 5번
]
