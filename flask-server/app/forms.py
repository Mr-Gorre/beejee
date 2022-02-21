from flask_wtf import FlaskForm
from wtforms import StringField, EmailField
from wtforms.validators import DataRequired


class TodoForm(FlaskForm):
    username = StringField("username", validators=[DataRequired()])
    email = EmailField("email", validators=[DataRequired()])
    text = StringField("text", validators=[DataRequired()])
