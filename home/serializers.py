from django.utils import timezone
from rest_framework import serializers

from table.models import Post, PostImage, Like

class MainSerializer(serializers.ModelSerializer):
    crew_name = serializers.SerializerMethodField()
    crew_profile = serializers.SerializerMethodField()
    d_day = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    thumbnail = serializers.SerializerMethodField()

    def get_crew_name(self, obj):
        return obj.crew.crew_name
    
    def get_crew_profile(self, obj):
        if obj.crew.photo:
            return obj.crew.photo
        return None
    
    def get_d_day(self, obj):
        delta = obj.apply_end_date - timezone.now()
        days_remaining = delta.days+1

        if days_remaining < 0:
            return "마감"
        elif days_remaining < 1:
            return "D-0"
        else:
            return f"D-{days_remaining}"
    
    def get_like_count(self, obj):
        return obj.total_like_count()

    def get_category(self, obj):
        if obj.crew.category:
            return obj.crew.category.category_name
        return None
    
    def get_is_liked(self, obj):
        user = self.context.get('request').user
        if user and not user.is_anonymous:
            return Like.objects.filter(post=obj, user=user).exists()
        else:
            return False
        
    def get_thumbnail(self, obj):
        return PostImage.objects.filter(post=obj, is_thumbnail=True).first()

    class Meta:
        model = Post
        fields = ['id', 'title', 'crew_name', 'crew_profile', 'd_day', 'like_count', 'category', 'is_liked', 'thumbnail']
