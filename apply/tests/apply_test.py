from django.test import TestCase
from rest_framework.test import APIClient

from .common.generator import create_section, create_long_question, create_checkbox_question, create_file_question, create_user
from .common.test_constants import APPLY_REQUEST, INVALID_APPLY_REQUEST
from table.models import Crew, Post

# 일반 유저가 지원서를 작성한다
class ApplyCreateTest(TestCase):
    url = '/apply/'

    def setUp(self):
        self.crew = Crew.objects.create(id=1, crew_name="0", description="0")
        self.post = Post.objects.create(id=1,
                            apply_start_date="1000-01-01 00:00:00",
                            apply_end_date="1000-01-01 00:00:00",
                            document_result_date="1000-01-01 00:00:00",
                            has_interview=False,
                            requirement_target="0",
                            title="0",
                            content="0",
                            membership_fee="0",
                            crew=self.crew,
                            progress="0")
        self.user = create_user(email="test@naver.com", name="test user", password="1234", sogang_mail="test", student_number="test", first_major="test")
        self.section1 = create_section(id=1, section_name="공통", post=self.post)
        self.section1_q1 = create_long_question("자기소개하세요.", 1, self.section1)
        self.section2_q2 = create_checkbox_question("면접가능시간을 선택해주세요", 1, 2, 2, self.section1)
        self.section3_q1 = create_file_question("관련 포트폴리오를 제출해주세요", 1, self.section1)

    # 지원서를 작성하여 STATUS 201을 반환한다
    def test_apply(self):
        # given & when
        client = APIClient()
        client.force_authenticate(user=self.user)
        response = client.post(self.url,
                               data=APPLY_REQUEST,
                               format='json')
        
        # then
        self.assertEqual(response.status_code, 201)

    # 잘못된 지원서 생성 요청으로 STATUS 400을 반환한다
    def test_invalid_apply(self):
        # given & when
        client = APIClient()
        client.force_authenticate(user=self.user)
        response = client.post(self.url,
                               data=INVALID_APPLY_REQUEST,
                               format='json')
        # then
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["detail"], "잘못된 지원서 작성 요청입니다.")