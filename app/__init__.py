from flask import Flask,render_template
from config import config_options

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_options[config_name]) #load configuration variables

    

    #register blueprint
    from app.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app



