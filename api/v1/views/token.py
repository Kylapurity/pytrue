#!/usr/bin/python3
""" Token management views """
from models.refresh_token import RefreshToken
from models.user import User
from models.tokens import grantRefreshTokenSwap
from datetime import datetime, timedelta
from api.v1.views import api_views
from api.v1.exc import OauthError
from flask import request, current_app, jsonify
from werkzeug.exceptions import NotImplemented
from sqlalchemy.exc import NoResultFound


@api_views.route('/token', methods=['POST'], strict_slashes=True)
def token():
    """Access token request endpoint"""
    grant_type = request.form.get('grant_type')
    if grant_type == 'password':
        return resourceOwnerPasswordGrant()
    elif grant_type == 'refresh_token':
        return refreshTokenGrant()
    else:
        raise NotImplemented("Invalid grant type")

def resourceOwnerPasswordGrant():
    """Implements resource owner grant type"""
    username = request.form.get('username')
    password = request.form.get('password')

    aud = current_app.config["JWT_AUD"]
    try:
        user = User.find_by(email=username)
    except NoResultFound:
        raise OauthError("No user found with that email, or password invalid.")
    if not user.isConfirmed():
        raise OauthError("Email not confirmed")
    if not user.authenticate(password):
        raise OauthError("No user found with that email, or password invalid.")

    token_response = {
            "access_token": "",
            "token_type": "Bearer",
            "expires_in": current_app.config["JWT_EXP"],
            "refresh_token": ""
            }
    delta = timedelta(seconds=int(current_app.config["JWT_EXP"]))
    exp = datetime.now() + delta
    exp_timestamp = int(exp.timestamp())
    claims = {} # jwt claims
    claims["aud"] = current_app.config["JWT_AUD"]
    claims["exp"] = exp_timestamp
    claims["sub"] = user.id
    claims["iss"] = "pytrue"
    access_token, refresh_token = user.issueAccessToken(claims)
    token_response["access_token"] = access_token
    token_response["refresh_token"] = refresh_token

    return jsonify(token_response), 200

def refreshTokenGrant():
    """ Implements refresh token grant"""
    refresh_token = request.form.get('refresh_token')
    if not refresh_token:
        raise OauthError("refresh_token required")

    token_response = {
            "access_token": "",
            "token_type": "Bearer",
            "expires_in": current_app.config["JWT_EXP"],
            "refresh_token": ""
            }
    
    try:
        token = RefreshToken.find_by(token=refresh_token)
        user = token.user
        if token.revoked:
            raise OauthError("Invalid Refresh Token")
        token.revoked = True
        token.save()

        delta = timedelta(seconds=int(current_app.config["JWT_EXP"]))
        exp = datetime.now() + delta
        exp_timestamp = int(exp.timestamp())
        claims = {} # jwt claims
        claims["aud"] = current_app.config["JWT_AUD"]
        claims["exp"] = exp_timestamp
        claims["sub"] = user.id
        claims["iss"] = "pytrue"

        access_token, refresh_token = user.issueAccessToken(claims)
        token_response["access_token"] = access_token
        token_response["refresh_token"] = refresh_token

    except NoResulFound:
        raise OauthError("Invalid Refresh Token")

    return jsonify(token_response), 200
