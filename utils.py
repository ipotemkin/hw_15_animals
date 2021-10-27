import sqlite3
import prettytable
from errors import ValidationError


def run_plain_sql(sql_):
    with sqlite3.connect('animal.db') as conn:
        cur = conn.cursor()
        return cur.execute(sql_).fetchall()


def run_sql(sql_):
    with sqlite3.connect('animal.db') as conn:
        cur = conn.cursor()
        results = cur.execute(sql_)
        my_table = prettytable.from_db_cursor(results)
        my_table.max_width = 30
        return my_table


def make_results(*fields, data: list):
    if len(fields) != len(data[0]):
        raise ValidationError
    results = []
    for line in data:
        results_line = {}
        for i, field in enumerate(fields):
            results_line[field] = line[i]
        results.append(results_line)
    return results
