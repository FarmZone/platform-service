from __future__ import unicode_literals, absolute_import
from django.conf.urls import include, url
from farmzone.authentication import views


urlpatterns = [
    url(r'send-otp/?$', views.SendOTPView.as_view()),
    url(r'verify-otp/?$', views.VerifyOTPView.as_view()),
    url(r'user/profile/?$', views.UserProfileView.as_view()),
    url(r'user/save_address/?$', views.SaveAddressView.as_view()),
]
