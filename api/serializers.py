from rest_framework import serializers
from myadmin.models import *

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientRecord
        fields ='__all__'