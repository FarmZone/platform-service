

def get_seller_order_notification_type(order_id, order_status):
    return {
        'NEW': 'You have received a new order {0}'.format(order_id),
        'ACCEPTED': 'You have accepted item(s) in order {0}'.format(order_id),
        'REJECTED': 'You have rejected item(s) in order {0}'.format(order_id),
        'COMPLETED': 'You have delivered item(s) in order {0}'.format(order_id),
        'DISPATCHED': 'You have dispatched item(s) in order {0}'.format(order_id),
        'CANCELLED': 'Buyer has cancelled order {0}'.format(order_id),
    }.get(order_status)


def get_buyer_order_notification_type(order_id, order_status):
    return {
        'NEW': 'You have placed a new order {0}'.format(order_id),
        'ACCEPTED': 'Seller has accepted item(s) in order {0}'.format(order_id),
        'REJECTED': 'Seller has rejected item(s) in order {0}'.format(order_id),
        'COMPLETED': 'Seller has delivered item(s) in order {0}'.format(order_id),
        'DISPATCHED': 'Seller has dispatched item(s) in order {0}'.format(order_id),
        'CANCELLED': 'You have cancelled your order {0}'.format(order_id),
    }.get(order_status)


def get_seller_complain_notification_type(query_id, query_status):
    return {
        'NEW': 'You have received a new complain/service request {0}'.format(query_id),
        'ACCEPTED': 'You have accepted complain/service request {0}'.format(query_id),
        'REJECTED': 'You have rejected complain/service request {0}'.format(query_id),
        'RESOLVED': 'You have resolved complain/service request {0}'.format(query_id),
    }.get(query_status)


def get_buyer_complain_notification_type(query_id, query_status):
    return {
        'NEW': 'You have raised a new complain/service request {0}'.format(query_id),
        'ACCEPTED': 'Seller has accepted complain/service request {0}'.format(query_id),
        'REJECTED': 'Seller has rejected complain/service request {0}'.format(query_id),
        'RESOLVED': 'Seller has resolved complain/service request {0}'.format(query_id),
    }.get(query_status)
