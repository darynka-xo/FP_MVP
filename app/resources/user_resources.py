from flask_restful import Resource, reqparse
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User
from app import db

class UserRegister(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', required=True)
        parser.add_argument('password', required=True)
        parser.add_argument('role', required=True)
        data = parser.parse_args()

        hashed_password = generate_password_hash(data['password'], method='sha256')
        new_user = User(username=data['username'], password=hashed_password, role=data['role'])
        db.session.add(new_user)
        db.session.commit()
        return {'message': 'User registered successfully'}, 201

class UserLogin(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', required=True)
        parser.add_argument('password', required=True)
        data = parser.parse_args()

        user = User.query.filter_by(username=data['username']).first()
        if user and check_password_hash(user.password, data['password']):
            return {'message': f'Welcome, {user.username}!'}, 200
        return {'message': 'Invalid credentials'}, 401