from django.shortcuts import render
from rest_framework import viewsets
from table.models import *  # table 모델에서 Evaluation import
from .serializers import *
from apply.permissions import IsAdministrator
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions, status
from rest_framework.response import Response


class EvaluationViewSet(viewsets.ModelViewSet):
    queryset = Evaluation.objects.all()
    serializer_class = EvaluationSerializer
    permission_classes = [IsAdministrator]

    def perform_create(self, serializer):
        serializer.save(evaluator=self.request.user)

    def perform_update(self, serializer):
        evaluation = serializer.save()  # Evaluation 객체 저장
        apply_instance = evaluation.apply  # 관련된 Apply 인스턴스 가져오기

        # Evaluation의 결과에 따라 Apply의 상태 업데이트
        if evaluation.document_passed:
            apply_instance.document_pass = True
            if evaluation.final_passed:
                apply_instance.final_pass = True
            else:
                apply_instance.final_pass = False
        else:
            apply_instance.document_pass = False

        apply_instance.save()  # Apply 객체 업데이트


# 1번. 이 Post 지원한 지원자들의 기본정보 리스트로 반환하기 (GET) (ok)
@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])  # 로그인 되어 있어야 하는 제약
def get_applied_user_list(request):
    user = request.user  # 관리자
    post_id = request.GET.get("post_id")  # GET이니 쿼리 파라미터로 받기, post의 id를 클라이언트로부터 받기!

    try:
        post = Post.objects.get(id=post_id)
    except:
        pass

    crew = post.crew
    # 지금 접속한 사람이 해당 포스트 올린 동아리 소속 관리자인지 체크해야!
    try:
        administrator = Administrator.objects.get(user=user, crew=crew)
    except Administrator.Doesnotexist():
        return Response(
            {"error": "이 관리자는 해당 post를 올린 crew의 관리자 아님!"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    apply = Apply.objects.filter(post=post)  # [] 로 반환

    if not apply.exists():  # 해당 Post에 지원자가 아무도 없을 때
        return Response(
            {"message": "There is No any applyer"}, status=status.HTTP_200_OK
        )

    # 지원자가 있는거자나!
    user_list = []
    for x in apply:
        user_list.append(x.user)

    serializer = GetAppliedUserListSerializer(user_list, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)


# 2번. 1차 합격한 애들 명수 알려주기 (GET)  - 회의 후 결정
@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def get_document_pass_count(request):
    post_id = request.GET.get("post_id")

    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)

    document_pass_count = Apply.objects.filter(post=post, document_pass=True).count()

    return Response(
        {"document_pass_count": document_pass_count}, status=status.HTTP_200_OK
    )


# 3번. 특정 유저 클릭했을 때 그 사람이 받은 평균점수랑, 각각이 부여한 점수랑, 상위 몇 퍼인지 반환(GET)
@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def get_user_evaluation(request):
    user_id = request.GET.get("user_id")

    try:
        evaluations = Evaluation.objects.filter(apply__user__id=user_id)
    except Evaluation.DoesNotExist:
        return Response(
            {"error": "Evaluations not found"}, status=status.HTTP_404_NOT_FOUND
        )

    if not evaluations.exists():
        return Response(
            {"message": "No evaluations found for this user"},
            status=status.HTTP_404_NOT_FOUND,
        )

    total_score = sum(evaluation.score for evaluation in evaluations)
    average_score = total_score / evaluations.count()
    evaluation_data = [
        {"evaluator": evaluation.user.name, "score": evaluation.score}
        for evaluation in evaluations
    ]

    return Response(
        {"average_score": average_score, "evaluations": evaluation_data},
        status=status.HTTP_200_OK,
    )


# 4번. 특정 유저 클릭했을 때 그 사람이 받은 평균점수랑, 각각이 부여한 점수랑, 한 줄평,  상위 몇 퍼인지 반환(GET)


# # 5번. 어떤 사람 1차 합격시키기 or 취소시키기 (POST) (ok) - 버튼 분리
# @api_view(["POST"])
# @permission_classes([permissions.IsAuthenticated])
# def document_pass_post(request):
#     user = request.user  # 로그인한 관리자
#     post_id = request.data.get("post_id")  # POST요청 일때 바디로부터 받아오는 방법
#     applicant_id = request.data.get("applicant_id")  # 지원자 아이디!

#     try:
#         applicant = User.objects.get(id=applicant_id)
#     except:
#         pass

#     try:
#         post = Post.objects.get(id=post_id)
#     except:
#         pass

#     try:
#         apply = Apply.objects.get(user=applicant, post=post)
#     except:
#         return Response(
#             {"error": "해당 지원자는 이 Post지원한 것 아님!"}, status=status.HTTP_400_BAD_REQUEST
#         )

#     if apply.document_pass == False:
#         apply.document_pass = True
#         apply.save()
#         return Response({"message": "해당 지원자 1차 합격시킴!!"}, status=status.HTTP_200_OK)
#     else:  # True 였으면
#         apply.document_pass = False
#         apply.save()
#         return Response({"message": "해당 지원자 1차 합격 취소시킴!!"}, status=status.HTTP_200_OK)


# 5-1번. 어떤 사람 1차 합격시키기 (POST)
@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def set_document_pass(request):
    user = request.user  # 로그인한 관리자
    post_id = request.data.get("post_id")
    applicant_id = request.data.get("applicant_id")

    try:
        applicant = User.objects.get(id=applicant_id)
        post = Post.objects.get(id=post_id)
        apply = Apply.objects.get(user=applicant, post=post)
    except (User.DoesNotExist, Post.DoesNotExist, Apply.DoesNotExist):
        return Response(
            {"error": "Invalid request data"}, status=status.HTTP_400_BAD_REQUEST
        )

    apply.document_pass = True
    apply.save()
    return Response({"message": "1차 합격 처리되었습니다."}, status=status.HTTP_200_OK)


# 5-2번. 어떤 사람 1차 합격 취소시키기 (POST)
@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def unset_document_pass(request):
    user = request.user  # 로그인한 관리자
    post_id = request.data.get("post_id")
    applicant_id = request.data.get("applicant_id")

    try:
        applicant = User.objects.get(id=applicant_id)
        post = Post.objects.get(id=post_id)
        apply = Apply.objects.get(user=applicant, post=post)
    except (User.DoesNotExist, Post.DoesNotExist, Apply.DoesNotExist):
        return Response(
            {"error": "Invalid request data"}, status=status.HTTP_400_BAD_REQUEST
        )

    apply.document_pass = False
    apply.save()
    return Response({"message": "1차 합격이 취소되었습니다."}, status=status.HTTP_200_OK)


# # 6번. 어떤 사람 최종 합격시키기 or 최종합격 취소시키기 (POST) (ok) - 버튼분리
# @api_view(["POST"])
# @permission_classes([permissions.IsAuthenticated])
# def final_pass_post(request):
#     user = request.user  # 로그인한 관리자
#     post_id = request.data.get("post_id")  # POST요청 일때 바디로부터 받아오는 방법
#     applicant_id = request.data.get("applicant_id")  # 지원자 아이디!

#     try:
#         applicant = User.objects.get(id=applicant_id)
#     except:
#         pass

#     try:
#         post = Post.objects.get(id=post_id)
#     except:
#         pass

#     try:
#         apply = Apply.objects.get(user=applicant, post=post)
#     except:
#         return Response(
#             {"error": "해당 지원자는 이 Post지원한 것 아님!"}, status=status.HTTP_400_BAD_REQUEST
#         )

#     if apply.final_pass == False:
#         apply.final_pass = True
#         apply.save()
#         return Response({"message": "해당 지원자 최종합격시킴!!"}, status=status.HTTP_200_OK)
#     else:  # True 였으면
#         apply.final_pass = False
#         apply.save()
#         return Response({"message": "해당 지원자 최종합격 취소시킴!!"}, status=status.HTTP_200_OK)


# 6-1번. 어떤 사람 최종 합격시키기 (POST)
@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def set_final_pass(request):
    user = request.user  # 로그인한 관리자
    post_id = request.data.get("post_id")
    applicant_id = request.data.get("applicant_id")

    try:
        applicant = User.objects.get(id=applicant_id)
        post = Post.objects.get(id=post_id)
        apply = Apply.objects.get(user=applicant, post=post)
    except (User.DoesNotExist, Post.DoesNotExist, Apply.DoesNotExist):
        return Response(
            {"error": "Invalid request data"}, status=status.HTTP_400_BAD_REQUEST
        )

    apply.final_pass = True
    apply.save()
    return Response({"message": "최종 합격 처리되었습니다."}, status=status.HTTP_200_OK)


# 6-2번. 어떤 사람 최종 합격 취소시키기 (POST)
@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def unset_final_pass(request):
    user = request.user  # 로그인한 관리자
    post_id = request.data.get("post_id")
    applicant_id = request.data.get("applicant_id")

    try:
        applicant = User.objects.get(id=applicant_id)
        post = Post.objects.get(id=post_id)
        apply = Apply.objects.get(user=applicant, post=post)
    except (User.DoesNotExist, Post.DoesNotExist, Apply.DoesNotExist):
        return Response(
            {"error": "Invalid request data"}, status=status.HTTP_400_BAD_REQUEST
        )

    apply.final_pass = False
    apply.save()
    return Response({"message": "최종 합격이 취소되었습니다."}, status=status.HTTP_200_OK)


# 7번. 어떤 사람의 '지원서 확인하기'눌렀을 때 그 사람이 쓴 지원서 가져오는 Api (GET)
@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def get_user_applications(request):
    user_id = request.GET.get("user_id")
    post_id = request.GET.get("post_id")

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)

    try:
        apply = Apply.objects.get(user=user, post=post)
    except Post.DoesNotExist:
        return Response(
            {"error": "No applications found for this user"},
            status=status.HTTP_404_NOT_FOUND,
        )

    # 전체 다 담아서 반환해줄 빈 딕셔너리 만들기
    context = {}

    # 장문형 질문 답변 가져오기
    longsentence_answer = LongSentenceAnswer.objects.filter(apply=apply)
    longsentence_question = []

    if not longsentence_answer.exists():  # 비어있을 때
        pass
    else:  # 비어있지 않을 때
        for x in longsentence_answer:
            longsentence_question.append(x.long_sentence)

    Sentence_answer_dic = {}

    for i in range(len(longsentence_answer)):
        temp_list = [
            longsentence_question[i].section.section_name,
            longsentence_question[i].question,
            longsentence_question[i].letter_count_limit,
            longsentence_answer[i].answer,
        ]
        Sentence_answer_dic[i + 1] = temp_list

    context["longsentence"] = Sentence_answer_dic  # 맵 안에 맵을 넣는다!

    # 체크박스 질문 옵션 답변 가져오기

    checkbox_answers = CheckBoxAnswer.objects.filter(apply=apply)
    checkbox_questions = []

    if not checkbox_answers.exists():
        pass
    else:
        for x in checkbox_answers:
            checkbox_questions.append(x.check_box)

    checkbox_options = []
    for checkbox in checkbox_questions:
        checkbox_options.append(checkbox.check_box_option.all())

    check_box_dic = {}

    for i in range(len(checkbox_questions)):
        temp_list = []

        section_qustion = {
            "section": checkbox_questions[i].section.section_name,
            "객관식 질문": checkbox_questions[i].question,
        }
        temp_list.append(section_qustion)

        for y in range(len(checkbox_options[i])):
            string = "객관식 후보" + str(y + 1)
            options = {
                string: checkbox_options[i][y].option,
            }
            temp_list.append(options)

        users_answer = {"사용자의 답": checkbox_answers[i].answer}

        temp_list.append(users_answer)
        check_box_dic[i + 1] = temp_list

    context["checkbox"] = check_box_dic

    # 파일 질문 - 답 가져오기
    file_answer = FileAnswer.objects.filter(apply=apply)
    file_question = []

    if not file_answer.exists():  # 비어있을 때
        pass
    else:  # 비어있지 않을 때
        for x in file_answer:
            file_question.append(x.file)

    file_answer_dic = {}

    for i in range(len(file_answer)):
        temp_list = [
            file_question[i].section.section_name,
            file_question[i].question,
        ]  # 여기에 나중에 File 링크 담도록 수정!
        file_answer_dic[i + 1] = temp_list

    context["file"] = file_answer_dic  # 맵 안에 맵을 넣는다!

    return Response(context, status=status.HTTP_200_OK)


