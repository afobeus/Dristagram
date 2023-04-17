from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, EmailField, DateField, BooleanField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired()])
    name = StringField("Name", validators=[DataRequired()])
    surname = StringField("Surname", validators=[DataRequired()])
    nickname = StringField("Nickname", validators=[DataRequired()])
    birthday = DateField("Birthday", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    password_again = PasswordField("Repeat password", validators=[DataRequired()])
    agreement = BooleanField("Согласен с политикой конфидециальности")
    submit = SubmitField("Submit")


class LoginForm(FlaskForm):
    login = StringField("Nickname", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember me")
    submit = SubmitField("Submit")
