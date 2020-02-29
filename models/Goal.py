from models.Model import db, ma
from datetime import datetime

class Goal(db.Model):
    __tablename__ = 'goals'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    goal = db.Column(db.String(64)) 
    tags = db.Column(db.String(64)) 
    timestamp = db.Column(db.TIMESTAMP, default=datetime.now(), nullable=False)
    status = db.Column(db.String(20), default='incomplete')
    category = db.Column(db.String(20))
    completion_time = db.Column(db.TIMESTAMP) 

    def __init__(self, user_id, goal, tags, category, status, completion_time=None):
        self.user_id = user_id 
        self.goal = goal
        self.tags = tags
        self.category = category
        self.status = status
        completion_time = completion_time

    def __repr__(self):
        return '<Goal %r>' % (self.goal)

class GoalSchema(ma.Schema):
    class Meta:
        fields = ("id", "user_id", 
                    "goal", "tags", 
                    "timestamp", "status", "category", "completion_time")
