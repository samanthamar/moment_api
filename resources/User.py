from flask import request
from flask_restful import Resource
from models.Model import db
from models.User import User, UserSchema

users_schema = UserSchema(many=True)
user_schema = UserSchema()

class UserResource(Resource):
    def get(self):
        """ Get all users
        """
        users = User.query.all()
        users = users_schema.dump(users)
        return {'status': 'success', 'data': users}, 200

    def post(self):
        """ Creates a a new user 
        """
        username = request.form['username']
        password = request.form['password']
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        return {'status': 'success', 'data': user_schema.dump(new_user)}, 200

