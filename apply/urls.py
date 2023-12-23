from django.urls import path

from .views import application_create, Appication, ApplyCreate

urlpatterns = [
    path('application/', application_create, name='application-create'), # 지원서 양식 생성(create)
    path('post/<int:post_id>/', Appication.as_view(), name='application'), # 지원서 양식 조회(get)
    path('', ApplyCreate.as_view(), name='apply'), # 지원서 작성(create)
]
