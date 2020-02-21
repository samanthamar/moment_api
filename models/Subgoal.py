from models.Model import db, ma
from datetime import datetime

class Subgoal(db.Model):
    __tablename__ = 'subgoals'
    id = db.Column(db.Integer, primary_key=True)
    subgoal = db.Column(db.String(64)) 
    goal_id = db.Column(db.Integer, db.ForeignKey('goals.id'))
    tags = db.Column(db.String(64)) 
    timestamp = db.Column(db.TIMESTAMP, default=datetime.now(), nullable=False)
    status = db.Column(db.String(20), default='incomplete')
    category = db.Column(db.String(20))

    def __init__(self, subgoal, goal_id, tags, category, status):
        self.subgoal = subgoal 
        self.tags = tags
        self.goal_id = goal_id
        self.category = category
        self.status = status

    def __repr__(self):
        return '<Subgoal %r>' % (self.subgoal)

class SubgoalSchema(ma.Schema):
    class Meta:
        fields = ("id", "subgoal", 
                    "goal_id", "tags", 
                    "timestamp", "status", "category")
