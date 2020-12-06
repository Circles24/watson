from rest_framework import serializers
from .models import Task
from .crawl_engine import start_processing
import requests

def is_url_valid(url):
    try:
        res = requests.head(url)
        is_status_valid = res.status_code == 200
        is_header_valid = False
        possible_headers = ['content-type', 'Content-Type', 'Content-type', 'CONTENT-TYPE']
        for header in possible_headers:
            if header in res.headers.keys():
                is_header_valid = res.headers[header].startswith('text/html')
        return is_status_valid and is_header_valid
    except Exception as ex:
        return False


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

    def validate_url(self, url):
        if is_url_valid(url) == False:
            raise serializers.ValidationError('invalid url')
        return url

    def save_and_start_processing(self):
        self.save()
        start_processing.delay(self.data['id'])



class GetTaskSerializer(serializers.Serializer):
    id = serializers.IntegerField()

    def validate_id(self, id):
        if Task.objects.filter(id=id).count() == 0:
            raise serializers.ValidationError(f'no task with id::{id} exists')
        return id

    def get_task(self):
        return Task.objects.filter(id=self.validated_data['id']).first()
