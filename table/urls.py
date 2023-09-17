from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
# from rest_framework_simplejwt.views import TokenRefreshView
# from .views import UserRegisterView, CustomTokenObtainPairView


router = DefaultRouter()
router.register(r'user', UserViewSet)
router.register(r'category', CategoryViewSet)
router.register(r'crew', CrewViewSet)
router.register(r'administrator', AdministratorViewSet)
router.register(r'post', PostViewSet)
router.register(r'post_image', PostImageViewSet)
router.register(r'apply', ApplyViewSet)
router.register(r'like', LikeViewSet)
router.register(r'section', SectionViewSet)
router.register(r'long_sentence', LongSentenceViewSet)
router.register(r'long_sentence_answer', LongSentenceAnswerViewSet)
router.register(r'check_box', CheckBoxViewSet)
router.register(r'check_box_option', CheckBoxOptionViewSet)
router.register(r'check_box_answer', CheckBoxAnswerViewSet)
router.register(r'file', FileViewSet)
router.register(r'file_answer', FileAnswerViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # path('register/', UserRegisterView.as_view(), name='user-register'),            # 회원가입 Api 문서 Ok
    # path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),  # 로그인 Api 문서 Ok
    # path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),       # access token 리프레쉬 Api 문서 Ok
]

