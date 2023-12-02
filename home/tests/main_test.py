from django.db.models import Q
from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient

from datetime import timedelta

from table.models import Post, Crew, Category


# 메인 페이지에서 모집 공고 목록을 조회한다.
class MainTest(TestCase):
    url = '/home/'
    client = APIClient()

    def setUp(self):
        now = timezone.now().date()
        IT_CATEGORY = create_category(1, "IT")
        MARKETING_CATEGORY = create_category(2, "창업")
        self.crew1 = Crew.objects.create(id=1, crew_name="멋쟁이사자처럼", description="0", category = IT_CATEGORY)
        self.crew2 = Crew.objects.create(id=2, crew_name="CEOS", description="0", category = MARKETING_CATEGORY)
        self.post1 = create_post(1, now, "신입부원을 모집합니다.", self.crew1)
        self.post2 = create_post(2, now+timedelta(days=8), "컴온", self.crew1)
        self.post3 = create_post(3, now+timedelta(days=9), "BE 신입부원 모집합니다.", self.crew2)
        self.post4 = create_post(4, now+timedelta(days=-1), "FE 신입부원 모집합니다.", self.crew2)

    # 모집 마감 순으로 모집 공고를 조회한다.
    def test_deadline_order(self):
        # given & when
        response = self.client.get(self.url)

        #then
        d_day1 = response.json()[0]['d_day'][2:]
        d_day2 = response.json()[1]['d_day'][2:]
        d_day3 = response.json()[2]['d_day'][2:]
        self.assertLess(d_day1, d_day2)
        self.assertLess(d_day2, d_day3)
        self.assertEqual(response.status_code, 200)

    # 모집 공고의 동아리 이름과 제목으로 검색한다.
    def test_search(self):
        # given & when
        params = {'search': 'CE'}
        response = self.client.get(self.url, data=params)

        # then
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.status_code, 200)

    # 모집 공고를 필터 검색한다.
    def test_filter(self):
        # given & when
        params = {'category': ['창업']}
        response = self.client.get(self.url, data=params)

        # then
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.status_code, 200)

    # 모집 공고를 키워드 검색과 필터 검색한다.
    def test_filter_search(self):
        # given & when
        params = {'category': ['IT'], 'search': '모집합니다'}
        response = self.client.get(self.url, data=params)

        # then
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.status_code, 200)

def create_post(id, apply_end_date, title, crew):
    return Post.objects.create(
        id=id,
        apply_start_date="1000-01-01 00:00:00",
        apply_end_date=apply_end_date.strftime('%Y-%m-%d 00:00:00'),
        document_result_date="1000-01-01 00:00:00",
        has_interview=False,
        requirement_target="0",
        title=title,
        content="0",
        membership_fee="0",
        crew=crew,
        progress="0"
    )

def create_category(id, name):
    return Category.objects.create(id=id, category_name=name)