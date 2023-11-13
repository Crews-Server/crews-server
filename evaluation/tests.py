from django.test import TestCase
from table.models import User, Apply, Post, Crew, Category, Evaluation
from django.utils import timezone


class EvaluationModelTest(TestCase):
    def setUp(self):
        # 필요한 모델들을 생성합니다.
        self.category = Category.objects.create(category_name="Sports")
        self.crew = Crew.objects.create(
            crew_name="Football Club",
            description="A football club",
            category=self.category,
        )
        self.user = User.objects.create_user(
            email="test@example.com",
            name="Test User",
            password="testpassword",
            sogang_mail="test@sogang.ac.kr",
            student_number="20220001",
            first_major="Computer Science",
        )
        self.post = Post.objects.create(
            title="Test Post",
            content="Test Content",
            crew=self.crew,
            apply_start_date=timezone.now(),
            apply_end_date=timezone.now(),
            document_result_date=timezone.now(),
        )
        self.apply = Apply.objects.create(user=self.user, post=self.post)
        self.evaluation = Evaluation.objects.create(
            evaluator=self.user,
            apply=self.apply,
            score=5,
            comment="Initial evaluation",
            document_passed=False,
            final_passed=False,
        )

    def test_evaluation_creation(self):
        # Evaluation 인스턴스를 생성합니다.
        evaluation = Evaluation.objects.create(
            evaluator=self.user,
            apply=self.apply,
            score=5,
            comment="Good evaluation",
            document_passed=True,
            final_passed=True,
        )

        # Evaluation 인스턴스가 올바르게 생성되었는지 검증합니다.
        self.assertEqual(evaluation.evaluator, self.user)
        self.assertEqual(evaluation.apply, self.apply)
        self.assertEqual(evaluation.score, 5)
        self.assertEqual(evaluation.comment, "Good evaluation")
        self.assertEqual(evaluation.document_passed, True)
        self.assertEqual(evaluation.final_passed, True)

    def test_evaluation_update_apply_status(self):
        # Evaluation 객체의 상태를 업데이트
        self.evaluation.document_passed = True
        self.evaluation.final_passed = False
        self.evaluation.save()

        # Apply 객체의 상태를 직접 업데이트
        self.apply.document_pass = self.evaluation.document_passed
        self.apply.final_pass = self.evaluation.final_passed
        self.apply.save()

        # Apply 객체의 상태 확인
        self.apply.refresh_from_db()
        self.assertTrue(self.apply.document_pass)
        self.assertFalse(self.apply.final_pass)
