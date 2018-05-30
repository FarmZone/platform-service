from farmzone.util_config.tasks import send_sms_to_user_id, send_buyer_order_notification\
    , send_seller_order_notification, send_buyer_complain_notification, send_seller_complain_notification
from farmzone.notification.keys import user as user_keys
from farmzone.notification.keys import order as order_keys
from farmzone.notification.keys import query as query_keys
from farmzone.order.models import OrderStatus
from farmzone.support.models import SupportStatus


def send_create_user_notification(user_id):
    send_sms_to_user_id(user_id, user_keys.user_create_user_user_key, id=user_id)


def send_place_order_notification(user_id, order_id, seller_user_ids):
    send_sms_to_user_id(user_id, order_keys.buyer_place_order_buyer_key, order_id=order_id)
    send_buyer_order_notification(user_id, order_id, OrderStatus.NEW.value)
    if seller_user_ids:
        for seller_user_id in seller_user_ids:
            send_sms_to_user_id(seller_user_id, order_keys.buyer_place_order_seller_key, order_id=order_id)
            send_seller_order_notification(seller_user_id, order_id, OrderStatus.NEW.value)


def send_cancel_order_notification(user_id, order_id, seller_user_ids):
    send_sms_to_user_id(user_id, order_keys.buyer_cancel_order_buyer_key, order_id=order_id)
    send_buyer_order_notification(user_id, order_id, OrderStatus.CANCELLED.value)
    if seller_user_ids:
        for seller_user_id in seller_user_ids:
            send_sms_to_user_id(seller_user_id, order_keys.buyer_cancel_order_seller_key, order_id=order_id)
            send_seller_order_notification(seller_user_id, order_id, OrderStatus.CANCELLED.value)


def send_accept_order_notification(order_detail_id, order, buyer_user, seller_user_ids):
    if buyer_user:
        send_sms_to_user_id(buyer_user.id, order_keys.seller_accept_order_buyer_key,
                            order_id=order.id if order else None)
        send_buyer_order_notification(buyer_user.id, order.id, OrderStatus.ACCEPTED.value)
    if seller_user_ids:
        for seller_user_id in seller_user_ids:
            send_sms_to_user_id(seller_user_id, order_keys.seller_accept_order_seller_key,
                            order_id=order.id if order else None)
            send_seller_order_notification(seller_user_id, order.id, OrderStatus.ACCEPTED.value)


def send_dispatch_order_notification(order_detail_id, order, buyer_user, seller_user_ids):
    if buyer_user:
        send_sms_to_user_id(buyer_user.id, order_keys.seller_dispatch_order_buyer_key,
                            order_id=order.id if order else None)
        send_buyer_order_notification(buyer_user.id, order.id, OrderStatus.DISPATCHED.value)
    if seller_user_ids:
        for seller_user_id in seller_user_ids:
            send_sms_to_user_id(seller_user_id, order_keys.seller_dispatch_order_seller_key,
                            order_id=order.id if order else None)
            send_seller_order_notification(seller_user_id, order.id, OrderStatus.DISPATCHED.value)


def send_complete_order_notification(order_detail_id, order, buyer_user, seller_user_ids):
    if buyer_user:
        send_sms_to_user_id(buyer_user.id, order_keys.buyer_complete_order_buyer_key,
                            order_id=order.id if order else None)
        send_buyer_order_notification(buyer_user.id, order.id, OrderStatus.COMPLETED.value)
    if seller_user_ids:
        for seller_user_id in seller_user_ids:
            send_sms_to_user_id(seller_user_id, order_keys.buyer_complete_order_seller_key,
                            order_id=order.id if order else None)
            send_seller_order_notification(seller_user_id, order.id, OrderStatus.COMPLETED.value)


def send_save_query_notification(user_id, query_id, seller_user_ids):
    send_sms_to_user_id(user_id, query_keys.buyer_save_query_buyer_key, query_id=query_id)
    send_buyer_complain_notification(user_id, query_id, SupportStatus.NEW.value)
    if seller_user_ids:
        for seller_user_id in seller_user_ids:
            send_sms_to_user_id(seller_user_id, query_keys.buyer_save_query_seller_key, query_id=query_id)
            send_seller_complain_notification(seller_user_id, query_id, SupportStatus.NEW.value)


def send_accept_query_notification(query_id, buyer_user, seller_user_ids):
    if buyer_user:
        send_sms_to_user_id(buyer_user.id, query_keys.seller_accept_query_buyer_key, query_id=query_id)
        send_buyer_complain_notification(buyer_user.id, query_id, SupportStatus.ACCEPTED.value)
    if seller_user_ids:
        for seller_user_id in seller_user_ids:
            send_sms_to_user_id(seller_user_id, query_keys.seller_accept_query_seller_key, query_id=query_id)
            send_seller_complain_notification(seller_user_id, query_id, SupportStatus.ACCEPTED.value)


def send_resolve_query_notification(user_id, query_id, seller_user_ids):
    send_sms_to_user_id(user_id, query_keys.buyer_resolve_query_buyer_key, query_id=query_id)
    send_buyer_complain_notification(user_id, query_id, SupportStatus.RESOLVED.value)
    if seller_user_ids:
        for seller_user_id in seller_user_ids:
            send_sms_to_user_id(seller_user_id, query_keys.buyer_resolve_query_seller_key, query_id=query_id)
            send_seller_complain_notification(seller_user_id, query_id, SupportStatus.RESOLVED.value)
