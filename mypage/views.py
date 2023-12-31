from table.models import *
from .serializers import *

from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist

from django.utils import timezone  # now = timezone.now() 이렇게 사용하기

# 1. 일반 User의 기본 정보 반환해주는 GET API
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_normal_user_info(request):   # post-man 테스트 완료
    user = request.user

    if user.is_operator == True:
        return Response({"error":"He is operator! not normal User!"}, status=status.HTTP_403_FORBIDDEN)  

    serializer = GetNormalUserInfoSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)


# 2번 관리자 User의 동아리 정보 반환해주는 GET API
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_operator_user_info(request):
    user = request.user

    if user.is_operator == False:
        return Response({"error":"He is not operator! just normal User!"}, status=status.HTTP_404_NOT_FOUND)

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



# 3. '일반 유저'의 마이페이지에서 자기가 지원한 동아리 지원서 리스트 반환해주는 GET api
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


# 4. '일반 유저'의 마이페이지에서 찜한 모집 공고 리스트 반환해주는 GET api
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

    serializer = GetLikedPostSerializer(post_list, many = True, context={'user':user})

    return Response(serializer.data, status=status.HTTP_200_OK)


# 5. '동아리 계정'의 마이페이지에서 자신들이 올린 모집 공고 리스트 반환해주는 GET api
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_crews_posts(request):
    user = request.user
    
    if user.is_operator != True:
        return Response({"error": "This User is not Crew's operator"}, status=status.HTTP_403_FORBIDDEN)

    try:
        administrator = Administrator.objects.get(user = user)
    except Administrator.DoesNotExist():
        pass

    crew = administrator.crew

    post_List = Post.objects.filter(crew = crew)

    if not post_List.exists(): #posts 리스트가 비어있을 때 -> 아직 공고를 올리지 않았음을 알려줘야!
        return Response({"message": "No posts found for this crew"}, status=status.HTTP_200_OK)
    
    serializer = GetCrewsPostsSerializer(post_List, many=True, context={'user':user})

    return Response(serializer.data, status=status.HTTP_200_OK)


# 6번 위의 1~5번까지 쪼개놓은 API 전부 하나로 합친 All-in-one 
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_all_mypage_info(request):
    user = request.user

    context = {}

    # 만약 이 사람이 동아리 관리자 계정이라면
    if user.is_operator == True:
        
        try:
            administrator = Administrator.objects.get(user=user)
        except Administrator.DoesNotExist:  # 관리자 계정이지만 연결된 동아리는 없는 경우
            return Response({"error":"He is operator but there is no linked Crew!"}, status=status.HTTP_404_NOT_FOUND) 

        
        # 동아리의 기본 정보 담기
        crew_info = {
            "crew_name" : administrator.crew.crew_name,
            "crew_description" : administrator.crew.description,
            "crew's_category" : administrator.crew.category.category_name,
            # 'crew_photo' : administrator.crew.photo,
        }

        # 해당 동아리의 Post 정보 가져오기!
        crew = administrator.crew
        post_List = Post.objects.filter(crew = crew)

        if not post_List.exists(): #posts 리스트가 비어있을 때 -> 아직 공고를 올리지 않았음을 알려줘야!
            return Response({"message": "No posts found for this crew"}, status=status.HTTP_200_OK)
        
        post_list_info = GetCrewsPostsSerializer(post_List, many=True, context={'user':user})

        context["crew_info"] = crew_info
        context["post_list_info"] = post_list_info.data

        context["is_operator"] = True

        return Response(context, status=status.HTTP_200_OK)


    # 만약 이 사람이 일반 유저라면
    else:
        
        # 유저의 기본 정보 가져오기
        user_nomal_info = GetNormalUserInfoSerializer(user)
        context["user_nomal_info"] = user_nomal_info.data # 위에서 정리한 정보 context에 담기!

        # 유저가 지원한 Post 리스트 가져오기
        apply = Apply.objects.filter(user=user)
        posts = [x.post for x in apply]  # apply에 연결되어있는 Post 객체들 다 담기!

        applied_list = GetAppliedListSerializer(posts, many=True, context={'user':user})
        context["applied_list"] = applied_list.data # 위에서 정리한 정보 context에 담기!

        # 유저가 찜한 Post 리스트 가져오기!
        liked = Like.objects.filter(user = user)
        post_list = [like.post for like in liked]

        liked_list = GetLikedPostSerializer(post_list, many = True, context={'user':user})
        context["liked_list"] = liked_list.data

        context["is_operator"] = False

        return Response(context, status=status.HTTP_200_OK)


# 7번 프로필 정보 수정하는 PATCH API (사진, 1전공, 2전공, 3전공)
@api_view(['PATCH'])
@permission_classes([permissions.IsAuthenticated])
def change_user_info(request):

    user = request.user

    # 관리자인 경우 (사진, 동아리 소개 한 문장 수정 가능)
    if user.is_operator == True: 
        pass


    # 일반 유저인 경우 (사진, 1전공, 2전공, 3전공)  
    else:
        pass









