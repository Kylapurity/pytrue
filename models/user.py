#!/usr/bin/python3
""" User model """
from models import db
from models.base_model import BaseModel
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import NoResultFound
from models import tokens
from flask import current_app

class User(BaseModel, db.Model):
    """ User class model """


    __tablename__ = "users"
    aud = db.Column(db.String(100))
    role = db.Column(db.String(100))
    email = db.Column(db.String(250), unique=True, nullable=False)
    _password = db.Column('password', db.String(250), nullable=False)
    confirmation_token = db.Column(db.String(250))
    confirmation_send_at = db.Column(db.DateTime)
    is_confirmed = db.Column(db.Boolean(), default=False)
    recovery_token = db.Column(db.String(250))
    recovery_sent_at = db.Column(db.DateTime)
    is_super_admin = db.Column(db.Boolean(), nullable=True)

    @property
    def password(self):
        return self._password
    
    @password.setter
    def password(self, value):
        """ password setter """
        self._password = generate_password_hash(value)

    def to_dict(self):
        """User to dict"""
        out_dict = {
                "id": self.id,
                "email": self.email,
                "confirmation_sent_at": self.confirmation_send_at,
                "created_at": self.created_at,
                "updated_at": self.updated_at,
                }
        return out_dict

    def isConfirmed(self):
        """Returns True is user is email confirmed"""
        return self.is_confirmed == True

    def authenticate(self, password):
        """checks the password provided against db one"""
        return check_password_hash(self._password, password)
   
    def exists(self):
        """Checks if email exists"""
        try:
            self.find_by(email=self.email)
            return True
        except NoResultFound:
            return False

    def issueAccessToken(self, claims: str):
        """ Create access token and its refresh token"""
        import jwt

        refresh_token = tokens.grantAuthenticatedUser(self.id)
        access_token = jwt.encode(claims,
                current_app.config["JWT_SECRET"], algorithm="HS256")
        return (access_token, refresh_token)
