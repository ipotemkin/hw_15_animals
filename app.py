from flask import Flask, jsonify, render_template
from errors import NotFoundError, BadRequestError, ValidationError
from utils import run_plain_sql, make_results, get_full_record

app = Flask(__name__)


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


# shows an animal's card in the browser
@app.route('/card/<int:uid>')
def shows_card_by_id(uid: int):
    return render_template('animal_card.html', card=get_full_record(uid))


# returns an animal record in JSON by the given uid
@app.route('/<int:uid>')
def shows_by_id(uid: int):
    return jsonify(get_full_record(uid))


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
