from farmzone.order.models import OrderDetail, Orders
from collections import OrderedDict
from farmzone.util_config.db import execute_query
from farmzone.util_config import generate_public_s3_access_url, utc_standard_format_to_preferred_tz_timestp
import logging
logger = logging.getLogger(__name__)


seller_order_general_sql = """
select p.product_code, sp.name as sub_product_name, s.seller_code, s.name as seller_name
, sp.sub_product_code, p.name as product_name, c.name as category_name , c.category_code as category_code
, p.img_orig as product_img_orig, sp.img_orig as sub_product_img_orig
, p.img_thumb as product_img_thumb, sp.img_thumb as sub_product_img_thumb
, o.total_price, od.price, od.discount, od.status, od.qty, o.id, o.created_at 
, u.full_name, u.email, ph.phone_number
from orders o inner join order_detail od on o.id=od.order_id 
inner join seller_sub_product ssp on ssp.id=od.seller_sub_product_id 
inner join sub_product sp on sp.id=ssp.sub_product_id inner join product p on p.id=sp.product_id 
inner join product_category c on c.id=p.product_category_id 
inner join sellers s on ssp.seller_id=s.id
inner join users u on o.user_id=u.id
inner join phone_numbers ph on ph.user_id=u.id
where 1=1 
"""


def format_orders(result, product_count_map=None, offset=None, count=None):
    order_map = OrderedDict()
    for item in result:
        if item.id not in order_map:
            order_map[item.id] = {"products": []}
        order = order_map[item.id]
        order["id"] = item.id
        order["total_price"] = item.total_price
        order["created_at"] = utc_standard_format_to_preferred_tz_timestp(item.created_at)
        order["user"] = {"full_name": item.full_name, "email": item.email, "phone_number": item.phone_number}
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
        products.append(sub_product_map)
    orders = []
    for key in order_map:
        orders.append(order_map[key])
    return orders[offset:count] if (offset is not None and count is not None) else orders


seller_upcoming_orders_sql = seller_order_general_sql + """
and s.seller_code='{0}' and od.status!='COMPLETED' 
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
