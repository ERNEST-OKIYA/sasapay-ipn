
from django.contrib.contenttypes.models import ContentType

from rest_framework import generics
from .serializers import *

class ContentTypeList(generics.ListAPIView):
    """ list content types  """

    serializer_class=ContentTypeSerializer
   


    def get_queryset(self):
        return ContentType.objects.all()







