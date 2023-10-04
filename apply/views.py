from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import PostSerializer, SectionSerializer, LongSentenceSerializer, CheckBoxSerializer, FileSerializer, CheckBoxOptionSerializer
from .permissions import IsAdministrator

from table.models import Post


# 모집 공고를 생성하는 api
class PostCreate(generics.CreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAdministrator]


# section 별로 지원서 문항을 생성하는 api
"""
request body
- section_name
- section_description
- question
    - type
    - is_essential
    - question
    ...
"""
@api_view(['POST'])
def application_create(request, post_id):

    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)

    # section 저장
    section_serailizer = SectionSerializer(
        data={
            "section_name": request.data["section_name"],
            "post": post_id,
            "description": request.data["description"]
        }
    )

    if section_serailizer.is_valid(raise_exception=True):
        saved_section = section_serailizer.save()


    # 문항 저장
    for question_dict in request.data["question"]:
        question_dict["section"] = saved_section.id

        # 장문형 문항 저장
        if question_dict["type"] == "long_sentence":
            serializer = LongSentenceSerializer(data=question_dict)

            if serializer.is_valid(raise_exception=True):
                saved = serializer.save()

        # 객관식 문항 저장
        elif question_dict["type"] == "checkbox":
            option_list = question_dict["options"]
            serializer = CheckBoxSerializer(data=question_dict)

            if serializer.is_valid(raise_exception=True):
                saved = serializer.save()

            # 객관식 문항의 선택지 저장하기
            for option in option_list:
                option_serializer = CheckBoxOptionSerializer(
                    data={"option": option, "check_box": saved.id})
                if option_serializer.is_valid(raise_exception=True):
                    option_serializer.save()

        # 파일 문항 저장
        elif question_dict["type"] == "file":
            serializer = FileSerializer(data=question_dict)

            if serializer.is_valid(raise_exception=True):
                saved = serializer.save()

    return Response({"message": "Application is created"}, status=status.HTTP_201_CREATED)
