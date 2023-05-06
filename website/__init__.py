import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import sqlite3
from flask_mail import Mail
# from .models.Movies import Movie

basedir = os.path.abspath(os.path.dirname(__file__))

db = SQLAlchemy()
mail = None
DB_NAME = "cinema_ebooking_system.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'ghjvbk bjkdhcf'
    app.config['SQLALCHEMY_DATABASE_URI'] = \
        'sqlite:///' + os.path.join(basedir, f'{DB_NAME}')

    app.config['MAIL_SERVER']='smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = 'cinema.ebooking.llc@gmail.com'
    app.config['MAIL_PASSWORD'] = 'csrijfvijnjalcyb'
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True

    db.init_app(app)
    global mail
    mail = Mail(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    # populate_tables()

    return app
        
# def populate_tables():
#     movies_list = []
#     movies_list.append(Movie(title='', category='', cast='', director='', producer='', synopsis='', rating='', picture=''))
#     movies_list.append(Movie(title='', category='', cast='', director='', producer='', synopsis='', rating='', picture=''))
#     movies_list.append(Movie(title='', category='', cast='', director='', producer='', synopsis='', rating='', picture=''))
#     movies_list.append(Movie(title='', category='', cast='', director='', producer='', synopsis='', rating='', picture=''))