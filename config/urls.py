from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('apply/', include('apply.urls')),
    path('evaluation/', include('evaluation.urls')),
    path('home/', include('home.urls')),
    path('mypage/', include('mypage.urls')),
    path('post/', include('post.urls')),
    path('table/', include('table.urls')),
]
