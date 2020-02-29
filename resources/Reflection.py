from flask import request
from flask_restful import Resource
from models.Model import db
from models.Reflection import ReflectionModel, ReflectionSchema

reflections_schema = ReflectionSchema(many=True)
reflection_schema = ReflectionSchema()

class ReflectionList(Resource): 
    def get(self, user_id):
        """ Gets reflections for a user
        """
        reflections = ReflectionModel.query.filter_by(user_id=user_id)
        reflections = reflections_schema.dump(reflections)
        return {'status': 'success', 'data': reflections}, 200

class ReflectionResource(Resource):
    def post(self):
        """ Creates a new relfection for a user
        """
        user_id = request.form['user_id']
        reflection = request.form['reflection']
        new_reflection = ReflectionModel(user_id = user_id,
            reflection = reflection) 
        db.session.add(new_reflection)
        db.session.commit()
        return {'status': 'success', 'data': reflection_schema.dump(new_reflection)}, 200
    
    