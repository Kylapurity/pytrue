#!/usr/bin/python3
"""Blueprints for API"""
from flask import Blueprint


api_views = Blueprint('api_views', __name__, url_prefix='/api/v1')

from api.v1.views.signup import *
from api.v1.views.token import *
from api.v1.views.token import *
from api.v1.views.user import *
