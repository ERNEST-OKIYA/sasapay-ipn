
from django.conf.urls import url

from .views import *

urlpatterns=[
            url('^validation/$',C2BValidate.as_view(),name='c2b_validate'),
            url('^transactions/$',TransactionList.as_view(),),
            url('^confirm/$',C2BConfirm.as_view(),name='c2b_confirm'),
            url('^b2cresult/$',B2CApiResult.as_view(),name='b2c_api_result'),
            url('^b2ctimeout/$',B2CQueueTimeout.as_view(),name='b2c_queue_timeout'),
            url('^pay/$', B2CIncoming.as_view(), name='b2c_incoming'),
            url('^checkout-response/$', CheckoutResult.as_view(), name='checkout_response'),
            url('^incoming-checkouts/$', IncomingCheckouts.as_view(),
                name='checkout_incoming'),


            ]

