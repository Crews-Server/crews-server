from django.shortcuts import get_object_or_404
from django.test import TestCase
from rest_framework.test import APIClient

from apply.tests.common.generator import create_post, create_user
from table.models import Crew, Like

# 모집 공고를 찜한다.
class LikeTest(TestCase):
    url = '/post/1/like/'

    def setUp(self):
        self.LIKELION_CREW = Crew.objects.create(id=1, crew_name="멋쟁이사자처럼", description="0")
        self.POST = create_post(self.LIKELION_CREW)
        self.USER = create_user("1234@naver.com", "name", "password", "sogang@sogang.ac.kr", 20202020, "first_major")

    # 모집공고를 찜하여 STATUS 201을 반환한다.
    def test_create_like(self):
        # given & when
        client = APIClient()
        client.force_authenticate(user=self.USER)
        client.post(self.url)

        # then
        self.POST.refresh_from_db()
        self.assertEqual(self.POST.likes_count, 1)
        self.assertTrue(Like.objects.filter(user=self.USER, post=self.POST).exists())

    # 모집공고 찜을 취소하여 STATUS 200을 반환한다.
    def test_cancel_like(self):
        # given & when
        client = APIClient()
        client.force_authenticate(user=self.USER)
        client.post(self.url)
        client.post(self.url)

        # then
        self.POST.refresh_from_db()
        self.assertEqual(self.POST.likes_count, 0)
        self.assertFalse(Like.objects.filter(user=self.USER, post=self.POST).exists())
