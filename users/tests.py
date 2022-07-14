from django.test import TestCase

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


from rest_framework.authtoken.models import Token

from .models import User


class UserTests(APITestCase):
    
    def test_users(self):

        """
        Ensure new user can be created
        """

        url=reverse('users:user_list')
        data={'first_name':"morfat",'last_name':'mosoti',
              'email':'morfatmosoti@test.com','password':'admin2016',
              'phone_number':'254700872844'
              }
        response=self.client.post(url,data)
        
        #assign Token
        self.token=Token.objects.create(user=User.objects.get())
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(),1)
        self.assertEqual(User.objects.get().email,'morfatmosoti@test.com')
        
        #login
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        #get user test 
        url=reverse('users:user_detail',args=(1,))
        response=self.client.get(url)
        self.assertEqual(response.status_code,status.HTTP_200_OK)

        #put test 
        data={'first_name':'Mosoti Ogega'}
        response=self.client.patch(url,data=data)
        self.assertEqual(response.data.get('first_name'),'Mosoti Ogega')

        #put test 
        data={'first_name':"morfat",'last_name':'mosoti',
              'email':'morfatmosoti@test.com2',
              'phone_number':'254700872844'
              }

        response=self.client.put(url,data=data)
        self.assertEqual(response.data.get('email'),'morfatmosoti@test.com2')







