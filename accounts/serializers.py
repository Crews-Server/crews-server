from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone 
from rest_framework import serializers

from apply.models import Apply
from post.models import Post, Like

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


class GetNormalUserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'sogang_mail', 'student_number', 'first_major', 'second_major', 'third_major', 'is_operator',]  
        # 나중에 'photo'도 추가!!


class GetAppliedListSerializer(serializers.ModelSerializer):
    crew_name = serializers.SerializerMethodField()
    button_status = serializers.SerializerMethodField()
    category_name = serializers.SerializerMethodField()
    class Meta:
        model = Post
        fields = ['id', 'crew', 'category_name', 'crew_name', 'title', 'apply_end_date', 'button_status',]

    def get_crew_name(self, obj):
        crew = obj.crew.crew_name
        return crew

    def get_button_status(self, obj):
        user = self.context.get('user') # user 받아오기
        now = timezone.now()

        try:
            apply = Apply.objects.get(user=user, post = obj)
        except ObjectDoesNotExist:
            return 0

        if now < obj.apply_end_date:
            return "지원서 수정하기"
        elif obj.apply_end_date <= now and now < obj.document_result_date: # 서류 마감시간부터 서류(1차) 합격자 발표시간 사이일 때
            return "지원 기간 아님"
        elif obj.document_result_date <= now and now < obj.final_result_date:  # 1차 발표부터 최종 2차(최종)발표 사이까지
            return "1차 결과 확인"
        elif obj.final_result_date <= now and apply.document_pass == True:  # 2차 발표 시간 이후이면서 1차 합격한 사람의 경우
            return "2차 결과 확인" 
        else:
            return "모집 종료"


    def get_category_name(self, obj):
        crew = obj.crew
        category = crew.category
        return category.category_name


class GetLikedPostSerializer(serializers.ModelSerializer):
    crew_name = serializers.SerializerMethodField()
    button_status = serializers.SerializerMethodField()
    category_name = serializers.SerializerMethodField()
    class Meta:
        model = Post
        fields = ['id', 'crew', 'category_name', 'crew_name', 'title', 'apply_end_date', 'button_status',]  
        # 동아리 이름, 지원서 마감 기한, 모집글 제목

    def get_crew_name(self, obj):
        return obj.crew.crew_name
    
    def get_button_status(self, obj):
        user = self.context.get('user')   # user 받아오기
        now = timezone.now()

        try:
            like = Like.objects.get(user=user, post = obj)
        except ObjectDoesNotExist:
            return 0
        
        try:
            apply = Apply.objects.get(user=user, post = obj)
        except ObjectDoesNotExist:
            # 찜은 했으나 아직 지원은 안 한 경우
            if now < obj.apply_end_date:
                return "지원하기"
            elif obj.apply_end_date <= now and now < obj.document_result_date:     # 서류 마감시간부터 서류(1차) 합격자 발표시간 사이일 때
                return "지원 기간 아님"
            else:
                return "모집 종료"

        # 찜도 하고 지원도 한 경우!
        if now < obj.apply_end_date:
            return "지원서 수정하기"
        elif obj.apply_end_date <= now and now < obj.document_result_date: # 서류 마감시간부터 서류(1차) 합격자 발표시간 사이일 때
            return "지원 기간 아님"
        elif obj.document_result_date <= now and now < obj.final_result_date:  # 1차 발표부터 최종 2차(최종)발표 사이까지
            return "1차 결과 확인"
        elif obj.final_result_date <= now and apply.document_pass == True:  # 2차 발표 시간 이후이면서 1차 합격한 사람의 경우
            return "2차 결과 확인" 
        else:
            return "모집 종료"


    def get_category_name(self, obj):
        crew = obj.crew
        category = crew.category
        return category.category_name


class GetCrewsPostsSerializer(serializers.ModelSerializer):
    crew_name = serializers.SerializerMethodField()
    category_name = serializers.SerializerMethodField()
    button_status = serializers.SerializerMethodField()
    class Meta:
        model = Post
        fields = ['id', 'crew', 'category_name', 'crew_name', 'title', 'apply_end_date', 'button_status',]

    def get_crew_name(self, obj):
        crew = obj.crew.crew_name
        return crew

    def get_button_status(self, obj):
        user = self.context.get('user') # user 받아오기
        now = timezone.now()

        if now < obj.apply_end_date:
            return "모집 공고 수정하기"
        elif obj.apply_end_date <= now and now < obj.document_result_date: # 서류 마감시간부터 서류(1차) 합격자 발표시간 사이일 때
            return "지원서 평가하기"
        elif obj.document_result_date <= now and now < obj.final_result_date:  # 1차 발표부터 최종 2차(최종)발표 사이까지
            return "최종 결과 입력하기"

        
    def get_category_name(self, obj):
        crew = obj.crew
        category = crew.category
        return category.category_name
