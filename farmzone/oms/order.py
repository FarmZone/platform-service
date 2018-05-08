from farmzone.order.models import OrderDetail, OrderStatus, Orders, ORDER_CANCELLED_STATUS, OrderDetailProductIdentifier
from farmzone.util_config.custom_exceptions import CustomAPI400Exception
from collections import OrderedDict
from farmzone.util_config.db import execute_query
from farmzone.util_config import generate_public_s3_access_url, utc_standard_format_to_preferred_tz_timestp
from django.db import transaction
from django.db.models import Sum, F, DecimalField
import logging
import decimal
import arrow
from farmzone.notification import notification
from farmzone.sellers.models import SellerOwner
logger = logging.getLogger(__name__)


seller_order_general_sql = """
select p.product_code, p.name as product_name, p.img_orig as product_img_orig, p.img_thumb as product_img_thumb
, sp.name as sub_product_name, sp.sub_product_code, sp.img_orig as sub_product_img_orig, sp.img_thumb as sub_product_img_thumb
, s.seller_code, s.name as seller_name
, c.name as category_name , c.category_code as category_code
, o.total_price, od.price, od.discount, od.status, od.qty, o.id, od.created_at, od.id as order_detail_id, od.seller_sub_product_id  
, u.full_name, u.email, ph.phone_number 
, a.address_line1, a.address_line2, a.address_line3, sc.name as state
from orders o inner join order_detail od on o.id=od.order_id 
inner join seller_sub_product ssp on ssp.id=od.seller_sub_product_id 
inner join sub_product sp on sp.id=ssp.sub_product_id inner join product p on p.id=sp.product_id 
inner join product_category c on c.id=p.product_category_id 
inner join sellers s on ssp.seller_id=s.id
inner join users u on o.user_id=u.id
left join address a on u.id=a.user_id
left join state_codes sc on sc.id=a.state_id
inner join phone_numbers ph on ph.user_id=u.id
where 1=1 
"""


def format_orders(result, product_count_map=None, offset=None, count=None):
    order_map = OrderedDict()
    for item in result:
        if item.id not in order_map:
            order_map[item.id] = {"products": [], "total_price": decimal.Decimal(0.0)}
        order = order_map[item.id]
        order["id"] = item.id
        order["created_at"] = utc_standard_format_to_preferred_tz_timestp(item.created_at)
        order["user"] = {"full_name": item.full_name, "email": item.email, "phone_number": item.phone_number,
                         "address": {"address_line1":item.address_line1 if item.address_line1 else ""
                             , "address_line2":item.address_line2 if item.address_line2 else ""
                             , "address_line3":item.address_line3 if item.address_line3 else "", "state":item.state }}
        if product_count_map and product_count_map[item.id]:
            order["product_count"] = product_count_map[item.id]
        products = order["products"]
        sub_product_map = {}
        sub_product_map["product_name"] = item.product_name
        sub_product_map["product_code"] = item.product_code
        sub_product_map["product_img_orig"] = generate_public_s3_access_url(item.product_img_orig)
        sub_product_map["product_img_thumb"] = generate_public_s3_access_url(item.product_img_thumb)
        sub_product_map["seller_code"] = item.seller_code
        sub_product_map["seller_name"] = item.seller_name
        sub_product_map["sub_product_code"] = item.sub_product_code
        sub_product_map["sub_product_name"] = item.sub_product_name
        sub_product_map["sub_product_img_orig"] = generate_public_s3_access_url(item.sub_product_img_orig)
        sub_product_map["sub_product_img_thumb"] = generate_public_s3_access_url(item.sub_product_img_thumb)
        sub_product_map["price"] = item.price
        sub_product_map["discount"] = item.discount
        sub_product_map["status"] = item.status
        sub_product_map["qty"] = item.qty
        logger.debug("order {0} before total {1}".format(order["id"], order["total_price"]))
        if item.price is not None and item.qty is not None:
            cal_price = ((item.price - (item.discount if item.discount else decimal.Decimal(0.0))) * item.qty)
            order["total_price"] = order["total_price"] + cal_price
            logger.debug("order {0} calculated price {1}".format(order["id"], cal_price))
        sub_product_map["order_detail_id"] = item.order_detail_id
        sub_product_map["seller_sub_product_id"] = item.seller_sub_product_id
        logger.debug("order {0} after total {1}".format(order["id"], order["total_price"]))
        products.append(sub_product_map)
    orders = []
    for key in order_map:
        orders.append(order_map[key])
    return orders[offset:count] if (offset is not None and count is not None) else orders


