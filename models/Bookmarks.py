from models.Model import db, ma
from datetime import datetime

class BookmarksModel(db.Model):
    __tablename__ = 'bookmarks'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    resource_id = db.Column(db.Integer, db.ForeignKey('resources2.id'))
    timestamp = db.Column(db.TIMESTAMP, nullable=False)

    def __init__(self, user_id, resource_id):
        self.user_id = user_id
        self.resource_id = resource_id
        self.timestamp = datetime.utcnow()

    def __repr__(self):
        return '<Bookmark %r>' % (self.resource_id)

class BookmarksSchema(ma.Schema):
    class Meta:
        fields = ("id", "user_id", "resource_id", "timestamp")