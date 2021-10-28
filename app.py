from flask import Flask, jsonify, render_template
from errors import NotFoundError, BadRequestError, ValidationError
from utils import run_plain_sql, make_results

app = Flask(__name__)


# uid = 5000
sql = '''
        select animal_type, name, date_of_birth, outcome_date,
            b.breed as breed1, bb.breed as breed2,
            c.color as color1, cc.color as color2,
            o.outcome_subtype, ot.outcome_type
        from animals_OPT a
            left join breeds b on a.breed1_id = b.id
            left join breeds bb on a.breed2_id = bb.id
            left join colors c on a.color1_id = c.id
            left join colors cc on a.color2_id = cc.id
            left join outcome_subtypes o on a.outcome_subtype_id = o.id
            left join outcome_types ot on a.outcome_type_id = ot.id
        where animal_id = {}
'''
sql2 = '''
        select animal_type,
            name,
            date_of_birth,
            outcome_date,
            b.breed as breed1,
            bb.breed as breed2,
            c.color as color1,
            cc.color as color2,
            o.outcome_subtype,
            ot.outcome_type
        from 
        (select * from animals_OPT where animal_id = {}) a
            left join breeds b on a.breed1_id = b.id
            left join breeds bb on a.breed2_id = bb.id
            left join colors c on a.color1_id = c.id
            left join colors cc on a.color2_id = cc.id
            left join outcome_subtypes o on a.outcome_subtype_id = o.id
            left join outcome_types ot on a.outcome_type_id = ot.id
'''
sql3 = '''
        with subquery as (select * from animals_OPT where animal_id = {})
        select animal_type, name, date_of_birth, outcome_date,
            b.breed as breed1, bb.breed as breed2,
            c.color as color1, cc.color as color2,
            o.outcome_subtype, ot.outcome_type
        from subquery a
            left join breeds b on a.breed1_id = b.id
            left join breeds bb on a.breed2_id = bb.id
            left join colors c on a.color1_id = c.id
            left join colors cc on a.color2_id = cc.id
            left join outcome_subtypes o on a.outcome_subtype_id = o.id
            left join outcome_types ot on a.outcome_type_id = ot.id
'''
SQL = '''
    select animal_type, name, date_of_birth, outcome_date,
        b.breed as breed1, bb.breed as breed2,
        c.color as color1, cc.color as color2,
        o.outcome_subtype, ot.outcome_type
    from animals_OPT a
        left join breeds b on a.breed1_id = b.id
        left join breeds bb on a.breed2_id = bb.id
        left join colors c on a.color1_id = c.id
        left join colors cc on a.color2_id = cc.id
        left join outcome_subtypes o on a.outcome_subtype_id = o.id
        left join outcome_types ot on a.outcome_type_id = ot.id
    where animal_id = {}
    '''


@app.errorhandler(404)
@app.errorhandler(NotFoundError)
def not_found_error(error):
    return 'Not found', 404


@app.errorhandler(BadRequestError)
def not_found_error(error):
    return 'Bad request', 400


@app.errorhandler(ValidationError)
def validation_error(error):
    return 'Validation error', 400


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/card/<int:uid>')
def shows_card_by_id(uid: int):
    if not (results := run_plain_sql(SQL.format(uid))):
        raise NotFoundError
    return render_template('animal_card.html',
                           card=make_results('Animal type', 'Name', 'Date of birth', 'Outcome date', 'Breed 1',
                                             'Breed 2', 'Color 1', 'Color 2', 'Outcome subtype', 'Outcome type',
                                             data=results)[0])


@app.route('/<int:uid>')
def shows_by_id(uid: int):
    if not (results := run_plain_sql(SQL.format(uid))):
        raise NotFoundError
    return jsonify(make_results('Animal type', 'Name', 'Date of birth', 'Outcome date', 'Breed 1', 'Breed 2',
                                'Color 1', 'Color 2', 'Outcome subtype', 'Outcome type', data=results))


@app.route('/breeds/')
def shows_breeds():
    if not (results := run_plain_sql('''
    select distinct breed
    from breeds
    order by breed    
    ''')):
        raise NotFoundError
    return render_template('breeds.html', breeds=make_results('Breed', data=results))


@app.route('/colors/')
def shows_colors():
    if not (results := run_plain_sql('''
    select distinct color
    from colors
    order by color    
    ''')):
        raise NotFoundError
    return render_template('colors.html', colors=make_results('Color', data=results))


@app.route('/search/', methods=['GET', 'POST'])
def search():
    return render_template('search.html')


if __name__ == '__main__':
    app.run()

    # DEBUG and PROFILE -----
    # import time
    # uid = 3

    # results = run_sql('''
    # select *
    # from colors --animals_OPT
    # --limit 10
    # ''')
    # print(results)

    # 0.000778s
    # t0 = time.perf_counter()
    # results = run_sql(sql.format(uid))
    # elapsed = time.perf_counter() - t0
    # print(results)
    # print('SQL:\t[%0.8fs]' % elapsed)

    # 0.000807s
    # t0 = time.perf_counter()
    # results = run_sql(sql2.format(uid))
    # elapsed = time.perf_counter() - t0
    # # print(results)
    # print('SQL2:\t[%0.8fs]' % elapsed)

    # 0.000819s
    # t0 = time.perf_counter()
    # results = run_sql(sql3.format(uid))
    # elapsed = time.perf_counter() - t0
    # # print(results)
    # print('SQL3:\t[%0.8fs]' % elapsed)
