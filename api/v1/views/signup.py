#!/usr/bin/python3
""" Signup view """
from api.v1.forms import SignupForm
from api.v1.views import api_views
from flask import jsonify, request, make_response, abort
from models.user import User
from werkzeug.security import generate_password_hash
from werkzeug.exceptions import BadRequest
from datetime import datetime


@api_views.route('/signup', methods=['POST'], strict_slashes=False)
def signup():
    """ signup endpoint """
    req_json = request.get_json()
    form = SignupForm.from_json(req_json)
    print(req_json)
    if form.validate():
        user = User(email=form.email.data,
                password=generate_password_hash(form.password.data))
        # Todo send confirmation email
        user.confirmation_sent_at = datetime.utcnow()
        user.save()
        return jsonify(user.to_dict()), 201
    raise BadRequest(form.errors)
