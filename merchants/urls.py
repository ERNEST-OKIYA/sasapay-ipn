from django.conf.urls import url

from .views import MerchantList,MerchantDetail,MerchantAPICredentials


urlpatterns=[
    url(r'^$',MerchantList.as_view()),
    url('^(?P<pk>[\d+]+)/$',MerchantDetail.as_view()),
    url('^(?P<pk>[\d+]+)/api-credentials$',MerchantAPICredentials.as_view()),

]