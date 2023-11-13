from rest_framework import serializers
from table.models import Evaluation  # table 모델에서 Evaluation import


class EvaluationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evaluation
        fields = "__all__"
