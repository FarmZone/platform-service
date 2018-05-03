from __future__ import unicode_literals, absolute_import
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from rest_framework.routers import DefaultRouter
from farmzone.authentication.views import UserViewSet
from .swagger_customization import get_swagger_view
from farmzone.authentication import v1_urls as v1_authentication_urls
from farmzone.sellers import v1_urls as v1_seller_urls
from farmzone.buyers import v1_urls as v1_buyer_urls
from farmzone.support import v1_urls as v1_support_urls
from ajax_select import urls as ajax_select_urls

router = DefaultRouter()
router.register(r'users', UserViewSet)

schema_view = get_swagger_view(title='Farmzone APIs')


urlpatterns = [
    url(r'^ajax_select/', include(ajax_select_urls)),
    # url(r'^django-admin/', admin.site.urls),
    url(r'^', admin.site.urls),
    url(r'^accounts/login/$', auth_views.login, name='login'),
    url(r'^swagger/$', schema_view),
    url(r'^api/(?P<app_version>(\d*\.\d*\.\d*))/', include(v1_authentication_urls)),
    url(r'^api/(?P<app_version>(\d*\.\d*\.\d*))/', include(v1_seller_urls)),
    url(r'^api/(?P<app_version>(\d*\.\d*\.\d*))/', include(v1_buyer_urls)),
    url(r'^api/(?P<app_version>(\d*\.\d*\.\d*))/', include(v1_support_urls)),
    url(r'^api/v1/', include(v1_authentication_urls)),
    url(r'^api/v1/', include(v1_seller_urls)),
]

urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
