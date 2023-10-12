from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import (User, Category, Crew, Administrator, Post, PostImage, Apply, Like, Section, LongSentence, LongSentenceAnswer, CheckBox,
                    CheckBoxOption, CheckBoxAnswer, File, FileAnswer, Comment, Score)

# 회원가입할 때 쓰세요
# class UserRegisterSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only = True)

#     class Meta:
#         model = User
#         fields = ("id", "username", "password", "name", "sogang_mail", "student_number", "first_major", "second_major", "third_major",
#                 "is_operator")
        
#     def create(self, validated_data):
        
#         user = User.objects.create_user(
#             username = validated_data['username'],
#             passwprd = validated_data['password'],
#             name = validated_data['name'],
#             sogang_mail = validated_data['sogang_mail'],
#             student_number = validated_data['student_number'],
#             first_major = validated_data['first_major'],
#             second_major = validated_data.get('second_major', ''),
#             third_major = validated_data.get('third_major', ''),
#             is_operator = validated_data.get('is_operator', False)
#         )
#         return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'     

class CrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crew
        fields = '__all__'  

class AdministratorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Administrator
        fields = '__all__'   

class PostSerializer(serializers.ModelSerializer):
    total_likes = serializers.SerializerMethodField()    # 시리얼라이저 메서드 필드 사용
    total_applies = serializers.SerializerMethodField()  # 시리얼라이저 메서드 필드 사용
    class Meta:
        model = Post
        fields = ['id', 'apply_start_date', 'apply_end_date', 'document_result_date', 'has_interview', 'interview_start_date', 
                'interview_end_date', 'final_result_date', 'requirement_target', 'title', 'content', 'membership_fee', 'created_at', 
                'progress', 'image', 'total_likes', 'total_applies']
        
    def get_total_likes(self, obj):     # 시리얼라이저 메서드 필드에 저장될 value를 가져오기 위한 메서드 get_필드이름
        return obj.total_like_count()   # 여기서 obj는 현재 직렬화를 하려고 하는 Post의 그 객체를 의미
                                        # 여기서 return 하면 시리얼라이저 안에 있는 메서드 필드에 값이 저장!
    
    def get_total_applies(self, obj):  
        return obj.total_apply_count()

class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = '__all__'                   

class ApplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Apply
        fields = '__all__'

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'

class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = '__all__'

class LongSentenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = LongSentence
        fields = '__all__'

class LongSentenceAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = LongSentenceAnswer
        fields = '__all__'

class CheckBoxSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckBox
        fields = '__all__'

class CheckBoxOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckBoxOption
        fields = '__all__'

class CheckBoxAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckBoxAnswer
        fields = '__all__'

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = '__all__'

class FileAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileAnswer
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class ScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Score
        fields = '__all__'