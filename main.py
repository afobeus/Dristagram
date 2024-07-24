from flask import Flask, redirect, render_template, request, abort, jsonify, make_response
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, mixins
from flask_restful import Api
from sqlalchemy import desc

from datetime import datetime
import os

from data import db_session
from data.comments import Comment
from data.users import User
from data.posts import Post
from forms.post import PostAddForm
from forms.user import RegisterForm, LoginForm
import data.users_resource as users_resource

from functions import format_social_media_post_time, resize_image


app = Flask(__name__)

api = Api(app)

api.add_resource(users_resource.UsersListResource, '/api/users')
api.add_resource(users_resource.UsersResource, '/api/users/<int:user_id>')

login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    db_session.global_init("db/users.db")
    app.run(port=5000, host='127.0.0.1')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if not isinstance(current_user, mixins.AnonymousUserMixin):
        return redirect(f"/feed")

    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template("register.html", title="Регистрация",
                                   form=form, message="Пароли не совпадают")
        user = User()
        user.email = form.email.data
        user.name = form.name.data
        user.surname = form.surname.data
        user.nickname = form.nickname.data
        user.birthday = form.birthday.data
        user.hashed_password = form.password.data
        user.set_password(form.password.data)
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title="Регистрация",
                                   form=form, message="Такой пользователь уже есть")
        if not form.agreement.data:
            return render_template("register.html", title="Регистрация",
                                   form=form, message="Соласитесь с политикой")
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')  # Todo: add a message "User is registered successfully"
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if not isinstance(current_user, mixins.AnonymousUserMixin):
        return redirect(f"/feed")

    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.nickname == form.login.data).first()  # Todo: form.login.data?
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect(f"/user/{user.nickname}")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route("/view_comments/<int:post_id>")
def view_comments(post_id):
    db_sess = db_session.create_session()
    post = db_sess.query(Post).filter(Post.id == post_id).first()
    comments = post.comments
    return render_template("comments.html", title="Комментарии", comments=comments)


@app.route("/send_comment/<int:post_id>", methods=["POST"])
def send_comment(post_id):
    if request.form["comment_text"]:
        db_sess = db_session.create_session()
        comment = Comment()
        comment.comment_text = request.form["comment_text"]
        comment.post_id = post_id
        comment.user_id = current_user.id

        post = db_sess.query(Post).filter(Post.id == post_id).first()
        post.comments.append(comment)
        post.comments_number += 1
        db_sess.commit()

    return redirect("/feed")


@app.route("/", methods=["GET", "POST"])
@app.route("/feed")
def feed():
    if isinstance(current_user, mixins.AnonymousUserMixin):
        return redirect("/login")
    db_sess = db_session.create_session()
    posts = db_sess.query(Post).order_by(desc(Post.modified_date)).all()
    time_now = datetime.now()
    if len(posts) > 10:
        posts = posts[:10]
    prescriptions = [format_social_media_post_time(post.modified_date) for post in posts]
    return render_template("feed.html", title="Лента", posts=posts, time_now=time_now,
                           prescriptions=prescriptions)


@app.route("/addpost", methods=["GET", "POST"])
def add_post():
    if isinstance(current_user, mixins.AnonymousUserMixin):
        return redirect("/login")
    form = PostAddForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        post = Post()
        post.post_text = form.post_text.data
        file = form.post_picture.data
        filename, file_extension = os.path.splitext(file.filename)
        file_path = f"static/img/posts/post_img_{current_user.id}_{current_user.posts + 1}{file_extension}"
        file.save(file_path)
        # resize_image(file_path)
        post.post_picture = file_path
        user = db_sess.query(User).filter(User.id == current_user.id).first()
        current_user.post.append(post)
        db_sess.merge(current_user)
        user.posts += 1
        db_sess.commit()

        return redirect("/feed")
    return render_template("add_post.html", title="Добавление поста", form=form)


@app.route("/like_post/<int:post_id>/<redirect_link>")
def like_post(post_id, redirect_link):
    if isinstance(current_user, mixins.AnonymousUserMixin):
        return redirect("/login")
    db_sess = db_session.create_session()
    post = db_sess.query(Post).filter(Post.id == post_id).first()
    post.likes += 1
    db_sess.commit()
    if redirect_link == "post_page":
        return redirect(f"/post/{post.id}")
    else:
        return redirect("/feed")


@app.route("/delete_post/<int:post_id>")
def delete_post(post_id):
    if isinstance(current_user, mixins.AnonymousUserMixin):
        return redirect("/login")
    db_sess = db_session.create_session()
    post = db_sess.query(Post).filter(Post.id == post_id).first()
    db_sess.delete(post)
    db_sess.commit()
    return redirect("/feed")


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    if isinstance(current_user, mixins.AnonymousUserMixin):
        return redirect("/login")
    logout_user()
    return redirect("/")


@app.route('/user/<nickname>')
def user_profile(nickname):
    if isinstance(current_user, mixins.AnonymousUserMixin):
        return redirect("/login")
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.nickname == nickname).first()
    if not user:
        abort(404)
    values = {
        "title": f"Профиль {nickname}",
        "nickname": nickname,
        "user": user
    }
    return render_template("profile.html", **values)


@app.route("/post/<int:post_id>")
def post_page(post_id):
    if isinstance(current_user, mixins.AnonymousUserMixin):
        return redirect("/login")
    db_sess = db_session.create_session()
    post = db_sess.query(Post).filter(Post.id == post_id).first()
    values = {
        "title": f"Пост от {post.user.nickname}",
        "post": post,
        "prescription": format_social_media_post_time(post.modified_date)
    }
    return render_template("post_page.html", **values)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def bad_request(_):
    return make_response(jsonify({'error': 'Bad Request'}), 400)


if __name__ == '__main__':
    main()
