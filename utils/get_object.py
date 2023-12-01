from django.http import Http404
from rest_framework.generics import get_object_or_404

from config.exception.common_exception import NotFountExeption

def custom_get_object_or_404(queryset, *filter_args, **filter_kwargs):
    try:
        return get_object_or_404(queryset, *filter_args, **filter_kwargs)
    except Http404:
        raise NotFountExeption(queryset.get_name())