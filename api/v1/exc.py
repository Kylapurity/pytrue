#!/usr/bin/python3
""" Exceptions classes """
from werkzeug.exceptions import HTTPException

class OauthError(HTTPException):
    description = "invalid error"
    code = 400
