from table.models import *
from .serializers import *

from django.contrib.auth import get_user_model

from rest_framework import generics, permissions, status

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist

# 여기 아래 두 줄에 노란색 밑줄 떠도 걱정 ㄴㄴ -> 잘 작동 됨.
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken

from django.utils import timezone  # now = timezone.now() 이렇게 사용하기


User = get_user_model()

class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [permissions.AllowAny]

class CustomTokenObtainPairView(TokenObtainPairView):
    pass