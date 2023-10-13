from rest_framework import serializers
from django.contrib.auth import get_user_model
from table.models import *
from django.core.exceptions import ObjectDoesNotExist


class GetUserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'sogang_mail', 'student_number', 'first_major', 'second_major', 'third_major', 'is_operator',]  
        # 나중에 'photo'도 추가!!


# 2번 api 관련 시리얼라이저


# 3번 api 관련 시리얼라이저
class GetLikedPostSerializer(serializers.ModelSerializer):
    crew_name = serializers.SerializerMethodField()
    class Meta:
        model = Post
        fields = ['crew_name', 'apply_end_date', 'title']   
        # 동아리 이름, 지원서 마감 기한, 모집글 제목

    def get_crew_name(self, obj):
        return obj.crew.crew_name









