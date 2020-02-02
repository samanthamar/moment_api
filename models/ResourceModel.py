from models.Model import db, ma
from datetime import datetime

class ResourceModel(db.Model):
    __tablename__ = 'resources'
    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String(64))
    tags = db.Column(db.String(64))
    category = db.Column(db.String(20))
    timestamp = db.Column(db.TIMESTAMP, default=datetime.now(), nullable=False)

    def __init__(self, link, tags, category):
        self.link = link
        self.tags = tags
        self.category = category

    def __repr__(self):
        return '<Resource %r>' % (self.link)

class ResourceSchema(ma.Schema):
    class Meta:
        fields = ("id", "link", "tags", "category", "timestamp")
