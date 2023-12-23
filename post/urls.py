from django.urls import path
from .views import PostCreate, get_crew_info, like_post, post_content, click_apply_button

urlpatterns = [
    path('', PostCreate.as_view(), name='post-create'), # 모집 공고 생성(create)
    path('crew/', get_crew_info, name='get-crew-info'),                 # 1번
    path('<int:post_id>/like/', like_post, name='like-post'),                    # 2번
    path('', post_content, name='post-content'),                    # 3번
    path('apply/', click_apply_button, name='click-apply-button'),  # 4번
]
    