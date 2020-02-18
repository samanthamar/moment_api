from flask import Flask

def create_app(config_filename):
    application = Flask(__name__)
    application.config.from_object(config_filename)

    from app import api_bp
    application.register_blueprint(api_bp, url_prefix='/api')

    from models.Model import db
    db.init_app(application)

    return application

if __name__ == "__main__":
    application = create_app("config")
    application.run(debug=True)
