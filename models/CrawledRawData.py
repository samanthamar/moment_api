from models.Model import db, ma
from datetime import datetime

class CrawledRawData(db.Model):
    __tablename__ = 'crawled_raw_data'
    id = db.Column(db.Integer, primary_key=True)
    # This is a longtext
    text = db.Column(db.Text(4294000000))

    def __init__(self, text):
        self.text = text

    def __repr__(self):
        return '<Crawled Data %r>' % (self.text)

class CrawledRawDataSchema(ma.Schema):
    class Meta:
        fields = ("id", "text")