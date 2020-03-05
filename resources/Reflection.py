from datetime import datetime
from flask import request
from flask_restful import Resource
from models.Model import db
from models.Reflection import ReflectionModel, ReflectionSchema

reflections_schema = ReflectionSchema(many=True)
reflection_schema = ReflectionSchema()

class ReflectionList(Resource): 
    # NOTE: tested
    def get(self, user_id):
        """ Gets reflections for a user
        """
        reflections = ReflectionModel.query.filter_by(user_id=user_id)
        reflections = reflections_schema.dump(reflections)
        return {'status': 'success', 'data': reflections}, 200

class ReflectionResource(Resource):
    # NOTE: tested
    def post(self):
        """ Creates a new relfection for a user
        """
        user_id = request.get_json()['user_id']
        title = request.get_json()['title']
        reflection = request.get_json()['reflection']
        new_reflection = ReflectionModel(user_id = user_id,
            title=title,
            reflection = reflection) 
        db.session.add(new_reflection)
        db.session.commit()
        return {'status': 'success', 'data': reflection_schema.dump(new_reflection)}, 200

    # NOTE: tested
    def put(self):
        """ Edit an existing reflection (ie. updates the json stored in the DB)
        """
        reflection_id = request.get_json()['reflection_id']
        title = request.get_json()['title']
        relfection_update = request.get_json()['reflection']
        reflection = ReflectionModel.query.filter_by(id=reflection_id).first()
        # Update the reflection
        reflection.reflection = relfection_update
        reflection.title = title
        reflection.last_modified = datetime.now()
        db.session.add(reflection)
        db.session.commit()
        return {'status': 'success'}, 200

    # NOTE: tested 
    def delete(self): 
        """ Delete an existing reflection using reflection id 
        """
        reflection_id = request.get_json()['reflection_id']
        reflection = ReflectionModel.query.filter_by(id=reflection_id).first()
        db.session.delete(reflection)
        db.session.commit()
        return {'status': 'success'}, 200
    