from rest_framework import serializers
from django.contrib.auth import get_user_model
from table.models import *
from django.core.exceptions import ObjectDoesNotExist

from django.utils import timezone  # now = timezone.now() 이렇게 사용하기

class GetNormalUserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'sogang_mail', 'student_number', 'first_major', 'second_major', 'third_major', 'is_operator',]  
        # 나중에 'photo'도 추가!!


# 3번 api 관련 시리얼라이저

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
        except:
            return 0

        if now < obj.apply_end_date:
            return "지원서 수정하기"
        elif obj.apply_end_date <= now and now < obj.document_result_date: # 서류 마감시간부터 서류(1차) 합격자 발표시간 사이일 때
            return "지원 기간 아님"
        elif obj.document_result_date <= now and now < obj.final_result_date:  # 1차 발표부터 최종 2차(최종)발표 사이까지
            return "1차 결과 확인"
        elif obj.final_result_date <= now and apply.document_pass == True:  # 2차 발표 시간 이후이면서 1차 합격한 사람의 경우
            return "2차 결과 확인" 
        
    def get_category_name(self, obj):
        crew = obj.crew
        category = crew.category
        return category.category_name




# 4번 api 관련 시리얼라이저
class GetLikedPostSerializer(serializers.ModelSerializer):
    crew_name = serializers.SerializerMethodField()
    button_status = serializers.SerializerMethodField()
    category_name = serializers.SerializerMethodField()
    class Meta:
        model = Post
        fields = ['id','crew_name', 'category_name', 'apply_end_date', 'title',]   
        # 동아리 이름, 지원서 마감 기한, 모집글 제목

    def get_crew_name(self, obj):
        return obj.crew.crew_name
    
    def get_category_name(self, obj):
        crew = obj.crew
        category = crew.category
        return category.category_name
    
# 5번 api 관련 시리얼라이저    
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







