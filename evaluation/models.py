from django.conf import settings
from django.db import models

from apply.models import Apply


class Evaluation(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="evaluation"
    )
    apply = models.ForeignKey(
        Apply, on_delete=models.CASCADE, related_name="evaluation"
    )
    score = models.IntegerField()
    comment = models.TextField()

    def __str__(self):
        return f"Evaluation by {self.user.name} for {self.apply}"

    @classmethod
    def get_name(cls):
        return "평가"


class Comment(models.Model):
    apply = models.ForeignKey(
        Apply, related_name="comment", on_delete=models.CASCADE)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="comment", on_delete=models.CASCADE)
    
    @classmethod
    def get_name(cls):
        return "코멘트"


class Score(models.Model):
    apply = models.ForeignKey(
        Apply, related_name="score", on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="score",
                             on_delete=models.CASCADE)
    value = models.IntegerField(default=0)  # 디폴트 0으로 세팅

    @classmethod
    def get_name(cls):
        return "점수"