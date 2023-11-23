from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from .serializers import PostSerializer, SectionSerializer, LongSentenceSerializer, CheckBoxSerializer, FileSerializer, CheckBoxOptionSerializer
from .permissions import IsAdministrator

from table.models import Post, Administrator, Section, LongSentence, CheckBox, File, CheckBoxOption, Apply, LongSentenceAnswer, CheckBoxAnswer, FileAnswer


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
@permission_classes([IsAdministrator])
def application_create(request):

    try:
        post = Post.objects.get(id=request.data["post_id"])
    except Post.DoesNotExist:
        return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)
    
    administrator = Administrator.objects.get(user=request.user)
    if administrator.crew != post.crew:
        return Response({"error": "Request user is not Post's crew administrator"}, status=status.HTTP_403_FORBIDDEN)

    # section 저장
    section_serailizer = SectionSerializer(
        data={
            "section_name": request.data["section_name"],
            "post": request.data["post_id"],
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


# 모집 공고의 지원서 양식을 조회하는 api
class Appication(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, post_id, *args, **kwargs):
        
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)
        
        res = {}

        # 공통 section 문항 조회('section')
        common_section = Section.objects.get(post_id=post.id, section_name="공통")

        common_questions = LongSentenceSerializer(LongSentence.objects.filter(section=common_section), many=True).data
        common_questions = add_checkbox(CheckBox.objects.filter(section=common_section), common_questions)
        common_questions.extend(FileSerializer(File.objects.filter(section=common_section), many=True).data)
        
        common_questions = sorted(common_questions, key=lambda x: x.get('sequence', 0))

        res["공통"] = {"description": common_section.description,
                       "questions": common_questions}

        # section 별로 조회
        section_id = request.query_params.get('section-id')

        try:
            section = Section.objects.get(id=section_id)
        except Section.DoesNotExist:
            return Response({"error": "Section not found"}, status=status.HTTP_404_NOT_FOUND)
        
        section_questions = LongSentenceSerializer(LongSentence.objects.filter(section=section), many=True).data
        section_questions = add_checkbox(CheckBox.objects.filter(section=section), section_questions)
        section_questions.extend(FileSerializer(File.objects.filter(section=section), many=True).data)

        section_questions = sorted(section_questions, key=lambda x: x.get('sequence', 0))

        res[section.section_name] = {"description": section.description,
                                     "questions": section_questions}
        
        return Response(res, status=status.HTTP_200_OK)

# 체크 박스 문항 조회하기
def add_checkbox(checkbox_list, section_questions):
    index = 0
    for checkbox in CheckBoxSerializer(checkbox_list, many=True).data:
        checkbox["options"] = CheckBoxOptionSerializer(CheckBoxOption.objects.filter(check_box=checkbox_list[index]), many=True).data
        section_questions.append(checkbox)
        index += 1
    return section_questions


# 지원서를 작성하는 api
class ApplyCreate(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            post = Post.objects.get(id=request.data["post_id"])
        except Post.DoesNotExist:
            return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)
        
        apply = Apply.objects.create(user=request.user, post=post)

        for answer_dict in request.data["answers"]:
            question_type = answer_dict["type"]
            if(question_type == "long_sentence"):
                create_long_sentence_answer(answer_dict, apply)
            elif(question_type == "checkbox"):
                create_checkbox_answer(answer_dict, apply)
            elif(question_type == "file"):
                create_file_anwer(answer_dict, apply)
                
        return Response({"message": "Application is successed"}, status=status.HTTP_201_CREATED)

# 장문형 문항 답안 생성하기
def create_long_sentence_answer(answer_dict, apply):
    try:
        question = LongSentence.objects.get(id=answer_dict["question_id"])
    except LongSentence.DoesNotExist:
        return Response({"error": "LongSetence(id: "
                         + answer_dict["question_id"]
                         + ") not found"}, status=status.HTTP_404_NOT_FOUND)
    LongSentenceAnswer.objects.create(long_sentence=question, apply=apply, answer=answer_dict["content"])

# 체크박스 문항 답안 생성하기
def create_checkbox_answer(answer_dict, apply):
    try:
        question = CheckBox.objects.get(id=answer_dict["question_id"])
    except CheckBox.DoesNotExist:
        return Response({"error": "CheckBox(id: "
                         + answer_dict["question_id"]
                         + ") not found"}, status=status.HTTP_404_NOT_FOUND)
    CheckBoxAnswer.objects.create(check_box=question, apply=apply, answer=answer_dict["content"])

# 파일 문항 답안 생성하기
def create_file_anwer(answer_dict, apply):
    try:
        question = File.objects.get(id=answer_dict["question_id"])
    except File.DoesNotExist:
        return Response({"error": "File(id: "
                         + answer_dict["question_id"]
                         + ") not found"}, status=status.HTTP_404_NOT_FOUND)
    ## 파일 업로드 구현 안 됨
    FileAnswer.objects.create(file=question, apply=apply)