from rest_framework.pagination import CursorPagination
from rest_framework.response import Response


class HomeCursorPagination(CursorPagination):
    page_size = 6
    request_ordering = None

    def paginate_queryset(self, queryset, request, view=None):
        self.request_ordering = request.query_params.get('ordering', 'apply-end-date')
        self.request_ordering = self.request_ordering.replace('-', '_')
        return super().paginate_queryset(queryset, request, view)
    
    def get_ordering(self, request, queryset, view):
        return [self.request_ordering]
    
    def get_paginated_response(self, data):
        return Response({
            'has_next': self.get_next_link() is not None,
            'has_previous': self.get_previous_link() is not None,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data,
        })