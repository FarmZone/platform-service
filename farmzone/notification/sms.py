import json
import requests
import logging

from django.conf import settings
from .exceptions import MissingPhoneNumberException, MessageSendingFailed


logger = logging.getLogger(__name__)


class ExotelClient:
    # {0} is the sender id and {1} is the exotel token
    EXOTEL_SMS_URL = 'https://{0}:{1}@api.exotel.com/v1/Accounts/{0}/Sms/send.json'
    EXOTEL_SUCCESS_STATUS_LIST = ['queued', 'sending', 'submitted', 'sent']

    def __init__(self, sid, token, exo_phone):
        self.sid = sid
        self.token = token
        self.exo_phone = exo_phone

    def send_bulk_transactional_sms(self, phone_numbers, message):
        """
        Send SMS to multiple mobile numbers
        :param phone_number:
        :param message:
        :return:
        """
        if not settings.CAN_SEND_SMS:  # So that we do not send SMS while development
            return
        if not phone_numbers:
            logger.warning('No phone number received for meaasge: {0}'.format(message))
            raise MissingPhoneNumberException('No phone number received to send the SMS to')
        request_data = {
            'From': self.exo_phone,
            "To[]": phone_numbers,
            'Body': message
        }
        logger.info('Sending SMS to {0}. SMS content {1}'.format(phone_numbers, message))
        sms_response = requests.post(self.EXOTEL_SMS_URL.format(self.sid, self.token), data=request_data).json()
        logger.info(sms_response)
        for res in sms_response:
            if res.get('RestException'):
                logger.warn('SMS sending failed. Rsponse from exotel - {0}'.format(sms_response))
            elif res.get('SMSMessage') and res['SMSMessage']['Status'] \
                not in self.EXOTEL_SUCCESS_STATUS_LIST:
                raise MessageSendingFailed('The service provider failed to send the SMS')

    def send_transactional_sms(self, phone_number, message):
        """
        Sends SMS to user's mobile number
        :param phone_number: Mobile number of the user
        :return: HTTP response
        """
        if not settings.CAN_SEND_SMS:  # So that we do not send SMS while development
            return
        if not phone_number:
            logger.warning('No phone number received for meaasge: {0}'.format(message))
            raise MissingPhoneNumberException('No phone number received to send the SMS to')
        request_data = {
            'From': self.exo_phone,
            "To": phone_number,
            'Body': message
        }
        logger.info('Sending SMS to {0}. SMS content {1}'.format(phone_number, message))
        sms_response = requests.post(self.EXOTEL_SMS_URL.format(self.sid, self.token), data=request_data).json()
        logger.info(sms_response)
        if sms_response.get('RestException'):
            logger.warn('SMS sending failed. Rsponse from exotel - {0}'.format(sms_response))
        elif sms_response.get('SMSMessage') and sms_response['SMSMessage']['Status'] \
            not in self.EXOTEL_SUCCESS_STATUS_LIST:
            raise MessageSendingFailed('The service provider failed to send the SMS')


class Msg91Client:
    # {0} is the sender id and {1} is the exotel token
    MSG91_SMS_URL = 'http://api.msg91.com/api/v2/sendsms'

    def __init__(self, sender, route, country, authkey):
        self.sender = sender
        self.route = route
        self.country = country
        self.authkey = authkey
        self.request_method = "POST"
        self.content_type = "application/json"

    def _get_headers(self):
        return {'authkey': self.authkey, 'content-type': self.content_type}

    def _get_request(self):
        return { "sender": self.sender, "route": self.route, "country": self.country }

    def _get_response_from_msg91(self, method, url, data):
        resp = {}
        try:
            resp_obj = requests.request(method, url,
                                    headers=self._get_headers(),
                                    data=json.dumps(data), timeout=15)
            resp = resp_obj.json()
            logger.info("Response from Msg91 API for URL: {0}. Response status code {1}. Response: {2}"
                        .format(url, resp_obj.status_code, resp))
        except Exception as e:
            logger.info("Error occurred on response from Msg91 API for URL: {0}. Error is {1}".\
                        format(url, str(e)))
        return resp

    def send_bulk_transactional_sms(self, phone_numbers, message):
        pass

    def send_transactional_sms(self, phone_number, message):
        """
        Sends SMS to user's mobile number
        :param phone_number: Mobile number of the user
        :return: HTTP response
        """
        if not settings.CAN_SEND_SMS:  # So that we do not send SMS while development
            return
        if not phone_number:
            logger.warning('No phone number received for meaasge: {0}'.format(message))
            raise MissingPhoneNumberException('No phone number received to send the SMS to')
        request_data = self._get_request()
        request_data["sms"] = [{"message": message, "to": [phone_number]}]
        logger.info('Sending SMS to {0}. SMS content {1}'.format(phone_number, request_data))
        sms_response = self._get_response_from_msg91(self.request_method, self.MSG91_SMS_URL, request_data)
        logger.info("sms_response {0}".format(sms_response))
        if sms_response.get('type') != "success":
            raise MessageSendingFailed('The service provider failed to send the SMS')


class SMSRouter:

    def __init__(self, providers):
        self.providers = providers

    def _pick_provider(self):
        # TODO: Logic to pick a provider
        return self.providers[0]

    def send_bulk_transactional_sms(self, phone_numbers, message):
        """
        Pick the provider and call its send_transaction_sms method
        :param phone_numbers: Phone number of the user to whom the SMS has to be sent
        :return: HTTP response
        """
        provider = self._pick_provider()
        return provider.send_bulk_transactional_sms(phone_numbers, message)

    def send_transactional_sms(self, phone_number, message):
        """
        Pick the provider and call its send_transaction_sms method
        :param phone_number: Phone number of the user to whom the SMS has to be sent
        :return: HTTP response
        """
        provider = self._pick_provider()
        return provider.send_transactional_sms(phone_number, message)


exotel = ExotelClient(settings.EXOTEL_SID, settings.EXOTEL_TOKEN, settings.EXO_PHONE)
msg91 = Msg91Client(settings.MSG91_SENDER, settings.MSG91_TSMS_ROUTE, settings.MSG91_COUNTRY, settings.MSG91_TOKEN)

sms_provider = SMSRouter([msg91, exotel, ])
