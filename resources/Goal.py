from flask import request
from flask_restful import Resource
from models.Model import db
from models.Goal import Goal, GoalSchema
from models.Subgoal import Subgoal, SubgoalSchema
from keywords.Extractor import KeywordExtractor
import datetime 

goals_schema = GoalSchema(many=True)
goal_schema = GoalSchema()
subgoals_schema = SubgoalSchema(many=True)

class GoalList(Resource): 
    # NOTE: tested
    def get(self,user_id, complete_status): 
        """
        Input: user_id - id of the user, 
               complete_status - complete or incomplete
        Return: list of complete or incomplete goals 
        """
        goals_list = []
        goals = Goal.query.filter_by(user_id=user_id, status=complete_status)
        # For each high level goal, get the subgoal associated for each 
        subgoal_count = 0 
        subgoals_complete = 0 
        for goal in goals:
            goal_id = goal.id 
            subgoals = Subgoal.query.filter_by(goal_id=goal_id)
            # Iterate through subgoals to get total and number of inc subgoals 
            for subgoal in subgoals:
                subgoal_count += 1 
                if subgoal.status == 'complete':
                    subgoals_complete += 1 
            subgoals = subgoals_schema.dump(subgoals)
            goal = goal_schema.dump(goal)
            goals_list.append({'goal': goal,'subgoals': subgoals, 'completion': {'total_subgoals': subgoal_count, 'completed_subgoals': subgoals_complete}})
        # goals list is a list of dicts 
        return {'status': 'success', 'data': goals_list}, 200

    # NOTE: tested 
    def put(self, user_id, complete_status):
        """Completes or incompletes a main goal and all of it's subgoals 
        """
        goal_id = request.get_json()['goal_id']
        goal = Goal.query.filter_by(id=goal_id).first() 
        # Update goal complete status 
        goal.status = complete_status 
        # update this field only if being completed 
        if complete_status == 'complete':
            goal.completion_time = datetime.datetime.now()
        else: 
            # Reset completion time if incompleting the goal
            goal.completion_time = None
        db.session.add(goal)
        # Get all the subgoals associated with the goal 
        subgoals = Subgoal.query.filter_by(goal_id=goal_id) 
        # Update all subgoals to new status
        for subgoal in subgoals:
            subgoal.status = complete_status 
            db.session.add(subgoal)
        db.session.commit()
        return {'status': 'success'}, 200

