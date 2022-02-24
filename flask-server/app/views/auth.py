from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import login_user, logout_user
from app import db
from app.forms import LoginForm
from app.models import User
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    login_failed = False
    form = LoginForm()
    if form.validate_on_submit():
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('todos.index'))
        else:
            login_failed = True
    return render_template("auth/login.html", title="Login Form", form=form, login_failed=login_failed)


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('todos.index'))
