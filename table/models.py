from django.db import models
from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


# 유저를 생성하는 매니저 클래스
class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(
        self,
        email,
        name,
        password,
        sogang_mail,
        student_number,
        first_major,
        **extra_fields,
    ):
        if not email:
            raise ValueError("must have user email(ID)")
        if not name:
            raise ValueError("must have user name")
        if not password:
            raise ValueError("must have user password")
        if not sogang_mail:
            raise ValueError("must have sogang_mail")
        if not student_number:
            raise ValueError("must have student_number")
        if not first_major:
            raise ValueError("must have first_major")

        email = self.normalize_email(email)
        sogang_mail = self.normalize_email(sogang_mail)

        user = self.model(
            email=email,
            name=name,
            sogang_mail=sogang_mail,
            student_number=student_number,
            first_major=first_major,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, name, password, **extra_fields):
        extra_fields.setdefault("sogang_mail", "default@sogang.ac.kr")
        extra_fields.setdefault("student_number", "00000000")
        extra_fields.setdefault("first_major", "None")

        user = self.create_user(
            email=self.normalize_email(email),
            name=name,
            password=password,
            **extra_fields,
        )

        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


# 재정의한 User
class User(AbstractBaseUser, PermissionsMixin):
    objects = UserManager()

    email = models.EmailField(max_length=100, unique=True)
    name = models.CharField(
        max_length=30, unique=True
    )  # 사용자의 이름 validators=[validate_unique_nickname]
    sogang_mail = models.CharField(max_length=100, unique=True)  # 서강 이메일
    student_number = models.CharField(max_length=100, unique=True)  # 학번 ex) 20201111
    first_major = models.CharField(max_length=50)  # 본전공
    second_major = models.CharField(max_length=50, null=True, blank=True)  # 2전공
    third_major = models.CharField(max_length=50, null=True, blank=True)  # 3전공
    is_operator = models.BooleanField(default=False)  # 기본값은 '학생 유저'
    photo = models.FileField(upload_to='images/', null=True, blank=True)   # 학생의 사진

    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "email"  # 기본적으로 username으로 사용할 필드를 email 필드로 수정

    REQUIRED_FIELDS = ["name"]  # User 객체 생성할 때 필수적으로 제공해야 하는 필드 리스트.

    def __str__(self):
        return f"{self.name} | {self.student_number} | {self.first_major}"


# 카테고리
class Category(models.Model):
    category_name = models.CharField(max_length=50)

    def __str__(self):
        return self.category_name


# 동아리
class Crew(models.Model):
    crew_name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    category = models.ForeignKey(Category, related_name="crew", on_delete=models.SET_NULL, null=True) 
    photo = models.FileField(upload_to='images/', null=True, blank=True)    # 동아리의 사진

    def __str__(self):
        return self.crew_name


# 운영자 관계 모델
class Administrator(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="administer", on_delete=models.CASCADE
    )
    crew = models.ForeignKey(Crew, related_name="administer", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user}는 {self.crew}의 운영자"


# 모집공고
class Post(models.Model):
    apply_start_date = models.DateTimeField()  # 서류 시작 날짜
    apply_end_date = models.DateTimeField()  # 서류 마감 날짜
    document_result_date = models.DateTimeField()  # 서류 발표 날짜
    has_interview = models.BooleanField(default=True)  # 면접 여부, 기본값 True
    interview_start_date = models.DateTimeField(null=True, blank=True)  # 면접 시작 날짜
    interview_end_date = models.DateTimeField(null=True, blank=True)  # 면접 종료 날짜
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

    def total_apply_count(self):  # 해당 Post에 연결된 apply들이 몇 개인지 계산해서 반환해주는 메서드
        return self.apply.count()  # related_name 'apply'를 사용함. 따라서 역참조 할 때 apply 이용!

    def total_like_count(self):  # 해당 Post에 연결된 Like들이 몇 개인지 계산해서 반환해주는 메서드
        return self.like.count()  # related_name 'like'를 사용함. 따라서 역참조 할 때 like 이용!

    def __str__(self):
        return self.title


