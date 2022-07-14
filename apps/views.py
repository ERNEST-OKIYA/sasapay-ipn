

from rest_framework import generics
from utils.views import TransactionalViewMixin
from .serializers import *
from .models import App



class AppsList(TransactionalViewMixin,generics.ListCreateAPIView):
    """ this lsits and creates permission groups """
   

    serializer_class=AppSerializer
   
    def perform_create(self,serializer):
        serializer.save()

    def get_queryset(self):
        return App.objects.all()
