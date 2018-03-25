from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from farmzone.settings.common import PAGINATION_DEFAULT_PER_PAGE_RECORD_COUNT

class CustomPagination(PageNumberPagination):
    """Custom Paginator class which extends DRF\'s Pagination to
    allow specifying page_size in APIs
    """
    page_size = PAGINATION_DEFAULT_PER_PAGE_RECORD_COUNT
    page_size_query_param = 'page_size'
    max_page_size = 1000

