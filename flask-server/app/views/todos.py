from flask import Blueprint, redirect, render_template, request, url_for
from sqlalchemy import asc, desc
from app import db
from app.forms import TodoForm
from app.models import Todo
from app.config import PAGE_SIZE

todos = Blueprint('todos', __name__)


@todos.route('/')
@todos.route('/todos/')
def list():
    order = request.args.get('order_by')
    order_desc = request.args.get('desc', type= lambda x: x.lower() == "true")
    page = request.args.get('page', type=int, default=1)
    #TODO: hmmm
    orders = {
        'id': Todo.id,
        'username': Todo.username,
        'email': Todo.email,
        'text': Todo.text,
        'status': Todo.status
    }
    ordered_column = orders[order] if order in orders else orders['id']
    direction = desc if order_desc else asc

    form = TodoForm()
    todos = Todo.query.order_by(
        direction(ordered_column)).paginate(page, PAGE_SIZE, False)
    return render_template('todos/list.html', form=form, todos=todos, order_by=order, desc=order_desc)


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
        return redirect(redirect_url('todos.list'))
    return render_template('todos/list.html', form=form)


@todos.route('/todos/<id>')
def detail(id):
    return render_template('todos/detail.html')


@todos.route('/todos/<id>/edit', methods=['POST', 'GET'])
def edit(id):
    return render_template('todos/edit.html')

@todos.route('/todos/<id>/remove')
def delete(id):
    todo = Todo.query.get_or_404(id)
    db.session.delete(todo)
    db.session.commit()
    back_url = redirect_url('todos.list')
    return render_template('todos/delete.html', title=f"Remove {id}", todo=todo, back_url=back_url)


def redirect_url(default='index'):
    return request.referrer or url_for(default)