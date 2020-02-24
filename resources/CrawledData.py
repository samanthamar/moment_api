from flask import request
from flask_restful import Resource
from models.Model import db
from models.CrawledRawData import CrawledRawData, CrawledRawDataSchema

texts_schema = CrawledRawDataSchema(many=True)
text_schema = CrawledRawDataSchema()

class CrawledRawDataResource(Resource):
    def post(self):
        """ Add a new text file to database  
        """
        text = request.form['text']
        new_text = CrawledRawData(text=text)
        db.session.add(new_text)
        db.session.commit()
        return {'status': 'success', 'data': text_schema.dump(new_text)}, 200