from models.Model import db, ma
from datetime import datetime

class ResourceModel2(db.Model):
    __tablename__ = 'resources2'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(240))
    # Medium text
    link = db.Column(db.String(64000))
    text = db.Column(db.Text(4294000000))

    def __init__(self, title, link, text):
        self.title = title
        self.link = link
        self.text = text

    def __repr__(self):
        return '<Resource2 %r>' % (self.link)

class ResourceSchema2(ma.Schema):
    class Meta:
        fields = ("id", "title", "link", "text")
