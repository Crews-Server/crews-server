from django.conf import settings
from django.db import models

from post.models import Post, Section


class Apply(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="apply", on_delete=models.CASCADE
    )
    post = models.ForeignKey(Post, related_name="apply",
                             on_delete=models.CASCADE)
    apply_at = models.DateTimeField(auto_now=True)
    document_pass = models.BooleanField(
        default=False, null=True, blank=True
    )  # 서류 통과 여부, 기본값 False
    interview_date = models.DateTimeField(null=True, blank=True)  # 면접 날짜
    final_pass = models.BooleanField(
        default=False, null=True, blank=True
    )  # 최종합격 여부, 기본값 False
    score_avg = models.FloatField(default=0)

    # 면접 날짜 장소 시간 담는 변수 하나 생성

    def __str__(self):
        return f"{self.user} 의 {self.post} 지원"

    @classmethod
    def get_name(cls):
        return "지원"
    
    
class LongSentence(models.Model):
    question = models.CharField(max_length=300)  # ex) 지원자께서 지원하신 동기는 무엇인가요?
    letter_count_limit = models.IntegerField()  # 500자
    is_essential = models.BooleanField(default=True)  # 해당 타입이 필수적인지 아닌지 여부
    sequence = models.IntegerField(default=0)  # 문항 순서
    section = models.ForeignKey(
        Section, related_name="long_sentence", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"long sentence : {self.question}"
    
    @classmethod
    def get_name(cls):
        return "장문형 문항"


class LongSentenceAnswer(models.Model):
    long_sentence = models.ForeignKey(
        LongSentence, related_name="long_sentence_answer", on_delete=models.CASCADE
    )
    apply = models.ForeignKey(
        Apply, related_name="long_sentence_answer", on_delete=models.CASCADE
    )
    answer = models.TextField()

    @classmethod
    def get_name(cls):
        return "장문형 문항 답안"


class CheckBox(models.Model):
    question = models.CharField(max_length=300)
    is_essential = models.BooleanField(default=True)  # 해당 타입이 필수적인지 아닌지 여부
    answer_minumum = models.IntegerField(default=1)
    answer_maximum = models.IntegerField(default=1)
    sequence = models.IntegerField(default=0)  # 문항 순서
    section = models.ForeignKey(
        Section, related_name="check_box", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"check box : {self.question}"
    
    @classmethod
    def get_name(cls):
        return "체크박스 문항"


class CheckBoxOption(models.Model):
    option = models.CharField(max_length=200)
    check_box = models.ForeignKey(
        CheckBox, related_name="check_box_option", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.check_box}에 대한 보기 {self.option}"

    @classmethod
    def get_name(cls):
        return "체크박스 문항의 선택지"
    

class CheckBoxAnswer(models.Model):
    check_box = models.ForeignKey(
        CheckBox, related_name="check_box_answer", on_delete=models.CASCADE
    )
    apply = models.ForeignKey(
        Apply, related_name="check_box_answer", on_delete=models.CASCADE
    )
    answer = models.CharField(max_length=200)

    @classmethod
    def get_name(cls):
        return "체크박스 문항 답안"


class File(models.Model):
    question = models.CharField(max_length=300)
    is_essential = models.BooleanField(default=True)  # 해당 타입이 필수적인지 아닌지 여부
    sequence = models.IntegerField(default=0)  # 문항 순서
    section = models.ForeignKey(
        Section, related_name="file", on_delete=models.CASCADE)

    def __str__(self):
        return f"file : {self.question}"

    @classmethod
    def get_name(cls):
        return "파일 문항"


class FileAnswer(models.Model):
    file = models.ForeignKey(
        File, related_name="file_answer", on_delete=models.CASCADE)
    apply = models.ForeignKey(
        Apply, related_name="file_answer", on_delete=models.CASCADE
    )
    uploaded_file = models.FileField(upload_to='files/') 

    @classmethod
    def get_name(cls):
        return "파일 문항 답안"