# NOTE: tested       
class GoalResource(Resource):
    def post(self):
        """ Creates a new high level goal for user and subgoals
        """
        # First create the high level goal
        user_id = request.form['user_id']
        goal = request.form['goal']
        category = request.form['category']
        goal_tags = self.generate_keywords_goals(goal=goal, user_id=user_id)
        status = 'incomplete'
        new_goal = Goal(user_id = user_id,
            goal = goal, 
            tags = goal_tags, 
            status = status, 
            category = category)
        db.session.add(new_goal)
        db.session.commit()
        new_goal_id = goal_schema.dump(new_goal)['id']
        # Next, create the subgoals 
        n_subgoals = request.form['number_of_subgoals']
        for i in range(int(n_subgoals)):
            field = f'subgoal{i+1}'
            subgoal = request.form[field]
            if subgoal == "":
                continue 
            tags = self.generate_keywords_subgoals(subgoal=subgoal, goal_id=new_goal_id)
            db.session.add(Subgoal(goal_id = new_goal_id,
                subgoal = subgoal,
                tags = tags, 
                status = status))
        db.session.commit()
        return {'status': 'success'}, 200

    # NOTE: tested
    def delete(self):
        """ Deletes a main goal and all of it's subgoals 
        """  
        goal_id = request.get_json()['goal_id']
        goal = Goal.query.filter_by(id=goal_id).first() 
        # Get all the subgoals associated with the goal 
        subgoals = Subgoal.query.filter_by(goal_id=goal_id) 
        # delete all the subgoals
        for subgoal in subgoals:
            db.session.delete(subgoal)
            db.session.commit()
        # delete the main goal
        db.session.delete(goal)
        db.session.commit()
        return {'status': 'success'}, 200

    def put(self): 
        """Edit/add/delete subgoals
        """
        # Get main goal info 
        main_goal = request.get_json()['main_goal']
        goal_id = main_goal['goal_id']
        category = main_goal['category']
        goal = main_goal['goal']

        # Get the goal to update 
        goal_update = Goal.query.filter_by(id=goal_id).first()
        # Update the main goal
        goal_update.goal = goal
        goal_update.category = category 
        db.session.add(goal_update)

        # Get the subgoals from the request 
        subgoals = request.get_json()['subgoals'] # dict {subgoal_id, subgoal, status}
        # Determine subgoals to delete
        subgoals_existing = Subgoal.query.filter_by(goal_id=goal_id)
        print("@@@@@@@@@@@@@@DETERMINING SUBGOALS TO DELETE@@@@@@@@@@@@@@@@@@")
        for se in subgoals_existing: 
            print(se.id)
            delete_flag = True 
            for subgoal in subgoals: 
                if subgoal['subgoal_id']: 
                    # Check for id match 
                    if se.id == subgoal['subgoal_id']:
                        # since the subgoal exists in both the edit and in db
                        # do not delete it 
                        print("@@@@@@@@@@@DO NOT DELETE@@@@@@@@@@@@@@@@@")
                        delete_flag = False
            # Existing subgoal was not in the request, delete it                          
            if delete_flag: 
                print("@@@@@@@@@@@DELETE@@@@@@@@@@@@@@@@@")
                db.session.delete(se)   

        # Create new subgoals or edit existing 
        for subgoal in subgoals:
            # Parse request info
            subgoal_id = subgoal['subgoal_id']
            subgoal_title = subgoal['subgoal']
            status = subgoal['status']
            print("@@@@@@@@@@@SUBGOAL ID:@@@@@@@@@@@@@@@@@")
            print(subgoal_id)
            # CASE 1: create a new subgoal 
            if not subgoal_id:
                print("@@@@@@@@@@@CREATING NEW SUBGOAL@@@@@@@@@@@@@@@@@")
                tags = self.generate_keywords_subgoals(subgoal_title, goal_id)
                new_subgoal = Subgoal(subgoal_title, goal_id, tags, status)
                db.session.add(new_subgoal)
            # CASE 2: edit existing subgoal 
            subgoal_to_edit = Subgoal.query.filter_by(id=subgoal_id).first()
            if subgoal_to_edit: 
                print("@@@@@@@@@@@EDITING SUBGOAL@@@@@@@@@@@@@@@@@")
                subgoal_to_edit.subgoal = subgoal_title 
                subgoal_to_edit.status = status 

        db.session.commit()
        return {'status': 'success'}, 200 
        
    # NOTE: this could be refactored!!! 
    def generate_keywords_subgoals(self, subgoal, goal_id):
        subgoals = []
        # Gets list of subgoal objects
        subgoal_objs = Subgoal.query.filter_by(goal_id=goal_id)
        # Add each subgoal in db to list
        for subgoal_obj in subgoal_objs:
            subgoals.append(subgoal_obj.subgoal)
        # Append the desired goal to list to add it to corpus
        print(subgoal)
        subgoals.append(subgoal)
        # Extract the keywords from the goal
        extractor = KeywordExtractor(3)
        corpus = extractor.pre_process(subgoals)
        (tfidf_vec, feature_names) = extractor.create_tfidf_vectors(corpus, subgoal)
        # Dataframe
        keywords = extractor.extract_topn_from_vector(tfidf_vec, feature_names)
        # Keywords are indices to pd df, convert it to a list!
        keywords_list = keywords.index.tolist()
        keywords = ', '.join(keywords_list)
        return keywords

    # NOTE: this could be refactored!!! 
    def generate_keywords_goals(self, goal, user_id):
        goals = []
        # Gets list of subgoal objects
        goal_objs = Goal.query.filter_by(user_id=user_id)
        # Add each subgoal in db to list
        for goal_obj in goal_objs:
            goals.append(goal_obj.goal)
        # Append the desired goal to list to add it to corpus
        print(goal)
        goals.append(goal)
        # Extract the keywords from the goal
        extractor = KeywordExtractor(3)
        corpus = extractor.pre_process(goals)
        (tfidf_vec, feature_names) = extractor.create_tfidf_vectors(corpus, goal)
        # Dataframe
        keywords = extractor.extract_topn_from_vector(tfidf_vec, feature_names)
        # Keywords are indices to pd df, convert it to a list!
        keywords_list = keywords.index.tolist()
        keywords = ', '.join(keywords_list)
        return keywords