from rest_framework import serializers
from django.contrib.auth import get_user_model
from table.models import *
from django.core.exceptions import ObjectDoesNotExist

from django.utils import timezone  # now = timezone.now() 이렇게 사용하기

class GetMainPostsSerializer(serializers.ModelSerializer):
    # crew name
    crew_name = serializers.SerializerMethodField()
    # 모집마감 D-n 정보
    d_minus_info = serializers.SerializerMethodField()
    # 현재 찜한 사람 숫자 
    current_like_count = serializers.SerializerMethodField()
    # 이 동아리의 카테고리 정보 
    category = serializers.SerializerMethodField()
    # 해당 유저가 특정 post를 이미 찜 했는지 안 했는지 여부
    is_liked = serializers.SerializerMethodField()

    # crew image 추가해야!


    class Meta:
        model = Post
        fields = ['id', 'title', 'apply_end_date', 'crew_name', 'd_minus_info', 'current_like_count', 'category', 'is_liked']  
        # post 베너 사진 정보도 추가해야!

    def get_crew_name(self, obj):
        return obj.crew.crew_name
    

    def get_d_minus_info(self, obj):
        time_now = timezone.now()

        # apply_end_date 랑 time_now랑 비교하여 D-몇인지 알려주는 로직!
        delta = obj.apply_end_date - time_now

        days_remaining = delta.days
        if days_remaining < 0:
            return "이미 마감"
        elif days_remaining < 1:
            return "D-0"
        else:
            return f"D-{days_remaining}"
        

    def get_current_like_count(self, obj):

        post = obj

        likes = Like.objects.filter(post=post) 
        count = likes.count()
        return count
    
    def get_category(self, obj):
        return obj.crew.category.category_name
    
    def get_is_liked(self, obj):
        user = self.context.get('request').user  # context에서 request를 통해 user를 가져옴
        if user and not user.is_anonymous:
            # user가 로그인한 상태이면 '좋아요' 상태를 확인
            return Like.objects.filter(post=obj, user=user).exists()
        else:
            # 로그인하지 않은 사용자는 항상 False 반환
            return False







