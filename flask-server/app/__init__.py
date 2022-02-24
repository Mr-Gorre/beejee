from flask import Flask
from flask_login import LoginManager
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy


# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    Bootstrap5(app)

    app.config.from_pyfile("config.py")
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .views.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .views.todos import todos as todos_blueprint
    app.register_blueprint(todos_blueprint)

    return app

app=create_app()