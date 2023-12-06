from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient

from datetime import timedelta, datetime

from .utils import create_category, create_crew, create_post


# 메인 페이지에서 모집 공고 목록을 커서 페이지네이션으로 조회한다.
class MainPageTest(TestCase):
    url = '/home/'
    client = APIClient()

    def setUp(self):
        now = timezone.now().date()
        self.IT_CATEGORY = create_category(1, "IT")
        self.MARKETING_CATEGORY = create_category(2, "마케팅")
        self.LIKELION_CREW = create_crew(1, "멋쟁이사자처럼", self.IT_CATEGORY)
        self.CEOS_CREW = create_crew(2, "CEOS", self.MARKETING_CATEGORY)
        self.LIKELION_POST_LIST = create_posts(1, self.LIKELION_CREW, now) # 1~100 까지는 LIKELION_CREW의 post
        self.CEOS_POST_LIST = create_posts(101, self.CEOS_CREW, now) # 101~200 까지는 CEOS_CREW의 post
    
    # 첫 페이지를 조회한다.
    def test_cursor_pagination(self):
        # given & when
        ## 첫 번째 페이지 조회
        response = self.client.get(self.url)

        ## 두 번째 페이지 조회
        second_page = response.json()['next'].replace('http://testserver', '')
        response = self.client.get(second_page)

        # then
        self.assertEqual(len(response.json()['results']), 6)
        self.assertEqual(response.status_code, 200)

# 페이지네이션을 테스트하기 위해 많은 더미 데이터를 생성한다.
def create_posts(start_id, crew, now):
    posts = []
    titles = ["신입부원을 모집합니다.", "BE 신입부원 모집합니다.", "FE 신입부원 모집합니다."]
    dates = [now, now+timedelta(days=8), now+timedelta(days=9)]
    for i in range(start_id, start_id+99):
        posts.append(
            create_post(i, dates[i%3], titles[i%3], crew)
        )
    posts.append(create_post(start_id+99, datetime.max, "상시 모집합니다.", crew))