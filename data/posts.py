import datetime
import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class Post(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'posts'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    likes = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    post_text = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    post_picture = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    comments_number = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    place = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"), nullable=False)
    modified_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)

    user = orm.relationship('User')
    comments = orm.relationship("Comment", back_populates='post')
