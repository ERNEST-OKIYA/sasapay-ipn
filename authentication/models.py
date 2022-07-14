from django.db import models
from rest_framework.authentication import TokenAuthentication,BaseAuthentication
from rest_framework.authtoken.models import Token

from rest_framework.exceptions import AuthenticationFailed
from django.utils import timezone
from rest_framework import exceptions

from datetime import timedelta
from rest_framework import exceptions

from users.models import User
from merchants.models import Merchant



class ExpiringTokenAuthentication(TokenAuthentication):
    model=Token
    def authenticate_credentials(self, key):

        try:
            token = self.model.objects.get(key=key)
        except self.model.DoesNotExist:
            raise exceptions.AuthenticationFailed('Invalid Token')
        
        if not token.user.is_active:
            raise exceptions.AuthenticationFailed('User is inactive or deleted')

        if token.created < timezone.now() - timedelta(minutes=6000):
            raise exceptions.AuthenticationFailed('Token has expired')
        
        #update token created date for active users
        token.created = timezone.now()
        token.save() 

        return token.user, token
    


class APIAuthentication(BaseAuthentication):
    
    def authenticate(self, request):

        app_secret=request.META.get('HTTP_APP_SECRET')
        app_key = request.META.get('HTTP_APP_KEY')
       
        if not app_secret or  not app_key:
            return None
      
        user = Merchant.get_user(app_secret=app_secret,app_key=app_key)
        if not user:
            raise exceptions.AuthenticationFailed('Authentication Failed')
            
        if not user.is_active:
            raise exceptions.AuthenticationFailed('Account Disabled')

        return (user, None)
    
