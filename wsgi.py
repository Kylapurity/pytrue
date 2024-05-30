from api.v1.app import create_app
from werkzeug.exceptions import HTTPException
from flask import jsonify, request
from api.v1.helpers import extractJWTToken
from api.v1.exc import OauthError
from models.user import User
from jwt.exceptions import ExpiredSignatureError, DecodeError
from sqlalchemy.exc import NoResultFound
import jwt


app = create_app()

@app.errorhandler(HTTPException)
def handle_exception(e):
    """Formats api errors as json response"""
    return jsonify({
        "code": e.code,
        "message": e.description,
        }), e.code

@app.before_request
def load_jwt_user():
    """ Check that request has valid access token"""
    no_auth = ['/api/v1/token', '/api/v1/signup']
    if request.path not in no_auth:       
        try:
            encoded_token = extractJWTToken(request)
            key = app.config["JWT_SECRET"]
            claims = jwt.decode(encoded_token, key, options={"verify_aud": False}, algorithms=["HS256"])
            # fetch user
            user = User.find_by(id=claims["sub"])
            request.current_user = user
        except ValueError:
            raise OauthError("This endpoint requires a Bearer token")
        except NoResultFound:
            raise OauthError("This endpoint requires a Bearer token")
        except ExpiredSignatureError:
            raise OauthError("Bearer token has expired")
        except DecodeError:
            raise OauthError("Invalid access token format")



if __name__  == "__main__":
    app.run()
