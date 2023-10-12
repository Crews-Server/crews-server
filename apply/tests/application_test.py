from django.test import TestCase
from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework.test import APIClient
from table.models import Crew, Post, Section, LongSentence, CheckBox, CheckBoxOption, File, User, Administrator
from .test_constants import LONG_SENTENCE_CREATE_REQUEST, CHECKBOX_FILE_CREATE_REQUEST


# 지원서를 생성한다
class ApplicationCreateTest(TestCase):
    url = '/apply/application/'

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
        self.user = User.objects.create_user(email="test@naver.com", name="test user", password="1234")
        self.user.is_operator = True
        self.administrator = Administrator.objects.create(user=self.user, crew=self.crew)

    # 공통 섹션과 장문형 문항을 생성한다.
    def long_sentence_question_test(self):
        # given & when
        client = APIClient()
        client.force_authenticate(user=self.user)
        response = client.post(self.url,
                               data=LONG_SENTENCE_CREATE_REQUEST,
                               format='json')

        # then
        saved_section = get_object_or_404(Section, section_name=LONG_SENTENCE_CREATE_REQUEST["section_name"])
        saved_long_sentence1 = get_object_or_404(LongSentence, question=LONG_SENTENCE_CREATE_REQUEST["question"][0]["question"])
        saved_long_sentence2 = get_object_or_404(LongSentence, question=LONG_SENTENCE_CREATE_REQUEST["question"][1]["question"])

        self.assertEqual(response.status_code, 201)
        self.assertEqual(saved_section.post, self.post)
        self.assertEqual(saved_section.description, LONG_SENTENCE_CREATE_REQUEST["description"])
        self.assertEqual(saved_long_sentence1.section, saved_section)
        self.assertEqual(saved_long_sentence2.letter_count_limit, LONG_SENTENCE_CREATE_REQUEST["question"][1]["letter_count_limit"])

    # 객관식 문항(checkbox)과 파일 문항을 생성한다.
    def checkbox_file_question_test(self):
        # given & when
        client = APIClient()
        client.force_authenticate(user=self.user)
        response = client.post(self.url,
                               data=CHECKBOX_FILE_CREATE_REQUEST,
                               format='json')
        
        # then
        saved_checkbox = get_object_or_404(CheckBox, question=CHECKBOX_FILE_CREATE_REQUEST["question"][0]["question"])
        saved_options = get_list_or_404(CheckBoxOption, check_box=saved_checkbox)
        saved_file_question = get_object_or_404(File, question=CHECKBOX_FILE_CREATE_REQUEST["question"][1]["question"])
        self.assertEqual(response.status_code, 201)
        self.assertEqual(saved_checkbox.answer_minumum, CHECKBOX_FILE_CREATE_REQUEST["question"][0]["answer_minumum"])
        self.assertEqual(saved_options[0].option, CHECKBOX_FILE_CREATE_REQUEST["question"][0]["options"][0])
        self.assertEqual(saved_file_question.is_essential, CHECKBOX_FILE_CREATE_REQUEST["question"][1]["is_essential"])

# 지원서를 조회한다
class ApplicationReadTest(TestCase):
    url = '/apply/post/1/'
    
    def setUp(self):
        self.crew = Crew.objects.create(id=1, crew_name="0", description="0")
        self.post = create_post(self.crew)
        self.section1 = create_section(id=1, section_name="공통", post=self.post)
        self.section2 = create_section(id=2, section_name="백엔드", post=self.post)
        self.section3 = create_section(id=3, section_name="프론트엔드", post=self.post)
        self.section1_q1 = create_long_question("자기소개하세요.", 1, self.section1)
        self.section1_q2 = create_long_question("지원 동기를 써주세요.", 2, self.section1)
        self.section2_q1 = create_long_question("백엔드 관련 프로젝트 경험을 써주세요.", 1, self.section2)
        self.section2_q2 = create_checkbox_question("면접가능시간을 선택해주세요", 1, 2, 2, self.section2)
        self.section2_q2_o1 = create_option("오후 1시", self.section2_q2)
        self.section2_q2_o1 = create_option("오후 2시", self.section2_q2)
        self.section3_q1 = create_file_question("관련 포트폴리오를 제출해주세요", 1, self.section3)
        self.section3_q2 = create_checkbox_question("다른 동아리에서 비슷한 활동을 해 본 적 있나요?", 1, 1, 2, self.section3)
        self.section2_q2_o1 = create_option("예", self.section3_q2)
        self.section2_q2_o1 = create_option("아니오", self.section3_q2)
        self.section3_q3 = create_long_question("타 협업에서 소통 경험을 써주세요.", 3, self.section3)

        self.user = User.objects.create_user(email="test@naver.com", name="test user", password="1234")

    # 지원서를 섹션별로 조회한다
    def application_get_test(self):
        # given
        client = APIClient()
        client.force_authenticate(user=self.user)

        # when
        response = client.get(self.url, data={'section-id': 2})

        # then
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["공통"]["questions"]), 2)
        self.assertEqual(len(response.json()[self.section2.section_name]["questions"]), 2)
        self.assertLess(response.json()[self.section2.section_name]["questions"][0]["sequence"], 
                        response.json()[self.section2.section_name]["questions"][1]["sequence"])
        

# 테스트용 객체를 생성하는 함수들
def create_post(crew):
    return Post.objects.create(id=1,
                            apply_start_date="1000-01-01 00:00:00",
                            apply_end_date="1000-01-01 00:00:00",
                            document_result_date="1000-01-01 00:00:00",
                            has_interview=False,
                            requirement_target="0",
                            title="0",
                            content="0",
                            membership_fee="0",
                            crew=crew,
                            progress="0")

def create_section(id, section_name, post):
    return Section.objects.create(id=id,
                                  section_name=section_name,
                                  post=post,
                                  description="테스트용 섹션입니다.")

def create_long_question(content, sequence, section):
    return LongSentence.objects.create(question=content,
                                       letter_count_limit=500,
                                       is_essential=True,
                                       sequence=sequence,
                                       section=section)

def create_checkbox_question(content, answer_minumum, answer_maximum, sequence, section):
    return CheckBox.objects.create(question=content,
                                   is_essential=True,
                                   answer_minumum=answer_minumum,
                                   answer_maximum=answer_maximum,
                                   sequence=sequence,
                                   section=section)

def create_option(content, check_box):
    return CheckBoxOption.objects.create(option=content,
                                         check_box=check_box)

def create_file_question(question, sequence, section):
    return File.objects.create(question=question,
                               is_essential=True,
                               sequence=sequence,
                               section=section)