# 8번. 로그인한 관리자가 부여한(or 안 한) 지원자에 대한 점수랑 한 줄평 반환 + 1차합격/취소시키기/최종합격~그 버튼 상태 (GET)
@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def get_admin_evaluation_status(request):
    user_id = request.GET.get("user_id")

    admin_user = request.user
    try:
        evaluation = Evaluation.objects.get(user=admin_user, apply__user__id=user_id)
    except Evaluation.DoesNotExist:
        return Response(
            {"error": "Evaluation not found"}, status=status.HTTP_404_NOT_FOUND
        )

    apply_instance = evaluation.apply
    evaluation_status = {
        "score": evaluation.score,
        "comment": evaluation.comment,
        "document_pass": apply_instance.document_pass,
        "final_pass": apply_instance.final_pass,
    }

    return Response(evaluation_status, status=status.HTTP_200_OK)


# 9번. 어떤 사람의 지원서 보면서, 관리자가 점수랑 한줄평 입력하는 api (PATCH)
@api_view(["PATCH"])
@permission_classes([permissions.IsAuthenticated])
def update_evaluation(request):
    evaluation_id = request.GET.get("evaluation_id")

    try:
        evaluation = Evaluation.objects.get(id=evaluation_id, user=request.user)
    except Evaluation.DoesNotExist:
        return Response(
            {"error": "Evaluation not found"}, status=status.HTTP_404_NOT_FOUND
        )

    score = request.data.get("score")
    comment = request.data.get("comment")

    if score is not None:
        evaluation.score = score
    if comment is not None:
        evaluation.comment = comment

    evaluation.save()
    return Response(
        {"message": "Evaluation updated successfully"}, status=status.HTTP_200_OK
    )
