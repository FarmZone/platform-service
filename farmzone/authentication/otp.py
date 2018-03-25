import requests
from django.conf import settings
from .constants import OTP_STATUS, TWO_FACTOR_OTP_REQUEST_URL, TWO_FACTOR_OTP_VERIFICATION_URL


class TwoFactorOTPClient:

    def __init__(self, api_key):
        self.api_key = api_key

    def send_otp(self, mobile_number):
        """
        Sends OTP to user's mobile number
        :param mobile_number: Entered by the user
        :return: HTTP response
        """
        if mobile_number:
            otp_response = requests.get(TWO_FACTOR_OTP_REQUEST_URL.format(self.api_key, mobile_number)).json()
            if otp_response['Status'] == 'Success':
                return otp_response['Details']
            return None
        return None

    def verify_otp(self, session_id, otp):
        """
        Verifies the OTP and session ID given in the request
        :param session_id: Provided by the client
        :param otp: Provided by the User
        :return: Boolean
        """
        otp_response = requests.get(TWO_FACTOR_OTP_VERIFICATION_URL.format(self.api_key, session_id, otp)).json()
        if otp_response['Status'] == 'Success':
            return True
        return False


class OTPRouter:

    def __init__(self, otp_providers):
        self.otp_providers = otp_providers

    def _pick_provider(self):
        # TODO: Think of how the otp provider will be decided
        return self.otp_providers[0]

    def send_otp(self, phone_number):
        """
        Pick the provider and call its send_otp method
        :param p: OTP entered by the customer
        :return: HTTP response
        """
        provider = self._pick_provider()
        return provider.send_otp(phone_number)

    def verify_otp(self, session_id, otp):
        """
        Get the otp entered by user and verify it
        :param session_id: 2factor's session id
        :param: otp entered by the user
        :return: HTTP response
        """
        provider = self._pick_provider()
        return provider.verify_otp(session_id, otp)


two_factor_otp_client = TwoFactorOTPClient(settings.TWO_FACTOR_API_KEY)


otp_provider = OTPRouter([two_factor_otp_client])
