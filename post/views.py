from table.models import *
from .serializers import *

from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist

# 1. 동아리 정보 반환하는 api (GET), 이건 기본 정보 반환이라 로그인 유무 상관 없음.
# 동아리 이름, 동아리 한줄 소개, 동아리 프로필 사진, 동아리 카테고리 등의 정보 반환
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_crew_info(request):
    # post-man 테스트 완료
    
    # post_title = request.GET.get('post_title')  # 클라이언트로부터 공고(Post)의 title을 전달 받음 (url 쿼리 파라미터로 넘김)
    # crew_name = request.GET.get('crew_name')  # 클라이언트로부터 crew의 이름 가져옴

    post_id = request.GET.get('id')

    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)
    
    crew = post.crew  # 해당 Post 객체에 연결되어있는 Crew 객체 반환

    context = {
        "crew_name" : crew.crew_name,
        "post_title" : post.title,
        "crew_description" : crew.description,
        # "crew_photo" : crew.photo, 
        "category" : crew.category.category_name if crew.category else None, # 카테고리가 없으면 None으로 보내도록 분기 처리
    }

    return Response(context, status=status.HTTP_200_OK)


# 2. 유저가 해당 Post 찜 등록 or 해제 하기
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def like_post(request):

    user = request.user
    # post_title = request.data.get('post_title')  # 클라이언트로부터 공고(Post)의 title을 받음
    # crew_name = request.data.get('crew_name')  # 클라이언트로부터 crew의 이름 받음

    post_id = request.GET.get('id')

    if(user.is_operator == True):  
        return Response({"error": "He is Administrator, not general User!"}, status=status.HTTP_403_FORBIDDEN)
    
    try:
        post = Post.objects.get(id = post_id)
    except Post.DoesNotExist:
        return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)
    
    try:
        like = Like.objects.get(user=user, post=post)
    except Like.DoesNotExist:
        # 새로운 like 객체를 만들어야!
        new_like = Like(
            user = user,
            post = post
        )
        new_like.save()
        
        return Response({"message": "Like has been added."}, status=status.HTTP_201_CREATED)

    # 해당 like 객체를 삭제해야.
    like.delete()
    return Response({"message": "Like has been removed."}, status=status.HTTP_200_OK)






