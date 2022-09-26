import functools
from datetime import datetime
import pytz
from django.db import connection


def query_debugger(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        queries = connection.queries
        execution_time = 0
        print(f'\nQuery at: {datetime.now(tz=pytz.timezone("Europe/Kiev"))}')
        print('------------------------------------------------------------------')
        for query in queries:
            print('\t\t', query['sql'].replace('"', ''))
            execution_time += float(query['time'])
        print('------------------------------------------------------------------')
        print(f'Queries number: {len(queries)}')
        print(f'Execution time: {execution_time}')

        return result

    return wrapper
