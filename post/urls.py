from django.urls import path, include
from .views import *

urlpatterns = [
    path('get-crew-info/', get_crew_info, name='get-crew-info'), # 1번
]
    