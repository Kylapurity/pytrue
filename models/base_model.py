#!/usr/bin/python3
""" Base model """
from models import db
from datetime import datetime
import uuid


date_format = "%Y-%m-%dT%H:%M:%S.%f"
class BaseModel():
    """ Base Model """

    id = db.Column(db.String(60), primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        """ Inits the default fields """
        if kwargs:
            for column, value in kwargs.items():
                if hasattr(self, column):
                    setattr(self, column, value)
                if kwargs.get("created_at", None) and type(
                        self.created_at) is str:self.created_at =datetime.strptime(
                                kwargs["created_at"], date_format)
                else:
                    self.created_at = datetime.utcnow()
                if kwargs.get("updated_at", None) and type(self.updated_at) is str:
                    self.updated_at = datetime.strptime(
                            kwargs["updated_at"], date_format)
                else:
                    self.updated_at = datetime.utcnow()
                if kwargs.get("id", None) is None:
                    self.id = str(uuid.uuid4())
        else:
            id = str(uuid.uuid4())
            created_at = datetime.utcnow()
            updated_at = self.created_at

    def __str__(self):
        """String representation of the BaseModel class"""
        return f"User({self.email})"

    def save(self):
        """ Saves the user to data store """
        self.updated_at = datetime.utcnow()
        db.session.add(self)
        db.session.commit()
    
    @classmethod
    def find_by(cls, **kwargs):
        """ FInd user by dict """
        obj = db.session.query(cls).filter_by(**kwargs).one()
        return obj
    @classmethod
    def update(cls, id: int, **kwargs):
        """ updates the data model """
        obj = db.session.query(cls).get(id)
        if obj is None:
            return None
        update_source = {}
        for key, value in kwargs.items():
            if hasattr(cls, key):
                update_source[getattr(cls, key)] = value
            else:
                raise ValueError()
        db.session.query(cls).filter(cls.id == id).update(
            update_source,
            synchronize_session=False,
        )
        db.session.commit()

    def delete(self):
        """ remove user model from the  storage """
        db.session.delete(self)
        db.session.commit()
