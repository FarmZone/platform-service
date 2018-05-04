from farmzone.core.models import User
from farmzone.util_config.celery import app
from celery.utils.log import get_task_logger
from farmzone.util_config.translation_util import get_locale_based_template
from farmzone.notification.sms import sms_provider

logger = get_task_logger(__name__)


def send_sms_to_user(user, key, **kwargs):
    send_sms_to_user_id(user.id, key, **kwargs)


def send_sms_to_user_id(user_id, key, **kwargs):
    logger.info("Scheduling task to send SMS to user_id {0}".format(user_id))
    try:
        notify_user.delay(user_id, key, **kwargs)
    except Exception as e:
        logger.error("Not able to schedule send sms {0}".format(e))


@app.task
def notify_user(uid, sms_template_key, *args, **kwargs):
    user = User.objects.get(id=uid)
    if not user.is_active:
        logger.error("Inactive user_id: {0}. Not sending notification.".format(uid))
        return
    phone_number = user.get_phone_number()
    if not phone_number:
        logger.error("No phone number found for the user_id: {0}".format(uid))
        return

    preferred_locale = 'en'
    logger.debug("Sending SMS to user: {0}, in his preferred_local: {1}".format(user.full_name, preferred_locale))
    sms_body = get_locale_based_template(sms_template_key, preferred_locale)
    sms_body = sms_body.format(*args, **kwargs)
    logger.debug("Sending Transactional SMS {0} to number {1}".format(sms_body, phone_number))
    sms_provider.send_transactional_sms(phone_number, sms_body)
    logger.debug("SMS has been sent on number: {0}".format(phone_number))
