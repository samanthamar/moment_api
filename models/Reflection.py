from models.Model import db, ma
from datetime import datetime

class ReflectionModel(db.Model):
    __tablename__ = 'reflections'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(240))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    reflection = db.Column(db.JSON)
    date_created = db.Column(db.TIMESTAMP, default=datetime.now(), nullable=False)
    last_modified = db.Column(db.TIMESTAMP)

    def __init__(self, title, user_id, reflection, last_modified=None):
        self.title = title
        self.user_id = user_id
        self.reflection = reflection
        self.last_modified = last_modified

    def __repr__(self):
        return '<Reflection %r>' % (self.reflection)

class ReflectionSchema(ma.Schema):
    class Meta:
        fields = ("id", "title", "user_id", "reflection", "date_created", "last_modified")
