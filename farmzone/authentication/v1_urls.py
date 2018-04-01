from __future__ import unicode_literals, absolute_import
from django.conf.urls import include, url
from farmzone.authentication import views


urlpatterns = [
    url('send-otp/?$', views.SendOTPView.as_view()),
    url('verify-otp/?$', views.VerifyOTPView.as_view()),
    url('user/profile/?$', views.UserProfileView.as_view()),
]