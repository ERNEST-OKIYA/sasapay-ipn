
from django.conf.urls import url

from .views import *

urlpatterns=[

            url('^dashboard/$', Deposits.as_view(), name='dashboard'),
            url('^payouts/$', Payouts.as_view(), name='payouts'),
            


            ]