from django.urls import path, include
from .views import *

urlpatterns = [
    path('get-crew-info/', get_crew_info, name='get-crew-info'),                 # 1번
    path('<int:post_id>/like/', like_post, name='like-post'),                    # 2번
    path('post-content/', post_content, name='post-content'),                    # 3번
    path('click-apply-button/', click_apply_button, name='click-apply-button'),  # 4번
]
    