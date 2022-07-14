from django.conf.urls import url,include
from django.contrib import admin
from authentication.views import obtain_expiring_auth_token
from django.conf import settings
from django.conf.urls.static import static
from admin_portal.views import Deposits,Payouts
from django.contrib.auth import login,logout



urlpatterns = [

    url(r'^cpanel/', include('admin_portal.urls')),
    url(r'^authenticate/',obtain_expiring_auth_token,name='authenticate'),
    url(r'^users/', include('users.urls')),
    url(r'^groups/', include('groups.urls')),
    url(r'^permissions/', include('permissions.urls')),
    url(r'^content-types/', include('content_types.urls')),
    url(r'^merchants/', include('merchants.urls')),
    url(r'^ipn/', include('payments.urls')),
    url(r'^dashboard/',Deposits.as_view(),name='deposits'),
    url(r'^payouts/',Payouts.as_view(),name='payouts'),
    url(r'^login/$', login, name='login'),
    url(r'^logout/$', logout, name='logout' ),



    # url(r'^docs/$', get_swagger_view(title='REST API Documentation'))


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
