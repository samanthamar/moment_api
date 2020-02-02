from flask import request
from flask_restful import Resource
from models.Model import db
from models.Goal import Goal, GoalSchema
from models.Subgoal import Subgoal, SubgoalSchema

goals_schema = GoalSchema(many=True)
goal_schema = GoalSchema()
subgoals_schema = SubgoalSchema(many=True)

class GoalList(Resource): 
    def get(self, user_id):
        """ Gets all goals and related subgoals 
        associated with a user_id 
        """
        goals_list = []  
        # Get all high level goals for the user 
        goals = Goal.query.filter_by(user_id=user_id)
        # For each high level goal, get the subgoals for each 
        for goal in goals:
            goal_id = goal.id 
            subgoals = Subgoal.query.filter_by(goal_id=goal_id)
            subgoals = subgoals_schema.dump(subgoals)
            goal = goal_schema.dump(goal)
            goals_list.append({'goal': goal,'subgoals': subgoals})
        # goals list is a list of dicts 
        return {'status': 'success', 'data': goals_list}, 200

class GoalResource(Resource):
    def post(self):
        """ Creates a new high level goal for user 
        """
        user_id = request.form['user_id']
        goal = request.form['goal']
        # NOTE: WIP!!!
        tags = self.generateTags(goal) 
        category = request.form['category']
        new_goal = Goal(user_id = user_id,
            goal = goal, 
            tags = tags, 
            status = status, 
            category = category)
        db.session.add(new_goal)
        db.session.commit()
        return {'status': 'success', 'data': goal_schema.dump(new_goal)}, 200
    
    # WIP 
    def generateTags(self, goal):
        return 'tag1, tag2, tag3'