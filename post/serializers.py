from rest_framework import serializers
from django.contrib.auth import get_user_model
from table.models import *
from django.core.exceptions import ObjectDoesNotExist

class PostContent_PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = "__all__"

class PostContent_PostSerializer(serializers.ModelSerializer):
    image = PostContent_PostImageSerializer(many=True, read_only = True)     # Post 모델의 related_name과 동일하게 설정

    class Meta:
        model = Post
        fields = ['id', 'apply_start_date', 'apply_end_date', 'document_result_date', 'has_interview', 'interview_start_date', 
                'interview_end_date', 'final_result_date', 'requirement_target', 'title', 'content', 'membership_fee', 'created_at', 
                'progress', 'image' ]

        












