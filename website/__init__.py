from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import redis
from flask_session import Session
# from os import getenv
# from dotenv import load_dotenv
# from flask_pymongo import PyMongo

# load_dotenv()


# MYSQL_DB_NAME = getenv("MYSQL_DB_NAME")
# MYSQL_USERNAME = getenv("MYSQL_USERNAME")
# MYSQL_PASSWORD = getenv("MYSQL_PASSWORD")
# MYSQL_PORT = getenv("MYSQL_PORT")
# MYSQL_HOST = getenv("MYSQL_HOST")
# MONGO_DB_NAME = getenv("MONGO_DB_NAME")
# MONGO_HOST = getenv("MONGO_HOST")
# MONGO_PORT = getenv("MONGO_PORT")


db = SQLAlchemy()
# mongo = PyMongo()

# table_names = []

def create_app():

    app = Flask(__name__)   
    app.debug = True
    app.config['SECRET_KEY'] = 'secrecy101'

    app.config['SQLALCHEMY_DATABASE_URI'] = \
            f'mysql+pymysql://root:password@localhost:3306/intimateQUsers'
    
#     app.config['MONGO_URI'] = f'mongodb://localhost:27017/intimateQ'

    #configuring redis
    app.config['SESSION_TYPE'] = 'redis'
    app.config['SESSION_PERMANENT'] = False
    app.config['SESSION_USE_SIGNER'] = True
    app.config['SESSION_REDIS'] = redis.Redis(host='localhost', port=6379)    

    db.init_app(app)
    Session(app)
#     mongo.init_app(app)


    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')


    from .models import User, Doctor

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        user = User.query.get(int(id))
        if user is None:
            user = Doctor.query.get(int(id))
        return user
    
#     @login_manager.user_loader
#     def load_doctor(doctorId):
#         return Doctor.query.get(int(doctorId))

    with app.app_context():
        db.create_all()

    #     db.Model.metadata.reflect(db.engine)

    # # Print all loaded tables
    #     for table_name in db.Model.metadata.tables:
    #         table_names.append(table_name)
            # print(f"Loaded table: {table_name}")


    return app