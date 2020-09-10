import random
from datetime import datetime

from flask import (
    Flask,
    request,
    render_template,
    send_file,
    redirect,
    url_for
    )

from werkzeug.utils import secure_filename

from question_game.qa_game import QAGame
from app_question_game.processing.file_processing import allowed_file
from app_question_game.processing.file_reader import read_file, read_cat_file

from app_question_game.db import db
from app_question_game.models.bitext import BitextModel

from app_question_game.config import DevelopmentConfig, ProductionConfig
from app_question_game.config import get_logger

_logger = get_logger(logger_name=__name__)

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

# prepare app to work with db
db.init_app(app)

# an object to keep the state of user interactions
current_game = QAGame()


@app.before_first_request
def create_tables():
    db.drop_all()
    db.create_all()


@app.after_request
def add_header(response):
    response.cache_control.max_age = 0
    return response


@app.route('/')
def root():
    return redirect(url_for('main'))


@app.route('/upload', methods=['GET'])
def upload_view():
    """Provide a file upload page function."""
    return render_template('upload.html')


@app.route('/upload', methods=['POST'])
def upload():
    """Provide file upload functionality."""
    if request.method == 'POST':
        # check if the post request has the expected parts
        if 'bitext' not in request.files:
            return redirect(request.url)
        bitext_file = request.files['bitext']
        # if user does not select any file
        if bitext_file.filename == '':
            return redirect(request.url)
        if bitext_file and allowed_file(bitext_file.filename):
            try:
                filename = secure_filename(bitext_file.filename)
                _logger.info('Uploading file: ' + filename)
                res = read_file(bitext_file)
                _logger.info('Expected length is 2 or 3: ' + str(len(res[0])))
            except UnicodeDecodeError as err:
                return render_template(
                    'invalid_file.html',
                    err=err
                    )
            except ValueError as err:
                return render_template(
                    'invalid_file.html',
                    err=err
                    )
            else:
                if len(res[0]) == 2:
                    _logger.info('Expected length is 2:' + str(len(res[0])))
                    current_game.add_bitext_from_list(res, filename)
                elif len(res[0]) == 3:
                    _logger.info('Expected length is 3:' + str(len(res[0])))
                    # create database tables
                    db.drop_all()
                    db.create_all()
                    BitextModel.save_all_to_db(res)
                    current_game.set_topics(reset=True)
                else:
                    raise ValueError('Unexpected length')

    return render_template('upload.html',
                           stats=str(len(res)),
                           filename=filename
                           )


@app.route('/main', methods=['GET', 'POST'])
def main():
    data = []
    available_topics = BitextModel.get_categories_counts()
    _logger.info(str(available_topics))
    if request.method == 'GET':
        if request.args.get('submit_button') == "question":
            _logger.info('get_question GET request')
            try:
                topic = random.choice(current_game.get_topics())
            except IndexError:
                topic = []
            _logger.info('topic= ' + str(topic))
            if topic == current_game.filename:
                data = current_game.get_question()
            elif topic in current_game.get_topics():
                _logger.info('topic in selected_topic')
                random_qa_pair = BitextModel.random_line(topic)
                _logger.info('random_qa_pair= ' + str(random_qa_pair))
                data = current_game.get_question(online_qa=random_qa_pair)
            else:
                data = []

        elif request.args.get('submit_button') == 'answer':
            _logger.info('show_answer GET request')
            data = current_game.show_answer()

        elif request.args.get('submit_button') == 'reporting':
            _logger.info('get_report GET request')
            report_file_obj = current_game.get_bytes_io_report()

            return send_file(
                report_file_obj,
                as_attachment=True,
                attachment_filename='report-'+str(datetime.now())+'.txt',
                mimetype='text/csv',
                cache_timeout=0
            )
        elif request.args.get('submit_button') == 'submit_topics':
            for topic in request.args.getlist('topics'):
                _logger.info('topic == ' + str(topic))
                if topic == 'all':
                    current_game.set_topics(
                        [t[0] for t in available_topics],
                        reset=True)
                else:
                    topic = topic.split(',')[0][2:-1]
                    if topic not in current_game.get_topics():
                        current_game.set_topics(topic)

        elif request.args.get('submit_button') == 'clear':
            current_game.set_topics(reset=True)

    elif request.method == 'POST':
        _logger.info('POST request')
        guess = request.form['guess']
        _logger.info('guess from form: ' + str(guess))
        data = current_game.evaluate_guess(guess)

    _logger.info('data from view: ' + str(data))
    return render_template('main.html',
                           data=data,
                           selected_topics=current_game.get_topics(),
                           available_topics=available_topics
                           )


if __name__ == '__main__':
    app.run()
