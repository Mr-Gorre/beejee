from app import create_app
from create_db import create_db
from create_admin import create_admin


if __name__ == "__main__":
    from waitress import serve
    app = create_app()
    create_db(app)
    create_admin(app)
    serve(app, host="0.0.0.0", port=5000)