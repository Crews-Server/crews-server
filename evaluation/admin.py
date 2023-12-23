from django.contrib import admin

from .models import *

admin.site.register(Comment)
admin.site.register(Score)
admin.site.register(Evaluation)
