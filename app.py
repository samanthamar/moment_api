from flask import Blueprint
from flask_restful import Api
from resources.User import UserResource
from resources.ResResource import ResResource
from resources.Goal import GoalResource, GoalList
from resources.Subgoal import SubgoalResource

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

# Routes
api.add_resource(UserResource, '/users')
api.add_resource(ResResource, '/resources')
api.add_resource(GoalResource, '/goals')
api.add_resource(GoalList, '/goals/<user_id>')
api.add_resource(SubgoalResource, '/subgoals')