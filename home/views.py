from django.db.models import Q
from django.utils import timezone
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny

from .serializers import MainSerializer
from table.models import Post


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
        qs = super().get_queryset()

        categories = self.request.query_params.getlist('category')
        if categories:
            category_query = Q()
            for category in categories:
                category_query |= Q(crew__category__category_name=category, crew__category__isnull=False)
            qs = qs.filter(category_query)

        ordering = self.request.query_params.get('ordering', 'apply_end_date')
        if ordering == 'apply_end_date':
            return qs.filter(apply_end_date__gte=timezone.now().date()).order_by(ordering)
        return qs.order_by('-'+ordering)
