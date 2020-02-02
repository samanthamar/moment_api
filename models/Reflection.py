from models.Model import db, ma
from datetime import datetime

class ReflectionModel(db.Model):
    __tablename__ = 'reflections'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    goal_id = db.Column(db.Integer, db.ForeignKey('goals.id'))
    reflection = db.Column(db.String(128))
    timestamp = db.Column(db.TIMESTAMP, default=datetime.now(), nullable=False)

    def __init__(self, user_id, goal_id, reflection):
        self.user_id = user_id
        self.goal_id = goal_id
        self.reflection = reflection

    def __repr__(self):
        return '<Reflection %r>' % (self.reflection)

class ReflectionSchema(ma.Schema):
    class Meta:
        fields = ("id", "user_id", "goal_id", "timestamp", "reflection")
