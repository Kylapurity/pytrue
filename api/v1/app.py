from flask import Flask
from flask_cors import CORS
from api.v1.views import api_views
from models import db
import wtforms_json


# Globally accessible libraries
# db = SQLAlchemy()
cors = CORS(resources={r"/*": {"origins": "0.0.0.0"}})


def create_app():
    """App factory for api version 1"""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_pyfile("config.py")

    # Initialize Plugins
    db.init_app(app)
    cors.init_app(app)
    wtforms_json.init() # wtf extension to add json support

    with app.app_context():
        # Include our Routes
        # from . import routes

        # Register Blueprints
        app.register_blueprint(api_views)
        # app.register_blueprint(admin.admin_bp)
        db.create_all()

        return app
