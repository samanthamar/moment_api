from flask import request
from flask_restful import Resource
from models.Model import db
from models.ResourceModel import ResourceModel, ResourceSchema

resources_schema = ResourceSchema(many=True)
resource_schema = ResourceSchema()

class ResResource(Resource):
    def get(self):
        """ Gets all resources in database
        """
        resources = ResourceModel.query.all()
        resources = resources_schema.dump(resources)
        return {'status': 'success', 'data': resources}, 200
