from table.models import *
from .serializers import *

from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist

from django.utils import timezone  # now = timezone.now() 이렇게 사용하기


# 1번. 로그인 상관없이 어떤 유저가 메인 페이지 접속하자마자 최신 마감 순으로 강좌들 6개 반환하는 GET api
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def normal_get_main(request):

    reference_time = timezone.now()  # 현재 시간 반환하기!
    
    # 현재시간 기준으로 apply_end_date이 greater than한 애들 filter로 불러오고! 빠른 순서대로 6개만 pick!
    recent_posts = Post.objects.filter(apply_end_date__gte=reference_time).order_by('apply_end_date')[:6]

    serializers = GetMainPostsSerializer(recent_posts, many=True, context={'request': request})

    return Response(serializers.data,status=status.HTTP_200_OK)


# 2번. 유저가 검색어를 입력하거나, 카테고리를 클릭할 때마다 이에 해당되는 post 리스트 반환하는 GET api
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def search_post(request):

    # 우선 첫 번쨰로 '검색어'를 전달받아야함! 검색어는 있을 수도 있고 , 없을 수도 있음
    search_query = request.query_params.get('query', None)  # 기본값 None

    # 클라이언트로부터 Post의 category들의 이름들을 리스트로 받아야 함! 
    category_names = request.query_params.getlist('categories', [])  # 기본값 [] 빈 리스트

    post_list_from_query = []
    post_list_from_category = []

    total_list = []

    # 경우1 : 검색어만 있는 경우! -> 단순 검색어 있는지 여부
    if search_query is not None and len(category_names) == 0:
        post = Post.objects.filter(title__icontains=search_query)
        for x in post:
            post_list_from_query.append(x)

        total_list = post_list_from_query   

    # 경우2 : 검색어 없이 카테고리 리스트만 있는 경우 -> 단순 합집합 출력
    elif search_query is None and len(category_names) != 0:
        for i in range(len(category_names)):
            this_name = category_names[i]
            
            try:
                cate = Category.objects.get(category_name = this_name)
            except ObjectDoesNotExist:
                pass  

            crew = Crew.objects.filter(category = cate)
            
            if not crew.exists():
                continue # 만약 해당 카테고리에 등록된 동아리/학회가 없으면 다음 카테고리로 컨티뉴
            
            for c in crew:
                this_crew_posts_list = Post.objects.filter(crew = c)

                if not this_crew_posts_list.exists():
                    continue # 만약 해당 동아리/학회가 등록한 Post가 아직 없을 때 다음 동아리/학회로 컨티뉴
                
                for post in this_crew_posts_list:
                    if post not in post_list_from_category: # queryset안에 해당 Post객체가 없을 때만 append!
                        post_list_from_category.append(post)    
        total_list = post_list_from_category

    # 경우3: 검색어도 있고, 카테고리도 있는 경우 -> 해당 카테고리 객체 중 -> 검색어 해당 안되는 것들 삭제
    elif search_query is not None and len(category_names) != 0:
        for i in range(len(category_names)):
            this_name = category_names[i]
            
            try:
                cate = Category.objects.get(category_name = this_name)
            except ObjectDoesNotExist:
                pass  

            crew = Crew.objects.filter(category = cate)
            
            if not crew.exists():
                continue # 만약 해당 카테고리에 등록된 동아리/학회가 없으면 다음 카테고리로 컨티뉴
            
            for c in crew:
                this_crew_posts_list = Post.objects.filter(crew = c)

                if not this_crew_posts_list.exists():
                    continue # 만약 해당 동아리/학회가 등록한 Post가 아직 없을 때 다음 동아리/학회로 컨티뉴
                
                for post in this_crew_posts_list:
                    if post not in post_list_from_category: # queryset안에 해당 Post객체가 없을 때만 append!
                        post_list_from_category.append(post)    
        
        # 쿼리로부터 얻은 post
        post = Post.objects.filter(title__icontains=search_query)
        for x in post:
            post_list_from_query.append(x)

        # 여기서 두 리스트 교집합 구하기!
        total_list = list(set(post_list_from_query) & set(post_list_from_category))

    # 경우 4: 둘다 없는 경우? -> 에러!
    else:
        return Response({"error": "Invalid request data"}, status=status.HTTP_400_BAD_REQUEST)
    
    

    


    serializers = GetMainPostsSerializer(total_list, many=True, context={'request': request}) # 직렬화

    return Response(serializers.data,status=status.HTTP_200_OK)               

