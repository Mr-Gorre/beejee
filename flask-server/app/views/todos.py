from flask import Blueprint, redirect, render_template, request
from app import db
from app.forms import TodoForm
from app.models import Todo

todos = Blueprint('todos', __name__)


@todos.route('/')
@todos.route('/todos/')
def list():
    form = TodoForm()
    todos = Todo.query.limit(5).all()
    return render_template('todos/list.html', form=form, todos=todos)


@todos.route('/todos/', methods=['POST'])
def create():
    form = TodoForm(request.form)
    if form.validate_on_submit():
        username = request.form['username']
        email = request.form['email']
        text = request.form['text']
        todo = Todo(username=username, email=email, text=text)
        db.session.add(todo)
        db.session.commit()
        return redirect('/todos/')
    return render_template('todos/list.html', form=form)


@todos.route('/todos/[id]')
def detail():
    return render_template('todos/detail.html')


@todos.route('/todos/[id]/edit', methods=['POST', 'GET'])
def edit():
    return render_template('todos/detail.html')
