from django.conf.urls import url

from .views import *

urlpatterns=[
            
            url('^$',GroupList.as_view()),
            url('^users/$',GroupUsers.as_view()),
            url('^(?P<pk>[\d+]+)/$',GroupDetail.as_view()),
            url('^manage-users/$',GroupManageUser.as_view()),
            
            ]