seller_upcoming_orders_sql = seller_order_general_sql + """
and s.seller_code='{0}' and od.status not in ('COMPLETED', 'CART', 'CANCELLED') 
order by od.created_at desc
"""


def get_seller_upcoming_orders(seller_code, offset, count):
    result = execute_query(seller_upcoming_orders_sql.format(seller_code))
    return format_orders(result, None, offset, count)


seller_completed_orders_sql = seller_order_general_sql + """
and s.seller_code='{0}' and od.status='COMPLETED' 
order by od.created_at desc
"""


def get_seller_completed_orders(seller_code, offset, count):
    result = execute_query(seller_completed_orders_sql.format(seller_code))
    return format_orders(result, None, offset, count)


buyer_upcoming_orders_sql = seller_order_general_sql + """
and o.user_id='{0}' and od.status not in ('COMPLETED', 'CART', 'CANCELLED')
order by od.created_at desc
"""


def get_buyer_upcoming_orders(user_id, offset, count):
    result = execute_query(buyer_upcoming_orders_sql.format(user_id))
    return format_orders(result, None, offset, count)


buyer_completed_orders_sql = seller_order_general_sql + """
and o.user_id='{0}' and od.status='COMPLETED' 
order by od.created_at desc
"""


def get_buyer_completed_orders(user_id, offset, count):
    result = execute_query(buyer_completed_orders_sql.format(user_id))
    return format_orders(result, None, offset, count)


cart_detail_sql = """
select p.product_code, p.name as product_name, p.img_orig as product_img_orig, p.img_thumb as product_img_thumb
, sp.name as sub_product_name, sp.sub_product_code, sp.img_orig as sub_product_img_orig, sp.img_thumb as sub_product_img_thumb
, s.seller_code, s.name as seller_name
, c.name as category_name , c.category_code as category_code
, o.total_price, ssp.price, ssp.discount, od.status, od.qty, o.id, od.created_at, od.id as order_detail_id, od.seller_sub_product_id 
, u.full_name, u.email, ph.phone_number 
, a.address_line1, a.address_line2, a.address_line3, sc.name as state
from orders o inner join order_detail od on o.id=od.order_id 
inner join seller_sub_product ssp on ssp.id=od.seller_sub_product_id 
inner join sub_product sp on sp.id=ssp.sub_product_id inner join product p on p.id=sp.product_id 
inner join product_category c on c.id=p.product_category_id 
inner join sellers s on ssp.seller_id=s.id
inner join users u on o.user_id=u.id
left join address a on u.id=a.user_id
left join state_codes sc on sc.id=a.state_id
inner join phone_numbers ph on ph.user_id=u.id
where s.is_active=1 and ssp.is_active=1 and o.user_id='{0}' and od.status='CART' 
"""


def get_cart_product_detail(user_id):
    result = execute_query(cart_detail_sql.format(user_id))
    total_price = get_total_price(result)
    logger.debug("seller_subproduct_ids {0} & Cart detail {1} & total {2}".format(user_id, result, total_price))
    orders = format_orders(result)
    if orders:
        orders[0]["total_price"] = total_price
    return orders


def get_total_price(result):
    total_price = decimal.Decimal(0.0)
    for item in result:
        price = item.price
        discount = item.discount
        qty = item.qty
        logger.debug("p={0}, d={1}, q={2}, t{3}".format(type(price),type(discount), type(qty), type(total_price)))
        if price and qty:
            total_price = total_price + ((price - (discount if discount else decimal.Decimal(0.0))) * qty)
            logger.debug("t={0}".format(total_price))
    return total_price


