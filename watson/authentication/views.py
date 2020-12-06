from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import RegisterSerializer

@api_view(['POST'])
def register(request):
    try:
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'operation successful'})
        else:
            return Response(serializer.errors, 400)

    except Exception as ex:
        print('internal server error -> ', ex)
        return Response({'msg':'internal server error'}, 500)
