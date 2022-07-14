from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType


class ContentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        #depth=1
        model=ContentType
        fields='__all__'

