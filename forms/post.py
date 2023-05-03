from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileRequired, FileAllowed


class PostAddForm(FlaskForm):
    post_text = StringField("Содержание поста", validators=[DataRequired()])
    post_picture = FileField("Изображение", validators=[FileRequired(),
                                                        FileAllowed(['jpg', 'png'], 'Images only!')])
    submit = SubmitField("Submit")
