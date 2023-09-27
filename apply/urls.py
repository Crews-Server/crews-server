from django.urls import path, include
from .views import PostCreate

urlpatterns = [
    path('', PostCreate.as_view(), name='post-create'),
]
