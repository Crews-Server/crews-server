from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Evaluation

User = get_user_model()

class EvaluationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evaluation
        fields = "__all__"


class GetAppliedUserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "name",
            "student_number",
            "first_major",
            "second_major",
            "third_major",
        ]
