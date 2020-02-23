from flask import Flask
from flask_cors import CORS

application = Flask(__name__)

if __name__ == "__main__":
    # CORS(application)
    application.config.from_object("config")

    from app import api_bp
    application.register_blueprint(api_bp, url_prefix='/api')

    from models.Model import db
    db.init_app(application)
    application.run()
