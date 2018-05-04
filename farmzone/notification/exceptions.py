class MissingPhoneNumberException(Exception):
    """Raised when the sms module does not get a phone number to send the SMS to"""


class MessageSendingFailed(Exception):
    """Raised when the service provideer fails to send the sms"""
