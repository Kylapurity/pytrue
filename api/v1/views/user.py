#!/usr/bin/python3
""" Blueprint for user management"""
from models.user import User
from api.v1.views import api_views
from models import tokens
from flask import request, jsonify


@api_views.route('/user', methods=["GET"], strict_slashes=False)
def get_user():
    """Get current api user"""
    user = request.current_user
    return jsonify(user.to_dict()), 200

@api_views.route('/logout', methods=["GET"], strict_slashes=False)
def logout():
    """Logout endpoint"""
    user = request.current_user
    tokens.logout(user.id)
    return '', 204
