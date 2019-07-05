from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from app.config import Config


app = Flask(__name__)
app.config.from_object(Config)
app.jinja_env.add_extension('jinja2.ext.do')
app.jinja_env.add_extension('jinja2.ext.loopcontrols')
db = SQLAlchemy(app)
login = LoginManager(app)
migrate = Migrate(app, db)
bootstrap = Bootstrap(app)


# login.init_app(app)
# db.init_app(app)

# def create_app(config_class=Config):
    # db.drop_all()
    # db.create_all()

    # return app


from app import routes, models

