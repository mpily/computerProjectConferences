# third-party imports
import re , datetime, calendar
from flask import Flask, render_template,request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
# local imports
from config import app_config
from sqlalchemy import MetaData

naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}


# db variable initialization

#app = Flask(__name__)
db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))
login_manager = LoginManager()


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    with app.app_context():
        db.app = app
        db.init_app(app)
    Bootstrap(app)

    login_manager.init_app(app)
    login_manager.login_message = "You must be logged in to access this page."
    login_manager.login_view = "auth.login"
    #migrate = Migrate(app, db)

    from myapp import models
    @app.before_first_request
    def create_tables():

        with app.app_context():
            db.create_all()
            #conference1 = models.Conference(name="Vision 2030", description = "An indepth study on progress being made in oder to acheive vision 2030", startdate=datetime.date(2019,5,19),enddate =datetime.date(2019,5,22))
            #db.session.add(conference1)
            #db.session.commit()
            #Units.query.all()
            #workshop1=models.Workshop(name='agriculture', description='the progress we have made in food production', starttime=datetime.datetime(2019,5,19,12,0,0), endtime=datetime.datetime(2019,5,19,14,0,0), conference_id=1)
            #db.session.add(workshop1)
            #db.session.commit()
            #admin = models.Participant(name="admin",email="esoadmin@gmail.com",password="password",is_admin = True)
            #db.session.add(admin)
            #db.session.commit()


    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .home import home as home_blueprint
    app.register_blueprint(home_blueprint)


    return app
