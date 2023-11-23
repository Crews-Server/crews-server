from django.urls import path, include
from .views import PostCreate, application_create, Appication, ApplyCreate

urlpatterns = [
    path('post/', PostCreate.as_view(), name='post-create'), # 모집 공고 생성(create)
    path('application/', application_create, name='application-create'), # 지원서 양식 생성(create)
    path('post/<int:post_id>/', Appication.as_view(), name='application'), # 지원서 양식 조회(get)
    path('', ApplyCreate.as_view(), name='apply'), # 지원서 작성(create)
]
