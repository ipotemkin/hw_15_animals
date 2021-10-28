from flask import Flask, jsonify, render_template
from errors import NotFoundError, BadRequestError, ValidationError
from utils import run_plain_sql, make_results, get_colors_by_animal_id, get_breeds_by_animal_id

app = Flask(__name__)


SQL = '''
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
    results_with_names = make_results('Animal type', 'Name', 'Date of birth', 'Outcome date', 'Outcome subtype',
                                      'Outcome type', data=results)
    results_with_names[0]['Color'] = get_colors_by_animal_id(uid)
    results_with_names[0]['Breed'] = get_breeds_by_animal_id(uid)
    return render_template('animal_card.html', card=results_with_names[0])


@app.route('/<int:uid>')
def shows_by_id(uid: int):
    if not (results := run_plain_sql(SQL.format(uid))):
        raise NotFoundError
    results_with_names = make_results('Animal type', 'Name', 'Date of birth', 'Outcome date', 'Outcome subtype',
                                      'Outcome type', data=results)
    results_with_names[0]['Color'] = get_colors_by_animal_id(uid)
    results_with_names[0]['Breed'] = get_breeds_by_animal_id(uid)
    return jsonify(results_with_names[0])


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


if __name__ == '__main__':
    app.run()
