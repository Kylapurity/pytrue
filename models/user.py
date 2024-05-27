#!/usr/bin/python3
""" User model """
from models import db
from models.base_model import BaseModel
from werkzeug.security import generate_password_hash, check_password_hash


class User(BaseModel, db.Model):
    """ User class model """


    __tablename__ = "users"
    aud = db.Column(db.String(100))
    role = db.Column(db.String(100))
    email = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    confirmation_token = db.Column(db.String(250))
    confirmation_send_at = db.Column(db.DateTime)
    isConfirmed = db.Column(db.Boolean(), default=False)
    recovery_token = db.Column(db.String(250))
    recovery_sent_at = db.Column(db.DateTime)
    is_super_admin = db.Column(db.Boolean(), nullable=True)

    #  @password.setter
    def password(self, value):
        """ password setter """
        self.password = generate_password_hash(value)

    def to_dict(self):
        """User to dict"""
        out_dict = {
                "id": self.id,
                "email": self.email,
                "confirmation_sent_at": self.confirmation_sent_at,
                "created_at": self.created_at,
                "updated_at": self.updated_at,
                }
        return out_dict

    def isConfirmed(self):
        """Returns True is user is email confirmed"""
        return self.isConfirmed == True

    def authenticate(self, password):
        """checks the password provided against db one"""
        return check_password_hash(self.password, password)
