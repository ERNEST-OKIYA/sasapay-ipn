

from rest_framework import generics
from utils.views import TransactionalViewMixin
from .serializers import *
from .models import Merchant,gen_uuid




class MerchantList(TransactionalViewMixin,generics.ListCreateAPIView):
    """ this lsits and creates Merchants"""
   

    serializer_class=MerchantSerializer
   
    def perform_create(self,serializer):
        serializer.save()

    def get_queryset(self):
        return Merchant.objects.filter(is_deleted=False)


class MerchantDetail(TransactionalViewMixin,generics.RetrieveUpdateDestroyAPIView):
    """ edit merchannt 
    """

    serializer_class=MerchantSerializer
    queryset=Merchant.objects.all()

  
    def perform_destroy(self,model_object):
        model_object.is_deleted=True
        model_object.save()




class MerchantAPICredentials(TransactionalViewMixin,generics.RetrieveUpdateAPIView):
    """ Get API credetnisla of a user, and also update the user api credntisla
    calling this by empty patch, sets the API keys.
    """
    serializer_class=MerchantSerializer
    queryset=Merchant.objects.all()

    def get_object(self):
        pk=self.kwargs['pk']
        return Merchant.objects.get(pk=pk)
       

    def perform_update(self,serializer):
        return serializer.save(app_key=gen_uuid(),app_secret=gen_uuid())
        
       