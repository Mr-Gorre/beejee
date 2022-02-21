from flask import Blueprint, render_template
from app import db

todos = Blueprint('todos', __name__)


@todos.route('/')
@todos.route('/todos/')
def index():
    return render_template("todos/list.html")


@todos.route('/todos/[id]')
def profile():
    return render_template("todos/detail.html")
