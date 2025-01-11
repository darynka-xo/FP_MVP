from flask_restful import Resource, reqparse
from werkzeug.security import generate_password_hash, check_password_hash
from flask import request
from app.models import User
from app import db


class UserRegister(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', required=True)
        parser.add_argument('email', required=True)
        parser.add_argument('password', required=True)
        parser.add_argument('role', required=True)
        parser.add_argument('isChiefTechRegistering', type=bool)
        data = parser.parse_args()

        if User.query.filter((User.username == data['username']) |
                           (User.email == data['email'])).first():
            return {'message': 'User already exists'}, 400

        hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256', salt_length=16)
        new_user = User(
            username=data['username'],
            email=data['email'],
            password=hashed_password,
            role=data['role'],
            # If Chief Tech is registering, automatically approve the user
            approved=True if data['isChiefTechRegistering'] else False,
            blocked=False
        )

        db.session.add(new_user)
        db.session.commit()
        return {'message': 'User created successfully'}, 201


class UserLogin(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', required=True)
        parser.add_argument('password', required=True)
        data = parser.parse_args()
        user = User.query.filter_by(username=data['username']).first()
        if user and check_password_hash(user.password, data['password']):
            if not user.approved:
                return {'message': 'Your account is pending approval.'}, 403
            if user.blocked:
                return {'message': 'Your account has been blocked.'}, 403
            # Simple response with user data
            return {
                'message': f'Welcome, {user.username}!',
                'role': user.role,
                'username': user.username
            }, 200
        return {'message': 'Invalid credentials'}, 401


class UserLogout(Resource):
    def post(self):
        return {'message': 'Logged out successfully'}, 200


class UserApprovalList(Resource):
    def get(self):
        username = request.headers.get('username')

        if not username:
            return {'message': 'Not authenticated'}, 401

        user = User.query.filter_by(username=username).first()
        if not user or user.role != 'Chief Tech':
            return {'message': 'You are not authorized to access this resource.'}, 403

        unapproved_users = User.query.filter_by(approved=False, blocked=False).all()
        return {'users': [user.to_dict() for user in unapproved_users]}, 200


class UserApproveDeny(Resource):
    def post(self, user_id):
        username = request.headers.get('username')

        if not username:
            return {'message': 'Not authenticated'}, 401

        user = User.query.filter_by(username=username).first()
        if not user or user.role != 'Chief Tech':
            return {'message': 'Not authorized'}, 403

        parser = reqparse.RequestParser()
        parser.add_argument('action', required=True)
        data = parser.parse_args()

        target_user = User.query.get_or_404(user_id)
        if data['action'] == 'approve':
            target_user.approved = True
            target_user.blocked = False
        elif data['action'] == 'deny':
            target_user.approved = False
            target_user.blocked = True
        else:
            return {'message': 'Invalid action'}, 400

        db.session.commit()
        return {'message': f'User {target_user.username} has been {data["action"]}d.'}, 200