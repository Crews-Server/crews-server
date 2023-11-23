from table.models import *
from .serializers import *

from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist

from django.utils import timezone  # now = timezone.now() 이렇게 사용하기


# 1. 동아리 정보 반환하는 api (GET), 이건 기본 정보 반환이라 로그인 유무 상관 없음.
# 동아리 이름, 동아리 한줄 소개, 동아리 프로필 사진, 동아리 카테고리 등의 정보 반환
# + 추가 -> 동아리 리쿠르팅 일정 정보도 같이 반환해서 주기
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_crew_info(request):
    # post-man 테스트 완료
    
    # post_title = request.GET.get('post_title')  # 클라이언트로부터 공고(Post)의 title을 전달 받음 (url 쿼리 파라미터로 넘김)
    # crew_name = request.GET.get('crew_name')  # 클라이언트로부터 crew의 이름 가져옴

    post_id = request.GET.get('post_id')

    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)
    
    crew = post.crew  # 해당 Post 객체에 연결되어있는 Crew 객체 반환

    context = {
        "crew_name" : crew.crew_name,
        "post_title" : post.title,
        "crew_description" : crew.description,
        "crew_photo" : crew.photo, 
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

    post_id = request.data.get('post_id')

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


# 3번 해당 Post의 기본 정보 반환하기
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def post_content(request):
    # post-man 테스트 완료

    post_id = request.GET.get('post_id')  # GET이니 쿼리 파라미터로 받기

    try:
        post = Post.objects.get(id = post_id)
    except Post.DoesNotExist:
        return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = PostContent_PostSerializer(post, context={'request': request})
    return Response(serializer.data, status=status.HTTP_200_OK)


# 4번 지원서 버튼 관련 api  (GET)
@api_view(['GET'])
@permission_classes([permissions.AllowAny])  # 로그인 제약 없음
def click_apply_button(request):
    user = request.user
    post_id = request.GET.get('post_id')  # GET이니 쿼리 파라미터로 받기

    try:
        post = Post.objects.get(id = post_id)
    except Post.DoesNotExist:
        return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)
    
    now = timezone.now() # 현재 시간 불러오기

    if not user.is_authenticated:   # 해당 유저가 로그인 하지 않고 들어온 눈팅 유저 일 때
        context = {"message": "He is not login user!",}
        if now < post.apply_end_date:
            context["button_status"] = "지원서 작성하기"
        else:
            context["button_status"] = "지원 기간 아님"

        return Response(context, status=status.HTTP_200_OK)

    # 만약 해당 User가 저 Post의 작성자라면 일반 유저와 달리 지원폼 수정하기, 지원폼 평가하기와 같은 것이 떠야 함
    if user.is_operator == True:
        try:
            admin = Administrator.objects.get(user=user, post=post)
            context = {
                "message": "He is This post's Administrator!",
                "button_status" : "지원폼 수정하기",
                # "additional_button" : "지원폼 평가하기"
            }
            return Response(context, status=status.HTTP_200_OK)
        except Administrator.DoesNotExist: # user가 운영진 계정이라 할지라도,해당 post 운영진 아니면 상관x 
            pass
    
    # 일반 유저이거나, 동아리 관리자여도 해당 Post를 올린 동아리의 관리자가 아닐 경우! 
    now = timezone.now() # 현재 시간 다시 불러오기(미세한 오차를 방지하기 위해 혹시 몰라 다시 불러옴)
    context = {"message": "He is general user!",}

    try:
        apply = Apply.objects.get(user=user, post=post)
    except Apply.DoesNotExist: # 해당 post에 지원 신청하지 않았을 때 
        if now < post.apply_end_date:
            context["button_status"]  = "지원서 작성하기"
        else:
            context["button_status"] = "지원 기간 아님"
        return Response(context, status=status.HTTP_200_OK)

    # apply가 존재할 때 => 로그인한 user가 해당 Post를 이미 지원 했을 때
    if now < post.apply_end_date:
        context["button_status"] = "지원서 수정하기"
    elif post.apply_end_date <= now and now < post.document_result_date: # 서류 마감시간부터 서류(1차) 합격자 발표시간 사이일 때
        context["button_status"] = "지원 기간 아님"
    elif post.document_result_date <= now and now < post.final_result_date:  # 1차 발표부터 최종 2차(최종)발표 사이까지
        context["button_status"] = "1차 결과 확인"
    elif post.final_result_date <= now and apply.document_pass == True:  # 2차 발표 시간 이후이면서 1차 합격한 사람의 경우
        context["button_status"] = "2차 결과 확인"  
    
    return Response(context, status=status.HTTP_200_OK)
