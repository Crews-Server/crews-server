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