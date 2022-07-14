from django.conf.urls import url

from .views import AppsList


urlpatterns=[
    url(r'^$',AppsList.as_view(),name="apps"),
]