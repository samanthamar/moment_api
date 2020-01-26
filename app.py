from flask import Blueprint
from flask_restful import Api
from resources.User import UserResource
from resources.ResResource import ResResource

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

# Routes
api.add_resource(UserResource, '/users')
api.add_resource(ResResource, '/resources')