from django.conf.urls import url

from .views import *

urlpatterns=[
            url('^$',ContentTypeList.as_view()),
             ]
