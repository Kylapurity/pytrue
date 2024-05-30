#!/usr/bin/python3
""" Helper functions """


def extractJWTToken(req):
    """Extract bearer token from Authorization header"""
    header_value = req.headers.get("Authorization")
    if not header_value.startswith("Bearer"):
        raise ValueError("Invalid Authorization header format")
    try:
        encoded_token = header_value.split(" ")[1]
        return encoded_token
    except IndexError:
        raise ValueError("invalid token")
