from flask import request
from flask_restful import Resource
from models.Model import db
from models.Subgoal import Subgoal, SubgoalSchema

subgoals_schema = SubgoalSchema(many=True)
subgoal_schema = SubgoalSchema()

# class SubgoalList(Resource): 
#     def get(self, user_id):
#         # Get goals for a particular user 
#         # NOTE: want to return goals and their corresponding subgoals
#         # goals = Goal.query.filter_by(user_id=user_id)
#         # goals = goals_schema.dump(goals)
#         # return {'status': 'success', 'data': goals}, 200
#         pass

class SubgoalResource(Resource):
    def post(self):
        """ Creates a new subgoal related to a high level goal
        """
        user_id = request.form['user_id']
        subgoal = request.form['subgoal']
        goal_id = request.form['goal_id']
        # NOTE: WIP!!!
        tags = self.generateTags(goal) 
        category = request.form['category']
        new_subgoal = Subgoal(user_id = user_id,
            goal_id = goal_id, 
            subgoal = goal, 
            tags = tags, 
            status = status, 
            category = category)
        db.session.add(new_subgoal)
        db.session.commit()
        return {'status': 'success', 'data': subgoal_schema.dump(new_subgoal).dump(new_reflection) }, 200 
    
    # WIP 
    def generateTags(self, goal):
        return 'tag1, tag2, tag3'