from flask import Blueprint, render_template
from app import db
from app.forms import TodoForm

todos = Blueprint('todos', __name__)


@todos.route('/')
@todos.route('/todos/')
def list():
    form = TodoForm()
    return render_template("todos/list.html", form=form)


@todos.route('/todos/[id]')
def detail():
    return render_template("todos/detail.html")
