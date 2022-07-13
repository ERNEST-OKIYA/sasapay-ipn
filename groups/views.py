
from django.core.exceptions import ValidationError
from django.contrib.auth.models import Group
from rest_framework import generics

from utils.views import TransactionalViewMixin
from .serializers import *
from users.models import User







class GroupList(TransactionalViewMixin,generics.ListCreateAPIView):
    """ this lsits and creates permission groups """
   

    serializer_class=GroupSerializer
   
    def perform_create(self,serializer):
        serializer.save()

    def get_queryset(self):
        return Group.objects.all()




class GroupUsers(TransactionalViewMixin,generics.CreateAPIView):
    """ add user to permission group. also can remove user to permission group..abs
    if action==1 , add if action ==2 remove user 
    """

 
    serializer_class=GroupUserSerializer
    lookup_field=None 
    
  
    def perform_create(self,serializer):
        data=serializer.validated_data
       
        group=Group.objects.get(id=data.get('group'))
        user=User.objects.get(id=data.get('user'))
        if data.get('action')==1:
            #add 
            group.user_set.add(user)
        elif data.get('action')==2:
            #remove
            group.user_set.remove(user)
        else:
            pass

        return data



class GroupDetail(TransactionalViewMixin,generics.RetrieveUpdateDestroyAPIView):
    """ edit permission groups. 
    """

    serializer_class=GroupSerializer
    queryset=Group.objects.all()

  
    def perform_destroy(self,model_object):
        #model_object.is_active=True
        model_object.delete()




class GroupManageUser(TransactionalViewMixin,generics.CreateAPIView):
    """ add user to permission group. also can remove user to permission group..abs
    if action==1 , add if action ==2 remove user 
    """

    #permission_classes = (AllowAny,)
    #authentication_classes = ()
    
    serializer_class=GroupUserSerializer
    #renderer_classes = (CustomJSONRenderer, )

    def perform_create(self,serializer):
        data=serializer.validated_data
        print (data)
        group=Group.objects.get(id=data.get('group'))
        user=User.objects.get(id=data.get('user'))
        if data.get('action')==1:
            #add 
            group.user_set.add(user)
        elif data.get('action')==2:
            #remove
            group.user_set.remove(user)
        else:
            pass

        return data 
