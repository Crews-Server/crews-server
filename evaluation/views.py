from django.shortcuts import render
from rest_framework import viewsets
from table.models import Evaluation, Apply  # table 모델에서 Evaluation import
from .serializers import EvaluationSerializer
from apply.permissions import IsAdministrator


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
