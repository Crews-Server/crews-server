from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import (User, Category, Crew, Administrator, Post, PostImage, Apply, Like, Section, LongSentence, LongSentenceAnswer, CheckBox,
                    CheckBoxOption, CheckBoxAnswer, File, FileAnswer)

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
    class Meta:
        model = Post
        fields = '__all__'   

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
