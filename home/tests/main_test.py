from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient

from datetime import timedelta, datetime

from .utils import create_category, create_crew, create_post


# 메인 페이지에서 모집 공고 목록을 조회한다.
class MainTest(TestCase):
    url = '/home/'
    client = APIClient()

    def setUp(self):
        now = timezone.now().date()
        self.IT_CATEGORY = create_category(1, "IT")
        self.MARKETING_CATEGORY = create_category(2, "마케팅")
        self.LIKELION_CREW = create_crew(1, "멋쟁이사자처럼", self.IT_CATEGORY)
        self.CEOS_CREW = create_crew(2, "CEOS", self.MARKETING_CATEGORY)
        self.post1 = create_post(1, now, "신입부원을 모집합니다.", self.LIKELION_CREW)
        self.post2 = create_post(2, now+timedelta(days=8), "컴온", self.LIKELION_CREW)
        self.post3 = create_post(3, now+timedelta(days=9), "BE 신입부원 모집합니다.", self.CEOS_CREW)
        self.post4 = create_post(4, now+timedelta(days=-1), "FE 신입부원 모집합니다.", self.CEOS_CREW)
        self.post5 = create_post(5, datetime.max, "상시 모집합니다.", self.CEOS_CREW)

    # 모집 마감 순으로 모집 공고를 조회한다.
    def test_deadline_order(self):
        # given & when
        response = self.client.get(self.url)

        #then
        results = response.json()['results']
        d_day1 = results[0]['d_day'][2:]
        d_day2 = results[1]['d_day'][2:]
        d_day3 = results[2]['d_day'][2:]
        self.assertLess(d_day1, d_day2)
        self.assertLess(d_day2, d_day3)
        self.assertEqual(response.status_code, 200)

    # 모집 공고의 동아리 이름과 제목으로 검색한다.
    def test_search(self):
        # given & when
        params = {'search': 'CE'}
        response = self.client.get(self.url, data=params)

        # then
        results = response.json()['results']
        self.assertEqual(len(results), 2)
        self.assertEqual(response.status_code, 200)

    # 모집 공고를 필터 검색한다.
    def test_filter(self):
        # given & when
        params = {'category': ['마케팅']}
        response = self.client.get(self.url, data=params)

        # then
        results = response.json()['results']
        self.assertEqual(len(results), 2)
        self.assertEqual(response.status_code, 200)

    # 모집 공고를 키워드 검색과 필터 검색한다.
    def test_filter_search(self):
        # given & when
        params = {'category': ['IT'], 'search': '모집합니다'}
        response = self.client.get(self.url, data=params)

        # then
        results = response.json()['results']
        self.assertEqual(len(results), 1)
        self.assertEqual(response.status_code, 200)

    # 상시 모집인 모집 공고를 조회한다.
    def test_on_going_filter(self):
        # given & when
        params = {'on-going': "true"}
        response = self.client.get(self.url, data=params)

        # then
        results = response.json()['results']
        self.assertEqual(len(results), 1)
        self.assertEqual(response.status_code, 200)
