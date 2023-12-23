from rest_framework import serializers

from .models import PostImage, Post
from accounts.models import Crew
from post.models import Like


class PostImageSerializer(serializers.ModelSerializer):
    post_image = serializers.ImageField(use_url=True)

    class Meta:
        model = PostImage
        fields = ['post_image']


class PostSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    thumbnail = serializers.SerializerMethodField()

    def get_images(self, obj):
        image = obj.post_image.all() 
        return PostImageSerializer(instance=image, many=True, context=self.context).data

    def get_thumbnail(self, obj):
        thumbnail = obj.post_image.filter(is_thumbnail=True).first()
        return PostImageSerializer(instance=thumbnail, context=self.context).data

    class Meta:
        model = Post
        exclude = ['pass_message', 'fail_message', 'created_at']

    def create(self, validated_data):
        instance = Post.objects.create(**validated_data)
        image_set = self.context['request'].FILES

        thumbnail_image = image_set.get('thumbnail')

        if thumbnail_image:
            PostImage.objects.create(post=instance, post_image=thumbnail_image, is_thumbnail=True)

        for image_data in image_set.getlist('image'):
            PostImage.objects.create(post=instance, post_image=image_data, is_thumbnail=False)
        return instance


class ThisCrewSerializers(serializers.ModelSerializer):
    crew_category = serializers.SerializerMethodField()
    class Meta:
        model = Crew
        fields = ['crew_name', 'description', 'crew_category']   
    
    def get_crew_category(self, obj):
        return obj.category.category_name


class ThisPostSerializers(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title']


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
            try:
                like = Like.objects.get(post=obj, user=user)
                return True
            except:
                return False
        else:
            # 로그인하지 않은 사용자는 항상 False 반환
            return False

    def get_image(self, obj):
        request = self.context.get('request')
        image_urls = []
        for img in obj.post_image.all():
            image_urls.append(request.build_absolute_uri(img.post_image.url))
        return image_urls











