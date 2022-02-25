from app.models import User
from app import db, create_app
from werkzeug.security import generate_password_hash


def create_admin(app=None):
    app = app or create_app()
    app.app_context().push()
    admin = User.query.filter_by(username='Admin').first()
    if admin is None:
        admin = User(username="Admin", password=generate_password_hash("123"))
        db.session.add(admin)
        db.session.commit()


if __name__ == "__main__":
    create_admin()
