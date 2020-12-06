from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Task
from .serializers import TaskSerializer, GetTaskSerializer

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def post_task(request):
    try:
        data = dict(request.data)
        data['user'] = request.user.pk
        serializer = TaskSerializer(data=data)
        if serializer.is_valid():
            serializer.save_and_start_processing()
            return Response({'msg':'operation successful'})
        else :
            return Response(serializer.errors, 400)
    except Exception as ex:
        print('internal server error ->', ex)
        return Response({'msg':'internal server error'}, 500)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_task(request):
    try:
        serializer = GetTaskSerializer(data=request.data)
        if serializer.is_valid():
            task = serializer.get_task()
            serializer = TaskSerializer(serializer.get_task())
            if task.user != request.user:
                return Response({'msg':'unauthorized operation'}, 401)
            return Response(serializer.data)
        else :
            return Response(serializer.errors, 400)
    except Exception as ex:
        print('internal server error ->', ex)
        return Response({'msg':'internal server error'}, 500)

