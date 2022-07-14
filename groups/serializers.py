from rest_framework import serializers
from django.contrib.auth.models import Group



class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        #depth=1
        model=Group
        fields='__all__'

class GroupUserSerializer(serializers.Serializer):
    group=serializers.IntegerField()
    action=serializers.IntegerField()
    user=serializers.CharField(max_length=300)

