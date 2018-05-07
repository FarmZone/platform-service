from farmzone.util_config.tasks import send_sms_to_user_id
from farmzone.notification.keys import user as user_keys
from farmzone.notification.keys import order as order_keys
from farmzone.notification.keys import query as query_keys
from farmzone.qms.query import get_seller_user_by_query, get_buyer_user_by_query
from farmzone.oms.order import get_buyer_user_by_order_detail, get_seller_user_by_order_detail\
    , get_order_by_order_detail, get_seller_users_by_order


def send_create_user_notification(user_id):
    send_sms_to_user_id(user_id, user_keys.user_create_user_user_key, id=user_id)


def send_place_order_notification(user_id, order_id):
    send_sms_to_user_id(user_id, order_keys.buyer_place_order_buyer_key, order_id=order_id)
    seller_user_ids = get_seller_users_by_order(order_id)
    if seller_user_ids:
        for seller_user_id in seller_user_ids:
            send_sms_to_user_id(seller_user_id, order_keys.buyer_place_order_seller_key, order_id=order_id)


def send_cancel_order_notification(user_id, order_id):
    send_sms_to_user_id(user_id, order_keys.buyer_cancel_order_buyer_key, order_id=order_id)
    seller_user_ids = get_seller_users_by_order(order_id)
    if seller_user_ids:
        for seller_user_id in seller_user_ids:
            send_sms_to_user_id(seller_user_id, order_keys.buyer_cancel_order_seller_key, order_id=order_id)


def send_accept_order_notification(order_detail_id):
    order = get_order_by_order_detail(order_detail_id)
    buyer_user = get_buyer_user_by_order_detail(order_detail_id)
    if buyer_user:
        send_sms_to_user_id(buyer_user.id, order_keys.seller_accept_order_buyer_key,
                            order_id=order.id if order else None)
    seller_user = get_seller_user_by_order_detail(order_detail_id)
    if seller_user:
        send_sms_to_user_id(seller_user.id, order_keys.seller_accept_order_seller_key,
                            order_id=order.id if order else None)


def send_dispatch_order_notification(order_detail_id):
    order = get_order_by_order_detail(order_detail_id)
    buyer_user = get_buyer_user_by_order_detail(order_detail_id)
    if buyer_user:
        send_sms_to_user_id(buyer_user.id, order_keys.seller_dispatch_order_buyer_key,
                            order_id=order.id if order else None)
    seller_user = get_seller_user_by_order_detail(order_detail_id)
    if seller_user:
        send_sms_to_user_id(seller_user.id, order_keys.seller_dispatch_order_seller_key,
                            order_id=order.id if order else None)


def send_complete_order_notification(order_detail_id):
    order = get_order_by_order_detail(order_detail_id)
    buyer_user = get_buyer_user_by_order_detail(order_detail_id)
    if buyer_user:
        send_sms_to_user_id(buyer_user.id, order_keys.buyer_complete_order_buyer_key,
                            order_id=order.id if order else None)
    seller_user = get_seller_user_by_order_detail(order_detail_id)
    if seller_user:
        send_sms_to_user_id(seller_user.id, order_keys.buyer_complete_order_seller_key,
                            order_id=order.id if order else None)


def send_save_query_notification(user_id, query_id):
    send_sms_to_user_id(user_id, query_keys.buyer_save_query_buyer_key, query_id=query_id)
    seller_user = get_seller_user_by_query(query_id)
    if seller_user:
        send_sms_to_user_id(seller_user.id, query_keys.buyer_save_query_seller_key, query_id=query_id)


def send_accept_query_notification(query_id):
    buyer_user = get_buyer_user_by_query(query_id)
    if buyer_user:
        send_sms_to_user_id(buyer_user.id, query_keys.seller_accept_query_buyer_key, query_id=query_id)
    seller_user = get_seller_user_by_query(query_id)
    if seller_user:
        send_sms_to_user_id(seller_user.id, query_keys.seller_accept_query_seller_key, query_id=query_id)


def send_resolve_query_notification(user_id, query_id):
    send_sms_to_user_id(user_id, query_keys.buyer_resolve_query_buyer_key, query_id=query_id)
    seller_user = get_seller_user_by_query(query_id)
    if seller_user:
        send_sms_to_user_id(seller_user.id, query_keys.buyer_resolve_query_seller_key, query_id=query_id)
