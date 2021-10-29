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


def get_full_record(uid: int) -> dict:
    sql = '''
        with breeds_lst as (
            select animal_id, 
                group_concat(b.breed, '/') breed_lst
            from animals_breeds ab
                left join breeds b on ab.breed_id = b.id
            group by 1
            ),
        colors_lst as (
            select animal_id,
                group_concat(c.color, '/') color_lst
            from animals_colors ac
                left join colors c on ac.color_id = c.id
            group by 1
            )
        select at.animal_type animal_type,
            name,
            date_of_birth,
            outcome_date,
            o.outcome_subtype,
            ot.outcome_type,
            color_lst,
            breed_lst
        from animals_OPT a
            left join outcome_subtypes o on a.outcome_subtype_id = o.id
            left join outcome_types ot on a.outcome_type_id = ot.id
            left join animal_types at on a.animal_type_id = at.id
            left join colors_lst using (animal_id)
            left join breeds_lst using (animal_id)
        where animal_id = {}
        '''
    if not (results := run_plain_sql(sql.format(uid))):
        raise NotFoundError
    return make_results('Animal type', 'Name', 'Date of birth', 'Outcome date', 'Outcome subtype', 'Outcome type',
                        'Color', 'Breed', data=results)[0]
