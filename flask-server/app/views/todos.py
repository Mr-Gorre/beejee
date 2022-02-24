from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import login_required
from sqlalchemy import asc, desc
from app import db
from app.forms import TodoForm
from app.models import Todo
from app.config import PAGE_SIZE

todos = Blueprint('todos', __name__)


@todos.route('/')
def index():
    return redirect(url_for('todos.list'))


@todos.route('/todos/', methods=['GET', 'POST'])
def list():
    success = False

    form = TodoForm()
    if form.validate_on_submit():
        username = request.form['username']
        email = request.form['email']
        text = request.form['text']
        todo = Todo(username=username, email=email, text=text)
        db.session.add(todo)
        db.session.commit()
        form.username.data = ''
        form.email.data = ''
        form.text.data = ''
        success = True

    order = request.args.get('order_by')
    order_desc = request.args.get('desc', type=lambda x: x.lower() == "true")
    page = request.args.get('page', type=int, default=1)

    orders = {
        'id': Todo.id,
        'username': Todo.username,
        'email': Todo.email,
        'text': Todo.text,
        'status': Todo.status
    }
    cols = {
        'id': "#",
        'username': "Username",
        'email': "Email",
        'text': "Text",
        'status': "Status"
    }
    ordered_column = orders[order] if order in orders else orders['id']
    direction = desc if order_desc else asc

    todos = Todo.query.order_by(
        direction(ordered_column)).paginate(page, PAGE_SIZE, False)
    return render_template('todos/list.html', form=form, todos=todos, cols=cols, order_by=order, desc=order_desc, success=success)


@todos.route('/todos/<id>/edit', methods=['POST', 'GET'])
@login_required
def edit(id):
    todo = Todo.query.get_or_404(id)
    form = TodoForm(obj=todo)
    if form.validate_on_submit():
        todo.username = request.form['username']
        todo.email = request.form['email']
        todo.text = request.form['text']

        db.session.add(todo)
        db.session.commit()
        return render_template('todos/edit.html', form=form, todo=todo, success=True)
    return render_template('todos/edit.html', form=form, todo=todo)


@todos.route('/todos/<id>/remove')
@login_required
def delete(id):
    todo = Todo.query.get_or_404(id)
    db.session.delete(todo)
    db.session.commit()
    back_url = back_url(default='todos.list')
    return render_template('todos/delete.html', title=f"Remove {id}", todo=todo, back_url=back_url)

@todos.route('/todos/<id>/toggle')
@login_required
def toggle(id):
    todo = Todo.query.get_or_404(id)
    todo.status = not todo.status
    db.session.add(todo)
    db.session.commit()
    return redirect(back_url('todos.list'))



def back_url(default='index'):
    return request.referrer or url_for(default)