def place_order(user_id, id):
    item_count = OrderDetail.objects.filter(order_id=id, order__user_id=user_id, status=OrderStatus.CART.value).count()
    if item_count == 0:
        raise CustomAPI400Exception({
            "details": "Given id is not a valid cart id for this user or item in cart is zero",
            "status_code": "INVALID_REQUIRED_FIELDS"
        })
    total_price = OrderDetail.objects.filter(order_id=id, order__user_id=user_id, status=OrderStatus.CART.value)\
        .aggregate(total_price=Sum((F('price')-F('discount'))*F('qty'), output_field=DecimalField()))
    logger.debug("total {0}".format(total_price))
    now = arrow.utcnow().datetime
    with transaction.atomic():
        OrderDetail.objects.filter(order_id=id, order__user_id=user_id, status=OrderStatus.CART.value)\
            .update(status=OrderStatus.NEW.value, created_at=now, updated_at=now)
        if total_price and total_price["total_price"]:
            Orders.objects.filter(id=id, user_id=user_id)\
                .update(total_price=total_price["total_price"], created_at=now, updated_at=now)
    seller_user_ids = get_seller_users_by_order(id)
    notification.send_place_order_notification(user_id, id, seller_user_ids)


def cancel_order(user_id, id):
    item_count = OrderDetail.objects.filter(order_id=id, order__user_id=user_id, status__in=ORDER_CANCELLED_STATUS).count()
    if item_count == 0:
        raise CustomAPI400Exception({
            "details": "Given id is not a valid order id for this user or item in order is zero",
            "status_code": "INVALID_REQUIRED_FIELDS"
        })
    with transaction.atomic():
        OrderDetail.objects.filter(order_id=id, order__user_id=user_id, status__in=ORDER_CANCELLED_STATUS)\
            .update(status=OrderStatus.CANCELLED.value)
    seller_user_ids = get_seller_users_by_order(id)
    notification.send_cancel_order_notification(user_id, id, seller_user_ids)


def save_order_rating(order_detail_id, rating, user_id):
    order_detail = OrderDetail.objects.filter(id=order_detail_id, order__user_id=user_id).first()
    if not order_detail:
        raise CustomAPI400Exception({
            "details": "Given id is not a valid order id for this user or item in order is zero",
            "status_code": "INVALID_REQUIRED_FIELDS"
        })
    with transaction.atomic():
        order_detail.rating = rating
        order_detail.save()


def accept_order(order_detail_id, seller_code):
    order_detail = OrderDetail.objects.filter(id=order_detail_id, seller_sub_product__seller__seller_code=seller_code).first()
    if not order_detail:
        logger.info("order_detail_id does not match any order detail {0} for given seller {1}".format(order_detail_id, seller_code))
        raise CustomAPI400Exception({
            "details": "Given order_detail_id is not a valid id for this seller",
            "status_code": "INVALID_REQUIRED_FIELDS"
        })
    if order_detail.status != OrderStatus.NEW.value:
        logger.info("Order status is not in New state to accept {0}".format(order_detail.status))
        raise CustomAPI400Exception({
            "details": "Order Detail is not in valid state of New",
            "status_code": "INVALID_ORDER_DETAIL_STATE"
        })
    logger.info("Processing Request to accept order detail for seller {0}".format(seller_code))
    with transaction.atomic():
        order_detail.status = OrderStatus.ACCEPTED.value
        order_detail.save()
    order = get_order_by_order_detail(order_detail_id)
    seller_user = get_seller_user_by_order_detail(order_detail_id)
    buyer_user = get_buyer_user_by_order_detail(order_detail_id)
    notification.send_accept_order_notification(order_detail_id, order, buyer_user, seller_user)


