#!/usr/bin/python3
""" Refresh Tokens data model """
from models import db
from models.base_model import BaseModel


class RefreshToken(BaseModel, db.Model):
    """ Refresh tokens mapped data class """
    __tablename__ = 'refresh_tokens'

    token = db.Column(db.String(60), nullable=False, unique=True)
    user_id = db.Column(db.String(60), db.ForeignKey('users.id'), index=True)
    revoked = db.Column(db.Boolean, nullable=True, default=False)
    user = db.relationship('User', backref='refresh_tokens')
