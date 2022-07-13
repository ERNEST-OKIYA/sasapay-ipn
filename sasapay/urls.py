from django.conf.urls import url,include
from django.contrib import admin
from authentication.views import obtain_expiring_auth_token
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_swagger.views import get_swagger_view
from admin_portal.views import Dashboard
from django.contrib.auth.views import login,logout



urlpatterns = [

    url(r'^admin/', admin.site.urls),
    url(r'^authenticate/',obtain_expiring_auth_token,name='authenticate'),
    url(r'^users/', include('users.urls',namespace='users')),
    url(r'^groups/', include('groups.urls',namespace='groups')),
    url(r'^permissions/', include('permissions.urls',namespace='permissions')),
    url(r'^content-types/', include('content_types.urls',namespace='content_types')),
    url(r'^merchants/', include('merchants.urls',namespace='merchants')),
    url(r'^ipn/', include('payments.urls',namespace='payments')),
    url(r'^dashboard/',Dashboard.as_view(),name='dashboard'),
    url(r'^login/$', login, name='login'),

    url(r'^logout/$', logout, name='logout' ),



    # url(r'^docs/$', get_swagger_view(title='REST API Documentation'))


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
