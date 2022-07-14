from django.conf.urls import url

from users.views import *

urlpatterns=[
            url('^$',UserList.as_view(), name='user_list'),
            url('^change-password/$',UserChangePassword.as_view(),
                name='change_password'),
            url('^reset-password/$',UserResetPassword.as_view(),
                name='reset_password'),
            url('^verify-email/$',UserVerifyEmail.as_view(),
                name='verify_email'),

             url('^verify-phone/$',UserVerifyPhone.as_view(),
                name='verify_phone'),
          
            url('^(?P<pk>[a-zA-Z0-9-]+)/$',UserDetail.as_view(),
                name='user_detail'),
             ]
