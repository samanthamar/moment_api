from models.Model import db, ma
from datetime import datetime

class ResourceModel(db.Model):
    __tablename__ = 'resources'
    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String(64))
    tags = db.Column(db.String(64))
    timestamp = db.Column(db.TIMESTAMP, default=datetime.now(), nullable=False)
    useful = db.Column(db.Float)

    def __init__(self, link, tags, useful):
        self.link = link
        self.tags = tags
        self.useful = useful

    def __repr__(self):
        return '<Resource %r>' % (self.link)

class ResourceSchema(ma.Schema):
    class Meta:
        fields = ("id", "link", "tags", "timestamp", "useful")
