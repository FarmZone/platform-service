from farmzone.order.models import OrderDetail, OrderStatus, Orders, ORDER_CANCELLED_STATUS
from farmzone.util_config.custom_exceptions import CustomAPI400Exception
from collections import OrderedDict
from farmzone.util_config.db import execute_query
from farmzone.util_config import generate_public_s3_access_url, utc_standard_format_to_preferred_tz_timestp
from django.db import transaction
from django.db.models import Sum, F, DecimalField
import logging
import decimal
import arrow
logger = logging.getLogger(__name__)


seller_order_general_sql = """
select p.product_code, p.name as product_name, p.img_orig as product_img_orig, p.img_thumb as product_img_thumb
, sp.name as sub_product_name, sp.sub_product_code, sp.img_orig as sub_product_img_orig, sp.img_thumb as sub_product_img_thumb
, s.seller_code, s.name as seller_name
, c.name as category_name , c.category_code as category_code
, o.total_price, od.price, od.discount, od.status, od.qty, o.id, od.created_at, od.id as order_detail_id  
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
                         "address": {"address_line1":item.address_line1, "address_line2":item.address_line2
                             , "address_line3":item.address_line3, "state":item.state }}
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
, o.total_price, ssp.price, ssp.discount, od.status, od.qty, o.id, od.created_at, od.id as order_detail_id  
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
