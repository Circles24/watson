from django.urls import path
from .views import get_task, post_task

urlpatterns = [
        path('post', post_task, name='post task'),
        path('get', get_task, name='get task')
        ]
