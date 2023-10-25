from rest_framework.response import Response
from rest_framework.decorators import api_view
from myadmin.models import *
from .serializers import *

@api_view(['GET'])
def getData(request):
    client = ClientRecord.objects.all()
    serializers = ClientSerializer(client, many=True)
    return Response(serializers.data)