from django.urls import path
from .views import MainPost, HotPost

urlpatterns = [
    path('', MainPost.as_view(), name="main-page"), # 모집 공고 필터 검색
    path('hot/', HotPost.as_view(), name="hot-post"), # Hot 모집 공고 조회
]
