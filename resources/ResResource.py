from flask import request
from flask_restful import Resource
from models.Model import db
from models.ResourceModel import ResourceModel, ResourceSchema

resources_schema = ResourceSchema(many=True)
resource_schema = ResourceSchema()

class ResResource(Resource):
    def get(self):
        resources = ResourceModel.query.all()
        resources = resources_schema.dump(resources)
        return {'status': 'success', 'data': resources}, 200

    def post(self):
        link = request.form['link']
        tags = request.form['tags']
        useful = request.form['useful']
        new_res = ResourceModel(link=link, tags=tags, useful=useful)
        db.session.add(new_res)
        db.session.commit()
        return resource_schema.dump(new_res)
