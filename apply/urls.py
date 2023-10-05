from django.urls import path, include
from .views import PostCreate, application_create

urlpatterns = [
    path('', PostCreate.as_view(), name='post-create'),
    path('<int:post_id>/application/', application_create, name='application-create')
]
