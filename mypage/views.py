from table.models import *
from .serializers import *

from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist

from django.utils import timezone  # now = timezone.now() 이렇게 사용하기

# 1. User의 기본 정보 반환해주는 GET API
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_user_info(request):   # post-man 테스트 완료
    user = request.user

    if(user.is_operator == True): # 동아리 관계자 계정일 때
        try:
            administrator = Administrator.objects.get(user=user)
        except Administrator.DoesNotExist:
            return Response({"error":"He is operator but there is no linked Crew!"}, status=status.HTTP_404_NOT_FOUND)  

        context = {
            "crew_name" : administrator.crew.crew_name,
            "crew_description" : administrator.crew.description,
            "crew's_category" : administrator.crew.category.category_name,
            # 'crew_photo' : administrator.crew.photo,
        }

        return Response(context, status=status.HTTP_200_OK)

    else:  # 일반 유저 일 때
        serializer = GetUserInfoSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


# 2. '일반 유저'의 마이페이지에서 자기가 지원한 동아리 지원서 리스트 반환해주는 GET api
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_applied_list(request): 
    user = request.user

    if user.is_operator == True:
        return Response({"error": "He is Administrator, not general User!"}, status=status.HTTP_403_FORBIDDEN)

    apply = Apply.objects.filter(user=user)
    posts = [x.post for x in apply]  # apply에 연결되어있는 Post 객체들 다 담기!
    
    serializer = GetAppliedListSerializer(posts, many=True, context={'user':user})

    return Response(serializer.data, status=status.HTTP_200_OK)



# 3. '일반 유저'의 마이페이지에서 찜한 모집 공고 리스트 반환해주는 GET api
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_liked_post(request):
    user = request.user

    if user.is_operator == True:
        return Response({"error": "He is Administrator, not general User!"}, status=status.HTTP_403_FORBIDDEN)

    # 유저가 Like한 모든 객체 가져오기
    liked_list = Like.objects.filter(user = user)

    # 리스트 내에 Like 객체마다 연결된 Post 인스턴스 가져오기
    post_list = [like.post for like in liked_list]

    serializer = GetLikedPostSerializer(post_list, many = True)

    return Response(serializer.data, status=status.HTTP_200_OK)


# 4. '동아리 계정'의 마이페이지에서 자신들이 올린 모집 공고 리스트 반환해주는 GET api

