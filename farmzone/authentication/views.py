from __future__ import unicode_literals, absolute_import

import logging
from rest_framework import viewsets, mixins
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from farmzone.core.models import User, Address, UserAppInfo, StateCode
from farmzone.sellers.models import PreferredSeller
from .permissions import IsUserOrReadOnly
from .serializers import CreateUserSerializer
from farmzone.core.models import PhoneNumber
from rest_framework.response import Response
from farmzone.core.serializers import PhoneNumberSerializer, UserSerializer
from farmzone.authentication.otp import otp_provider
from .constants import OTP_STATUS
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.db import transaction, IntegrityError
from farmzone.notification import notification

logger = logging.getLogger(__name__)


class UserViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  viewsets.GenericViewSet):
    """
    Creates, Updates, and retrives User accounts
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsUserOrReadOnly,)

    def create(self, request, *args, **kwargs):
        self.serializer_class = CreateUserSerializer
        self.permission_classes = (AllowAny,)
        return super(UserViewSet, self).create(request, *args, **kwargs)


class UserProfileView(APIView):
    def get(self, request, app_version=None):
        logger.info("Request to fetch user's profile for user_id: {0}".format(request.user.id))
        res = UserSerializer(request.user).data
        return Response(res)


def send_otp(record):
    """Utility function to send OTP and get HTTPResponse based on result"""

    mobile_number = record.phone_number
    session_id = otp_provider.send_otp(mobile_number)
    logger.info("Request to send OTP has been submitted successfully")
    if session_id:
        res = OTP_STATUS['sent']
        res.update({
            'session_id': session_id,
            "contact": PhoneNumberSerializer(record).data
        })
        return Response(res)
    res = OTP_STATUS['not_sent']
    return Response(res, status.HTTP_503_SERVICE_UNAVAILABLE)


class SendOTPView(APIView):
    """API to perform OTP based signup or login for farmers.
    :returns Response({ session_id: "uteir-12hsd-1823h2" })
    """
    permission_classes = ()

    @classmethod
    def new_user_onboarding(cls, mobile_number, user_name, request, app_version):
        with transaction.atomic():
            logger.info("Creating new user entry")
            user = User.create_user(user_name)
            logger.info("Creating new phone_number entry "
                        "for userID: {0}, mobile_number: {1}".format(user.id, mobile_number))
            PhoneNumber.create_phone_number(user, mobile_number)
            Address.create_address(user, request.data.get('state_code'))
            PreferredSeller.create_preferred_seller(user, request.data.get('seller_code'))
            UserAppInfo.create_user_app_info(user, app_version, request.data.get('other'), request.data.get('seller_code'))

    @classmethod
    def existing_user_onboarding(cls, user, user_name, request, app_version):
        user.full_name = user_name
        user.save()
        UserAppInfo.create_user_app_info(user, app_version, request.data.get('other'), request.data.get('seller_code'))
        PreferredSeller.create_preferred_seller(user, request.data.get('seller_code'))

    def execute(self, mobile_number, user_name, request, app_version):
        try:
            phone_number = PhoneNumber.objects.filter(phone_number=mobile_number).first()
            if not phone_number:
                logger.info("No record exists for the mobile_number: {0}. "
                            "Starting new user onboarding flow".format(mobile_number))
                self.new_user_onboarding(mobile_number, user_name, request, app_version)
                phone_number = PhoneNumber.objects.filter(phone_number=mobile_number).first()
            else:
                logger.info("Record exists for the mobile number: {0}".format(mobile_number))
                self.existing_user_onboarding(phone_number.user, user_name, request, app_version)
            return send_otp(phone_number)
        except IntegrityError as e:
            logger.debug("Error while registering user {0}".format(e))
            return Response({
                "status_code": "UNABLE_TO_REGISTER_USER",
                "details": "We are unable to register user. Please contact admin."
            }, status.HTTP_200_OK)

    def post(self, request, app_version=None):
        mobile_number = request.data.get('mobile_number')
        user_name = request.data.get('user_name')
        if not mobile_number or not user_name:
            logger.warning("Mobile number or username field is missing during send otp")
            return Response({
                "status_code": "MISSING_REQUIRED_FIELD",
                "details": "Either mobile number or username is missing."
            }, status.HTTP_200_OK)
        logger.info("Processing SendOTP request for mobile_number: {0}, username {1}".format(mobile_number, user_name))
        return self.execute(mobile_number, user_name, request, app_version)


class VerifyOTPView(APIView):
    """API to verify the phone number and mark it as active.

    This API should be called with mobile_number, otp and session_id
    obtained from send-otp API for successfull verification.

    :returns This API will return auth-token for the farmer
    """

    permission_classes = ()

    def post(self, request, app_version=None):
        otp = request.data.get('otp')
        mobile_number = request.data.get('mobile_number')
        session_id = request.data.get('session_id')
        logger.info("otp {0}, mobile_number {1}, session_id {2}".format(otp, mobile_number, session_id))
        if otp and session_id and mobile_number:
            if otp_provider.verify_otp(session_id, otp):
                try:
                    phone_number_record = PhoneNumber.objects.get(phone_number=mobile_number)
                    phone_number_record.is_active = True
                    phone_number_record.save()
                except PhoneNumber.DoesNotExist:
                    return Response({
                        'status_code': 'PHONE_NUMBER_DOES_NOT_EXIST',
                        'details': 'This phone number does not exist.'
                    }, status.HTTP_200_OK)
                try:
                    user = phone_number_record.user
                    auth_token = Token.objects.get(user=user)
                    if not user.is_welcome_sms_sent:
                        logger.debug("sending welcome msg to user {0}".format(user))
                        notification.send_create_user_notification(user.id)
                        user.is_welcome_sms_sent=True
                        user.save()
                except Token.DoesNotExist:
                    return Response(
                        {'status_code': 'TOKEN_DOES_NOT_EXIST', 'details': 'Auth token not found for this user.'},
                        status.HTTP_200_OK
                    )
                OTP_STATUS['verified']['auth_token'] = auth_token.key
                return Response(OTP_STATUS['verified'], status.HTTP_200_OK)
            return Response(OTP_STATUS['verification_failed'], status.HTTP_200_OK)
        return Response({'status': 'failed', 'details': 'Either OTP or session id or mobile number is missing.'}, status.HTTP_200_OK)


class SaveAddressView(APIView):
    permission_classes = ()

    def post(self, request, app_version=None):
        address_line1 = request.data.get('address_line1')
        address_line2 = request.data.get('address_line2')
        address_line3 = request.data.get('address_line3')
        state_code = request.data.get('state_code')
        user = request.user
        logger.info("state_code {0}, user {1}, address_line1 {2}".format(state_code, user, address_line1))
        if not state_code or not user:
            logger.warning("user and state_code is mandatory")
            return Response({
                "status_code": "MISSING_REQUIRED_FIELD",
                "details": "Please select state."
            }, status.HTTP_200_OK)
        state_obj = StateCode.objects.filter(code=state_code).first()
        if not state_obj:
            logger.warning("State code does not match any state {0}".format(state_code))
            return Response({
                "status_code": "INVALID_REQUIRED_FIELD",
                "details": "State code does not match any state."
            }, status.HTTP_200_OK)
        Address.create_update_address(user, state_obj, address_line1, address_line2, address_line3)
        return Response({
            "status_code": "SUCCESS",
            "details": "Address saved successfully"
        }, status.HTTP_200_OK)