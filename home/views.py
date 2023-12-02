from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .serializers import MainSerializer
from table.models import Post, Category, Crew


# 메인 페이지 조회 api
'''
Todo: No-offset 페이지네이션
'''
class Main(ListAPIView):
    queryset = Post.objects.all()
    permission_classes = [AllowAny]
    serializer_class = MainSerializer
    filter_backends = [SearchFilter]
    search_fields = ['title', 'crew__crew_name']

    def get_queryset(self):
        ordering = self.request.query_params.get('ordering', 'apply_end_date')
        qs = super().get_queryset()
        if ordering == 'apply_end_date':
            return qs.filter(apply_end_date__gte=timezone.now().date()).order_by(ordering)
        return qs.order_by('-'+ordering)
