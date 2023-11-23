from rest_framework import serializers
from django.contrib.auth import get_user_model
from table.models import *
from django.core.exceptions import ObjectDoesNotExist

class PostContent_PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = "__all__"

class PostContent_PostSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()     # Post 모델의 related_name과 동일하게 설정
    total_likes = serializers.SerializerMethodField()
    total_applies = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    class Meta:
        model = Post
        fields = ['id', 'apply_start_date', 'apply_end_date', 'document_result_date', 'has_interview', 'interview_start_date', 
                'interview_end_date', 'final_result_date', 'requirement_target', 'title', 'content', 'membership_fee', 'created_at', 
                'progress', 'image', 'total_likes', 'total_applies', 'is_liked',]

    def get_total_likes(self, obj):
        return obj.total_like_count()
    
    def get_total_applies(self, obj):
        return obj.total_apply_count()
        
    def get_is_liked(self, obj):
        user = self.context.get('request').user  # context에서 request를 통해 user를 가져옴

        if user and not user.is_anonymous:
            # user가 로그인한 상태이면 '좋아요' 상태를 확인
            return Like.objects.filter(post=obj, user=user).exists()
        else:
            # 로그인하지 않은 사용자는 항상 False 반환
            return False

    def get_image(self, obj):
        request = self.context.get('request')
        image_urls = []
        for img in obj.post_image.all():
            image_urls.append(request.build_absolute_uri(img.post_image.url))
        return image_urls











