from flask import Flask, redirect, render_template
from data import db_session
from data.users import User
from data.posts import Post
from forms.post import PostAddForm
from forms.user import RegisterForm, LoginForm
from flask_login import LoginManager, login_user, login_required, logout_user, current_user


app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    db_session.global_init("db/users.db")
    app.run(port=5000, host='127.0.0.1')


@app.route("/feed")
def feed():
    db_sess = db_session.create_session()
    posts = db_sess.query(Post).all()
    if len(posts) > 10:
        posts = posts[:10]
    return render_template("feed.html", title="Лента", posts=posts)


@app.route("/addpost", methods=["GET", "POST"])
def add_post():
    form = PostAddForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        post = Post()
        post.post_text = form.post_text.data
        post.post_picture = f"static/img/post_img_{current_user.posts + 1}.png"
        user = db_sess.query(User).filter(User.id == current_user.id).first()
        current_user.post.append(post)
        db_sess.merge(current_user)
        user.posts += 1
        db_sess.commit()
        return redirect("/feed")
    return render_template("add_post.html", title="Добавление поста", form=form)


@app.route("/", methods=["GET", "POST"])
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.nickname == form.login.data).first()
        if not user:
            return redirect("/register")
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect(f"/user/{user.nickname}")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template("register.html", title="Регистрация",
                                   form=form, message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title="Регистрация",
                                   form=form, message="Такой пользователь уже есть")
        if not form.agreement.data:
            return render_template("register.html", title="Регистрация",
                                   form=form, message="Соласитесь с политикой")

        user = User(
            email=form.email.data,
            name=form.name.data,
            surname=form.surname.data,
            nickname=form.nickname.data,
            birthday=form.birthday.data,
            hashed_password=form.password.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/user/<nickname>')
def user_profile(nickname):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.nickname == nickname).first()
    values = {
        "title": f"Профиль {nickname}",
        "nickname": nickname,
        "user": user
    }
    return render_template("profile.html", **values)


@app.route('/test')
def test():
    return render_template("authorised_base.html")


if __name__ == '__main__':
    main()
