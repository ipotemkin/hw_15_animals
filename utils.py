import sqlite3
import prettytable
from errors import ValidationError


def run_plain_sql(sql_: str) -> list:
    with sqlite3.connect('animal.db') as conn:
        cur = conn.cursor()
        return cur.execute(sql_).fetchall()


def run_sql(sql_: str) -> 'prettytable.prettytable.PrettyTable':
    with sqlite3.connect('animal.db') as conn:
        cur = conn.cursor()
        results = cur.execute(sql_)
        my_table = prettytable.from_db_cursor(results)
        my_table.max_width = 30
        return my_table


def make_results(*fields: str, data: list) -> list:
    if len(fields) != len(data[0]):
        raise ValidationError
    results = []
    for line in data:
        results_line = {}
        for i, field in enumerate(fields):
            results_line[field] = line[i]
        results.append(results_line)
    return results


def get_colors_by_animal_id(uid: int) -> str:
    sql_colors_by_animal_id = '''
        select color
        from animals_OPT a
            left join animals_colors ac using (animal_id)
            left join colors c on ac.color_id = c.id
        where animal_id = {} and color is not null     
    '''
    result = run_plain_sql(sql_colors_by_animal_id.format(uid))
    colors_lst = [color[0] for color in result]
    return ', '.join(colors_lst)