def dispatch_order(order_detail_id, seller_code):
    order_detail = OrderDetail.objects.filter(id=order_detail_id, seller_sub_product__seller__seller_code=seller_code).first()
    if not order_detail:
        logger.info("order_detail_id does not match any order detail {0} for given seller {1}".format(order_detail_id, seller_code))
        raise CustomAPI400Exception({
            "details": "Given order_detail_id is not a valid id for this seller",
            "status_code": "INVALID_REQUIRED_FIELDS"
        })
    if order_detail.status != OrderStatus.ACCEPTED.value:
        logger.info("Order status is not in Accept state to dispatch {0}".format(order_detail.status))
        raise CustomAPI400Exception({
            "details": "Order Detail is not in valid state of Accept",
            "status_code": "INVALID_ORDER_DETAIL_STATE"
        })
    logger.info("Processing Request to dispatch order detail for seller {0}".format(seller_code))
    with transaction.atomic():
        order_detail.status = OrderStatus.DISPATCHED.value
        order_detail.save()
    order = get_order_by_order_detail(order_detail_id)
    seller_user = get_seller_user_by_order_detail(order_detail_id)
    buyer_user = get_buyer_user_by_order_detail(order_detail_id)
    notification.send_dispatch_order_notification(order_detail_id, order, buyer_user, seller_user)


def complete_order(order_detail_id, user_id, product_identifiers):
    order_detail = OrderDetail.objects.filter(id=order_detail_id, order__user_id=user_id).first()
    if not order_detail:
        logger.info("order_detail_id does not match any order detail {0} for given user {1}".format(order_detail_id, user_id))
        raise CustomAPI400Exception({
            "details": "Given order_detail_id is not a valid id for this user",
            "status_code": "INVALID_REQUIRED_FIELDS"
        })
    if order_detail.status != OrderStatus.DISPATCHED.value:
        logger.info("Order status is not in dispatched state to complete {0}".format(order_detail.status))
        raise CustomAPI400Exception({
            "details": "Order Detail is not in valid state of Dispatched",
            "status_code": "INVALID_ORDER_DETAIL_STATE"
        })
    logger.info("product_identifiers {0}".format(product_identifiers))
    logger.info("Processing Request to complete order for user {0}".format(user_id))
    duplicate = OrderDetailProductIdentifier.objects.filter(product_identifier__in=product_identifiers).first()
    if duplicate:
        logger.info("Product Identifiers already exists {0}".format(product_identifiers))
        raise CustomAPI400Exception({
            "details": "Product Identifiers already exists",
            "status_code": "INVALID_PRODUCT_IDENTIFIER"
        })
    with transaction.atomic():
        order_detail.status = OrderStatus.COMPLETED.value
        order_detail.save()
        for product_identifier in product_identifiers:
            OrderDetailProductIdentifier.add_order_detail_product_identifier(order_detail_id, product_identifier)
    order = get_order_by_order_detail(order_detail_id)
    seller_user = get_seller_user_by_order_detail(order_detail_id)
    buyer_user = get_buyer_user_by_order_detail(order_detail_id)
    notification.send_complete_order_notification(order_detail_id, order, buyer_user, seller_user)


def get_seller_user_by_order_detail(order_detail_id):
    order_detail = OrderDetail.objects.select_related("seller_sub_product", "seller_sub_product__seller").filter(id=order_detail_id).first()
    if order_detail:
        seller = order_detail.seller_sub_product.seller
        if seller:
            seller_owner = SellerOwner.objects.select_related("user").filter(seller=seller).first()
            if seller_owner:
                return seller_owner.user
    return None


def get_buyer_user_by_order_detail(order_detail_id):
    order_detail = OrderDetail.objects.select_related("order", "order__user").filter(id=order_detail_id).first()
    if order_detail:
        return order_detail.order.user
    return None


def get_order_by_order_detail(order_detail_id):
    order_detail = OrderDetail.objects.select_related("order").filter(id=order_detail_id).first()
    if order_detail:
        return order_detail.order
    return None


def get_seller_users_by_order(order_id):
    seller_ids = OrderDetail.objects.filter(order_id=order_id).values_list("seller_sub_product__seller__id")
    if seller_ids:
        seller_users = SellerOwner.objects.filter(seller_id__in=seller_ids).values_list("user__id",flat=True).distinct()
        seller_users = list(seller_users)
        logger.debug("seller users {0}".format(seller_users))
        return seller_users
    return None