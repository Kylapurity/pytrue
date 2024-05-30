#!/usr/bin/python3
""" Exceptions classes """
from werkzeug.exceptions import HTTPException

class OauthError(HTTPException):
    """900* `Oauth Error`

    Raise if there is any error encountered during Oauth handling
    or server
    """

    code = 900
    description = (
        "Oauth error"
    )
