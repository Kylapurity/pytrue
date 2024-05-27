from api.v1.app import create_app
from werkzeug.exceptions import HTTPException
from flask import jsonify


app = create_app()

@app.errorhandler(HTTPException)
def handle_exception(e):
    """Formats api errors as json response"""
    return jsonify({
        "code": e.code,
        "message": e.description,
        }), e.code

@app.route("/", strict_slashes=False)
def index():
    """Index route"""
    return app.config["ENVIRONMENT"]

if __name__  == "__main__":
    app.run()
