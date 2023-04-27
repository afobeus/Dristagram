from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField
from wtforms.validators import DataRequired


class PostAddForm(FlaskForm):
    post_text = StringField("Содержание поста", validators=[DataRequired()])
    post_picture = FileField("Изображение", validators=[DataRequired()])
    submit = SubmitField("Submit")
