from rest_framework import serializers
from django.contrib.auth import get_user_model
from table.models import *
from django.core.exceptions import ObjectDoesNotExist

User = get_user_model()

class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password', 'name', 'sogang_mail', 'student_number', 'first_major', 'second_major', 'third_major']
        # email password name sogang_mail student_number first_major 속성들은 필수적으로 요청
        # second_major third_major 속성은 입력 안 하면 자동 NULL 값으로 처리.
        extra_kwargs = {
            'email' : {"required" : True},
            'name' : {"required" : True},
            'sogang_mail' : {"required" : True},
            'student_number' : {"required" : True},

            'password': {'write_only': True}, # 비밀번호와 같은 민감한 필드 숨기기
            
            'first_major' : {"required" : True},
            'second_major': {'required': False, 'allow_blank': True},
            'third_major': {'required': False, 'allow_blank': True},

        }

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # 사용자 정보 추가
        token['name'] = user.name
        token['student_number'] = user.student_number
        token['is_operator'] = user.is_operator
        
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        
        # validate 메소드가 반환하는 데이터에 사용자 정보 추가
        data.update({'name': self.user.name})
        data.update({'student_number': self.user.student_number})
        data.update({'is_operator': self.user.is_operator})

        return data








