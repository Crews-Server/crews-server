from django.urls import path, include
from .views import PostCreate, application_create

urlpatterns = [
    path('post/', PostCreate.as_view(), name='post-create'),
    path('application/', application_create, name='application-create')
]
