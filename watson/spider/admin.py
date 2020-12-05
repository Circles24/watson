from django.contrib import admin
from .models import Task, Page

admin.site.register([Task, Page])
