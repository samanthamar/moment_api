from flask import Blueprint
from flask_restful import Api
from resources.User import UserResource
from resources.ResResource import ResResource
from resources.Goal import GoalResource, GoalList
from resources.Subgoal import SubgoalResource
from resources.Reflection import ReflectionResource, ReflectionList

api_bp = Blueprint('api', __name__)
application = Api(api_bp)

# Routes
application.add_resource(UserResource, '/users')
application.add_resource(ResResource, '/resources') # get resource 
application.add_resource(GoalResource, '/goals') # Create goals
application.add_resource(GoalList, '/goals/<user_id>') # Get all goals and subgoals
application.add_resource(SubgoalResource, '/subgoals') # create subgoals 
application.add_resource(ReflectionResource, '/reflections') # create reflections
application.add_resource(ReflectionList, '/reflections/<user_id>') # get all reflections 
