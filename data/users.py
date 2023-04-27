import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import orm
from flask_login import UserMixin


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    email = sqlalchemy.Column(sqlalchemy.String, index=True, unique=True, nullable=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    surname = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    nickname = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    birthday = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    modified_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    description = sqlalchemy.Column(sqlalchemy.String, default="")
    avatar = sqlalchemy.Column(sqlalchemy.String, default="/static/img/avatars/default_avatar.png")
    subscribers = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    subscriptions = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    posts = sqlalchemy.Column(sqlalchemy.Integer, default=0)

    post = orm.relationship("Post", back_populates='user')

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)
