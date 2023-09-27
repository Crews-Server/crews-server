from rest_framework import generics
from .serializers import PostSerializer
from .permissions import IsAdministrator

# 모집 공고를 생성하는 api
class PostCreate(generics.CreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAdministrator]