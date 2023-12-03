from django.db.models import Q
from django.utils import timezone
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny

from datetime import datetime

from .serializers import MainSerializer
from table.models import Post


# 메인 페이지 모집 공고 조회 api
'''
TODO: No-offset 페이지네이션
'''
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

        # 정렬
        ordering = self.request.query_params.get('ordering', 'apply-end-date')
        ordering = ordering.replace('-', '_')
        if ordering == 'apply_end_date':
            return qs.order_by(ordering)
        return qs.order_by('-'+ordering)


# 지원자 수가 많은 Hot 모집 공고 조회 api
'''
TODO: No-offset 페이지네이션
'''
class HotPost(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = MainSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(apply_end_date__gte=timezone.now().date()).order_by('-applicants_count')