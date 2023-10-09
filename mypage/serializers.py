from rest_framework import serializers
from django.contrib.auth import get_user_model
from table.models import *
from django.core.exceptions import ObjectDoesNotExist


class GetUserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'first_major', 'second_major', 'third_major', 'email', 'student_number',]  # 나중에 'photo'도 추가!

    









