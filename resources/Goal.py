from flask import request
from flask_restful import Resource
from models.Model import db
from models.Goal import Goal, GoalSchema

goals_schema = GoalSchema(many=True)
goal_schema = GoalSchema()

class GoalList(Resource): 
    def get(self, user_id):
        # Get goals for a particular user 
        # NOTE: want to return goals and their corresponding subgoals
        goals = Goal.query.filter_by(user_id=user_id)
        goals = goals_schema.dump(goals)
        return {'status': 'success', 'data': goals}, 200

class GoalResource(Resource):
    def post(self):
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
        return goal_schema.dump(new_goal)
    
    # WIP 
    def generateTags(self, goal):
        return 'tag1, tag2, tag3'