from django.conf import settings
from django.db import models

from accounts.models import Crew

class Post(models.Model):
    apply_start_date = models.DateTimeField()  # 서류 시작 날짜
    apply_end_date = models.DateTimeField()  # 서류 마감 날짜
    document_result_date = models.DateTimeField()  # 서류 발표 날짜
    has_interview = models.BooleanField(default=True)  # 면접 여부, 기본값 True
    interview_start_date = models.DateTimeField(
        null=True, blank=True)  # 면접 시작 날짜
    interview_end_date = models.DateTimeField(
        null=True, blank=True)  # 면접 종료 날짜
    final_result_date = models.DateTimeField(null=True, blank=True)  # 최종 발표 날짜
    requirement_target = models.TextField()  # 모집 대상 명시 텍스트
    title = models.CharField(max_length=200)  # 공고 제목
    content = models.TextField()  # 공고 내용
    membership_fee = models.CharField(max_length=200)  # 회비 내용
    crew = models.ForeignKey(
        Crew, related_name="post", on_delete=models.CASCADE
    )  # Crew의 FK
    created_at = models.DateTimeField(auto_now_add=True)  # 모집 공고 생성일
    progress = models.CharField(max_length=300)
    pass_message = models.CharField(max_length=500, null=True, blank=True)
    fail_message = models.CharField(max_length=500, null=True, blank=True)
    likes_count = models.IntegerField(default=0)
    applicants_count = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    @classmethod
    def get_name(cls):
        return "모집공고"


class PostImage(models.Model):
    post = models.ForeignKey(
        Post, related_name="post_image", on_delete=models.CASCADE)
    post_image = models.FileField(upload_to='images/', null=True, blank=True) 
    is_thumbnail = models.BooleanField()

    def __str__(self):
        return f"{self.post} 의 사진 {self.id}"

    @classmethod
    def get_name(cls):
        return "모집공고의 이미지"
    
class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="like",
                             on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name="like",
                             on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} 의 {self.post} 찜"

    @classmethod
    def get_name(cls):
        return "모집공고의 찜"
    
class Section(models.Model):
    section_name = models.CharField(max_length=50)  # 공통 , 백엔드, 프론트앤드, 기획/디자인
    post = models.ForeignKey(
        Post, related_name="section", on_delete=models.CASCADE)
    description = models.TextField()

    def __str__(self):
        return self.section_name
    
    @classmethod
    def get_name(cls):
        return "모집공고의 섹션"