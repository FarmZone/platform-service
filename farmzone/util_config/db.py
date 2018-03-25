from django.db import connection
from collections import namedtuple
import logging

logger = logging.getLogger(__name__)


def execute_query(query):
    with connection.cursor() as c:
        c.execute(query)
        result = fetch_results(c)
        return result


def fetch_results(cursor):
    "Return all rows from a cursor as a namedtuple"
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]