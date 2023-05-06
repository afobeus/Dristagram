from . import db_session
from .users import User
from flask_restful import abort, Resource
from flask import jsonify
from data.users_resource_parser import parser


def abort_if_users_not_found(user_id):
    session = db_session.create_session()
    user = session.query(User).get(User)
    if not user:
        abort(404, message=f"User {user_id} not found")


class UsersResource(Resource):
    def get(self, user_id):
        abort_if_users_not_found(User)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        return jsonify({'users': user.to_dict(
            only=('emil', 'name', 'surname', 'nickname',
                  'birthday', 'hashed_password'))})

    def delete(self, user_id):
        abort_if_users_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        session.delete(user)
        session.commit()
        return jsonify({'success': 'OK'})


class UsersListResource(Resource):
    def get(self):
        session = db_session.create_session()
        users = session.query(User).all()
        return jsonify({'users': [item.to_dict(
            only=('emil', 'name', 'surname', 'nickname',
                  'birthday', 'hashed_password')) for item in users]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        user = User(
            emil=args['emil'],
            name=args['name'],
            surname=args['surname'],
            nickname=args['nickname'],
            birthday=args['birthday'],
            hashed_password=args['hashed_password']
        )
        session.add(user)
        session.commit()
        return jsonify({'success': 'OK'})