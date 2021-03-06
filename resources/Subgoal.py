from flask import request
from flask_restful import Resource
from models.Model import db
from models.Subgoal import Subgoal, SubgoalSchema
from keywords.Extractor import KeywordExtractor

subgoals_schema = SubgoalSchema(many=True)
subgoal_schema = SubgoalSchema()

class SubgoalsResource(Resource): 
    def get(self,goal_id): 
        """ Get subgoals based on goal_id 
        """
        subgoals = Subgoal.query.filter_by(goal_id=goal_id)
        subgoals = subgoals_schema.dump(subgoals)
        return {'status': 'success', 'data': subgoals}, 200

class SubgoalResource(Resource):
    def post(self):
        """ Creates a new subgoal related to a high level goal
        """
        subgoal = request.form['subgoal']
        goal_id = request.form['goal_id']
        status = 'incomplete'
        tags = self.generate_keywords(subgoal, goal_id)
        category = request.form['category']
        new_subgoal = Subgoal(goal_id = goal_id,
            subgoal = subgoal,
            tags = tags, 
            status = status, 
            category = category)
        db.session.add(new_subgoal)
        db.session.commit()
        return {'status': 'success', 'data': subgoal_schema.dump(new_subgoal) }, 200
    
    # NOTE: tested
    def put(self): 
        """ Update completion status for subgoals 
        """
        subgoals = request.get_json()['subgoals']
        for subgoal in subgoals: 
            subgoal_id = subgoal['subgoal_id']
            status = subgoal['status']
            subgoal_to_update = Subgoal.query.filter_by(id=subgoal_id).first()
            subgoal_to_update.status = status 
            db.session.add(subgoal_to_update)
        db.session.commit()
        return {'status': 'success'}, 200

    def generate_keywords(self, subgoal, goal_id):
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