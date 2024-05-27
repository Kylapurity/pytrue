#!/usr/bin/python3
""" wtf forms """
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Email


class SignupForm(FlaskForm):
    """ Signup form """
    email = StringField('Email', [DataRequired(), Email(), Email()])
    password = StringField('Password', [DataRequired()])
