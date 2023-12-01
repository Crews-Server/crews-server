from django.shortcuts import get_object_or_404
from django.test import TestCase
from rest_framework.test import APIRequestFactory, APIClient

from ..permissions import IsAdministrator
from .common.generator import create_user
from .common.test_constants import POST_REQUEST, BAD_POST_REQUEST, ON_GOING_POST_REQUEST
from table.models import Crew, Post

from django.contrib.auth import get_user_model
User = get_user_model()


# 모집 공고를 생성한다
class PostCreateTest(TestCase):
    url = '/apply/post/'

    def setUp(self):
        self.crew = Crew.objects.create(id=1, crew_name="멋쟁이사자처럼",
                                        description="전국 연합 IT 동아리, 멋쟁이사자처럼입니다!")
        self.user = create_user(email="test@naver.com", name="test user", password="1234", sogang_mail="test", student_number="test", first_major="test")
        self.user.is_operator = True


    # 모집 공고를 생성하여 STATUS 201을 반환한다
    def test_post_create(self):
        # given
        client = APIClient()
        client.force_authenticate(user=self.user)

        # when
        response = client.post(self.url,
                               data=POST_REQUEST,
                               format='json')

        # then
        saved_post = get_object_or_404(Post, title=POST_REQUEST['title'])
        self.assertEqual(response.status_code, 201)
        self.assertEqual(saved_post.title, POST_REQUEST['title'])
        self.assertEqual(saved_post.crew.id, POST_REQUEST['crew'])


    # 잘못된 모집 공고 생성 요청으로 STATUS 400을 반환한다
    def test_no_interview_post_create(self):
        # given
        client = APIClient()
        client.force_authenticate(user=self.user)

        # when
        response = client.post(self.url,
                               data=BAD_POST_REQUEST,
                               format='json')

        # then
        self.assertEqual(response.status_code, 400)
        print(response.json())


    # 상시 모집 공고를 생성하여 STATUS 201을 반환한다
    def test_on_going_post_create(self):
        # given
        client = APIClient()
        client.force_authenticate(user=self.user)

        # when
        response = client.post(self.url,
                               data=ON_GOING_POST_REQUEST,
                               format='json')
        
        # then
        self.assertEqual(response.status_code, 201)

    # 동아리 운영진 권한을 갖는다
    def test_create_permission(self):
        # given
        factory = APIRequestFactory()
        request = factory.post(self.url,
                               data=POST_REQUEST,
                               format='json')
        request.user = self.user

        # when
        permission = IsAdministrator()
        has_permission = permission.has_permission(request, None)

        # then
        self.assertTrue(has_permission)
