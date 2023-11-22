from django.urls import path, include
from .views import *

urlpatterns = [
    path('normal-get-main/', normal_get_main, name="normal-get-main"), # 1번
    path('search-post/', search_post, name="search-post"), # 2번
]
