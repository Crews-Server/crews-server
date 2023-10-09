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
def get_user_info(request):
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



