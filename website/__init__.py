from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import redis
from flask_session import Session
from os import getenv
from dotenv import load_dotenv
# from flask_pymongo import PyMongo

load_dotenv()


MYSQL_DB_NAME = getenv("MYSQL_DB_NAME").strip()
MYSQL_USERNAME = getenv("MYSQL_USERNAME").strip()
MYSQL_PASSWORD = getenv("MYSQL_PASSWORD").strip()
MYSQL_PORT = int(getenv("MYSQL_PORT").strip())
MYSQL_HOST = getenv("MYSQL_HOST").strip()

SESSION_TYPE = getenv("SESSION_TYPE").strip()
SESSION_REDIS_HOST = getenv("SESSION_REDIS_HOST").strip()
SESSION_REDIS_PORT = int(getenv("SESSION_REDIS_PORT").strip())
REDIS_USERNAME = getenv("REDIS_USERNAME").strip()
REDIS_PASSWORD = getenv("REDIS_PASSWORD").strip()


db = SQLAlchemy()
# mongo = PyMongo()

# table_names = []

def create_app():

    app = Flask(__name__, static_folder='static')   
    app.debug = True
    app.config['SECRET_KEY'] = 'secrecy101'

    app.config['SQLALCHEMY_DATABASE_URI'] = \
            f'mysql+pymysql://{MYSQL_USERNAME}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB_NAME}'
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_pre_ping': True,
        'pool_recycle': 280
    }
#     app.config['MONGO_URI'] = f'mongodb://localhost:27017/intimateQ'

    #configuring redis
    app.config['SESSION_TYPE'] = SESSION_TYPE
#     app.config['SESSION_PERMANENT'] = False
#     app.config['SESSION_USE_SIGNER'] = True
    redis_url = f"redis://{REDIS_USERNAME}:{SESSION_REDIS_PORT}"
#     app.config['SESSION_REDIS'] = redis.StrictRedis(
#                         host=SESSION_REDIS_HOST,
#                         port=SESSION_REDIS_PORT,
#                         username=REDIS_USERNAME,
#                         password=REDIS_PASSWORD,
#                         ssl=True)    
    app.config['SESSION_REDIS'] = redis.from_url(redis_url)

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