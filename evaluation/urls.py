from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EvaluationViewSet

router = DefaultRouter()
router.register(r"evaluations", EvaluationViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
