from django.db.models import Q
from django.utils import timezone
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from datetime import datetime

from .serializers import MainSerializer
from table.models import Post
from .paginations import HomeCursorPagination


# 메인 페이지 모집 공고 조회 api
class MainPost(ListAPIView):
    queryset = Post.objects.all()
    permission_classes = [AllowAny]
    serializer_class = MainSerializer
    filter_backends = [SearchFilter]
    search_fields = ['title', 'crew__crew_name']

    def get_queryset(self):
        qs = super().get_queryset().filter(apply_end_date__gte=timezone.now().date())

        # 상시 모집
        on_going = self.request.query_params.get('on-going', None)
        if on_going:
            qs = qs.filter(apply_end_date=datetime.max)

        # 카테고리 필터
        categories = self.request.query_params.getlist('category')
        if categories:
            category_query = Q()
            for category in categories:
                category_query |= Q(crew__category__category_name=category, crew__category__isnull=False)
            qs = qs.filter(category_query)

        return qs
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        paginator = HomeCursorPagination()
        paginated_queryset = paginator.paginate_queryset(queryset, request, view=self)

        if paginated_queryset is not None:
            serializer = self.get_serializer(paginated_queryset, many=True)
            return paginator.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


# 지원자 수가 많은 Hot 모집 공고 조회 api
'''
TODO: No-offset 페이지네이션 - 기획 회의 결과를 반영해야 한다.
'''
class HotPost(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = MainSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(apply_end_date__gte=timezone.now().date()).order_by('-applicants_count')