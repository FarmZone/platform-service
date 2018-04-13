from farmzone.util_config.db import execute_query
from farmzone.sellers.models import SellerSubProduct
from farmzone.util_config import generate_public_s3_access_url, str_to_key_value
from django.db.models import Count
from collections import OrderedDict
import logging
logger = logging.getLogger(__name__)

seller_product_general_sql = """
select p.product_code, sp.name as sub_product_name, s.seller_code, s.name as seller_name
, sp.sub_product_code, p.name as product_name, c.name as category_name, ssp.price , c.category_code as category_code
, p.img_orig as product_img_orig, sp.img_orig as sub_product_img_orig
, p.img_thumb as product_img_thumb, sp.img_thumb as sub_product_img_thumb, null as specifications 
from sellers s inner join seller_sub_product ssp on ssp.seller_id=s.id 
inner join sub_product sp on sp.id=ssp.sub_product_id inner join product p on p.id=sp.product_id 
inner join product_category c on c.id=p.product_category_id 
where s.is_active=1 and ssp.is_active=1 
"""


def format_products(result, product_count_map=None, offset=None, count=None):
    product_map = OrderedDict()
    for item in result:
        if item.category_name not in product_map:
            product_map[item.category_name] = {"products": OrderedDict()}
        category = product_map[item.category_name]
        category["category_name"] = item.category_name
        category["category_code"] = item.category_code
        if product_count_map and product_count_map[item.category_code]:
            category["product_count"] = product_count_map[item.category_code]
        products = category["products"]
        if item.product_code not in products:
            products[item.product_code] = {"sub_products": []}
        product = products[item.product_code]
        product["product_name"] = item.product_name
        product["product_code"] = item.product_code
        product["img_orig"] = generate_public_s3_access_url(item.product_img_orig)
        product["img_thumb"] = generate_public_s3_access_url(item.product_img_thumb)
        sub_products = product["sub_products"]
        sub_product_map = {}
        sub_product_map["seller_code"] = item.seller_code
        sub_product_map["seller_name"] = item.seller_name
        sub_product_map["price"] = item.price
        sub_product_map["sub_product_code"] = item.sub_product_code
        sub_product_map["sub_product_name"] = item.sub_product_name
        sub_product_map["img_orig"] = generate_public_s3_access_url(item.sub_product_img_orig)
        sub_product_map["img_thumb"] = generate_public_s3_access_url(item.sub_product_img_thumb)
        sub_product_map["specifications"] = str_to_key_value(item.specifications) if item.specifications else {}
        sub_products.append(sub_product_map)
    categories = []
    for key in product_map:
        cats = product_map[key]["products"]
        prod_list = []
        for k in cats:
            prods = cats[k]
            prod_list.append(prods)
        product_map[key]["products"] = prod_list[offset:count] if (offset is not None and count is not None) else prod_list
        categories.append(product_map[key])
    return categories


seller_products_sql = seller_product_general_sql + """
and (select count(distinct pi.id) from product pi inner join sub_product spi on pi.id=spi.product_id 
inner join seller_sub_product sspi on spi.id=sspi.sub_product_id inner join sellers si on si.id=sspi.seller_id 
where pi.product_category_id=p.product_category_id and si.is_active=1 and sspi.is_active=1  and si.id=s.id and pi.id<p.id)<5
and s.seller_code='{0}'
"""


def get_seller_products_summary(seller_code):
    product_count_map = get_product_count(seller_code)
    result = execute_query(seller_products_sql.format(seller_code))
    logger.debug("seller {0} products {1}".format(seller_code, result))
    return format_products(result, product_count_map)


def get_buyer_products_summary(seller_code):
    return get_seller_products_summary(seller_code)


def get_product_count(seller_code):
    product_counts = SellerSubProduct.objects.filter(is_active=True, seller__is_active=True,
                                                    seller__seller_code=seller_code) \
        .values('sub_product__product__product_category__category_code') \
        .annotate(product_count=Count('sub_product__product__product_code', distinct=True))
    #logger.debug("product_count {0}".format(list(product_counts)))
    product_count_map = {}
    for item in product_counts:
        product_count_map[item['sub_product__product__product_category__category_code']]= item['product_count']
    logger.debug("product_count_map {0}".format(product_count_map))
    return product_count_map


seller_products_by_category_sql = seller_product_general_sql + """
and s.seller_code='{0}' and c.category_code='{1}'
"""


def get_seller_products_by_category(seller_code, category_code, offset, count):
    result = execute_query(seller_products_by_category_sql.format(seller_code, category_code))
    #logger.debug("seller {0}, category_code {1} products {2}".format(seller_code, category_code, result))
    return format_products(result, None, offset, count)


def get_buyer_products_by_category(seller_code, category_code, offset, count):
    return get_seller_products_by_category(seller_code, category_code, offset, count)


seller_product_detail_sql = """
select max(p.product_code) as product_code, max(sp.name) as sub_product_name, max(s.seller_code) as seller_code
, max(s.name) as seller_name, max(sp.sub_product_code) as sub_product_code, max(p.name) as product_name
, max(c.name) as category_name, max(ssp.price) as price, max(c.category_code) as category_code
, max(p.img_orig) as product_img_orig, max(sp.img_orig) as sub_product_img_orig
, max(p.img_thumb) as product_img_thumb, max(sp.img_thumb) as sub_product_img_thumb 
, group_concat(concat(spd.key,':', spd.value)) as specifications 
from sellers s inner join seller_sub_product ssp on ssp.seller_id=s.id 
inner join sub_product sp on sp.id=ssp.sub_product_id inner join product p on p.id=sp.product_id 
inner join product_category c on c.id=p.product_category_id 
left join sub_product_detail spd on sp.id=spd.sub_product_id 
where s.is_active=1 and ssp.is_active=1 
""" + """
and s.seller_code='{0}' and p.product_code='{1}' group by sp.id 
"""


def get_seller_product_detail(seller_code, product_code):
    result = execute_query(seller_product_detail_sql.format(seller_code, product_code))
    logger.debug("seller {0}, product_code {1} product_detail {2}".format(seller_code, product_code, result))
    return format_products(result)


def get_buyer_product_detail(seller_code, product_code):
    return get_seller_product_detail(seller_code, product_code)


cart_detail_sql = seller_product_general_sql + """
and ssp.id in ({0})
"""


def get_cart_product_detail(seller_subproduct_ids):
    result = execute_query(cart_detail_sql.format(seller_subproduct_ids))
    logger.debug("seller_subproduct_ids {0} & Cart detail {1}".format(seller_subproduct_ids, result))
    return format_products(result)