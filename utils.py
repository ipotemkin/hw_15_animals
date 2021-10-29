import sqlite3
import prettytable
from errors import ValidationError, NotFoundError


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
    return '/'.join(colors_lst)


def get_breeds_by_animal_id(uid: int) -> str:
    sql_breeds_by_animal_id = '''
        select breed
        from animals_OPT a
            left join animals_breeds ac using (animal_id)
            left join breeds b on ac.breed_id = b.id
        where animal_id = {} and breed is not null     
    '''
    result = run_plain_sql(sql_breeds_by_animal_id.format(uid))
    breeds_lst = [breed[0] for breed in result]
    return '/'.join(breeds_lst)


def get_full_record(uid: int) -> dict:
    sql = '''
        select at.animal_type animal_type,
            name,
            date_of_birth,
            outcome_date,
            o.outcome_subtype,
            ot.outcome_type
        from animals_OPT a
            left join outcome_subtypes o on a.outcome_subtype_id = o.id
            left join outcome_types ot on a.outcome_type_id = ot.id
            left join animal_types at on a.animal_type_id = at.id
        where animal_id = {}
        '''
    if not (results := run_plain_sql(sql.format(uid))):
        raise NotFoundError
    results_with_names = make_results('Animal type', 'Name', 'Date of birth', 'Outcome date', 'Outcome subtype',
                                      'Outcome type', data=results)
    results_with_names[0]['Color'] = get_colors_by_animal_id(uid)
    results_with_names[0]['Breed'] = get_breeds_by_animal_id(uid)
    return results_with_names[0]