# Post의 이미지
class PostImage(models.Model):
    post_image = models.FileField(upload_to='images/', null=True, blank=True) 
    post = models.ForeignKey(Post, related_name="post_image", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.post} 의 사진 {self.id}"


# 모집공고 지원
class Apply(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="apply", on_delete=models.CASCADE
    )
    post = models.ForeignKey(Post, related_name="apply", on_delete=models.CASCADE)
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
    
    
# 평가 모델
class Evaluation(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="evaluation"
    )
    apply = models.ForeignKey(
        Apply, on_delete=models.CASCADE, related_name="evaluation"
    )
    score = models.IntegerField()
    comment = models.TextField()

    def __str__(self):
        return f"Evaluation by {self.user.name} for {self.apply}"    


# 모집공고 찜하기
class Like(models.Model):
    user = models.ForeignKey(User, related_name="like", on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name="like", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} 의 {self.post} 찜"


# 모집공고 섹션
class Section(models.Model):
    section_name = models.CharField(max_length=50)  # 공통 , 백엔드, 프론트앤드, 기획/디자인
    post = models.ForeignKey(Post, related_name="section", on_delete=models.CASCADE)
    description = models.TextField()

    def __str__(self):
        return self.section_name


# 장문형
class LongSentence(models.Model):
    question = models.CharField(max_length=300)  # ex) 지원자께서 지원하신 동기는 무엇인가요?
    letter_count_limit = models.IntegerField()  # 500자
    is_essential = models.BooleanField(default=True)  # 해당 타입이 필수적인지 아닌지 여부
    section = models.ForeignKey(
        Section, related_name="long_sentence", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"long sentence : {self.question}"


# 장문형 문항에 대한 답
class LongSentenceAnswer(models.Model):
    long_sentence = models.ForeignKey(
        LongSentence, related_name="long_sentence_answer", on_delete=models.CASCADE
    )
    apply = models.ForeignKey(
        Apply, related_name="long_sentence_answer", on_delete=models.CASCADE
    )
    answer = models.TextField()


# 체크박스
class CheckBox(models.Model):
    question = models.CharField(max_length=300)
    is_essential = models.BooleanField(default=True)  # 해당 타입이 필수적인지 아닌지 여부
    answer_minumum = models.IntegerField(default=1)
    answer_maximum = models.IntegerField(default=1)
    section = models.ForeignKey(
        Section, related_name="check_box", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"check box : {self.question}"


# 체크박스의 선택지
class CheckBoxOption(models.Model):
    option = models.CharField(max_length=200)
    check_box = models.ForeignKey(
        CheckBox, related_name="check_box_option", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.check_box}에 대한 보기 {self.option}"


# 체크박스에 대한 답
class CheckBoxAnswer(models.Model):
    check_box = models.ForeignKey(
        CheckBox, related_name="check_box_answer", on_delete=models.CASCADE
    )
    apply = models.ForeignKey(
        Apply, related_name="check_box_answer", on_delete=models.CASCADE
    )
    answer = models.CharField(max_length=200)


# 파일
class File(models.Model):
    question = models.CharField(max_length=300)
    is_essential = models.BooleanField(default=True)  # 해당 타입이 필수적인지 아닌지 여부
    section = models.ForeignKey(Section, related_name="file", on_delete=models.CASCADE)

    def __str__(self):
        return f"file : {self.question}"


# 파일에 대한 답
class FileAnswer(models.Model):
    file = models.ForeignKey(File, related_name="file_answer", on_delete=models.CASCADE)
    apply = models.ForeignKey(
        Apply, related_name="file_answer", on_delete=models.CASCADE
    )
    uploaded_file = models.FileField(upload_to='files/') 


class Comment(models.Model):
    apply = models.ForeignKey(Apply, related_name="comment", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="comment", on_delete=models.CASCADE)


class Score(models.Model):
    apply = models.ForeignKey(Apply, related_name="score", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="score", on_delete=models.CASCADE)
    value = models.IntegerField(default=0)  # 디폴트 0으로 세팅



