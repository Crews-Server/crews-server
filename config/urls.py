from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from .settings import DEBUG, MEDIA_URL, MEDIA_ROOT

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('apply/', include('apply.urls')),
    path('evaluation/', include('evaluation.urls')),
    path('home/', include('home.urls')),
    path('mypage/', include('mypage.urls')),
    path('post/', include('post.urls')),
]

if DEBUG:
    urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)