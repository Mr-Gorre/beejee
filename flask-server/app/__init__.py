from flask import Flask
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy


# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    Bootstrap5(app)

    app.config.from_pyfile("config.py")
    db.init_app(app)

    from .views.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .views.todos import todos as todos_blueprint
    app.register_blueprint(todos_blueprint)

    return app
