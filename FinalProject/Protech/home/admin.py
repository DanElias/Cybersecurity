from django.contrib import admin

from home.models import Question
from home.models import Choice

admin.site.register(Question)
admin.site.register(Choice)
