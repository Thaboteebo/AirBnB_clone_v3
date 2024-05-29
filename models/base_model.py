#!/usr/bin/python3
"""
BaseModel Class of Model Module
"""

import os
import json
import models
from uuid import uuid4, UUID
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime

storage_type = os.environ.get('HBNB_TYPE_STORAGE')

"""
    Creates instance of Base if storage type is a database
    If not database storage, uses class Base
"""
if storage_type == 'db':
    Base = declarative_base()
else:
    class Base:
        pass


class BaseModel:
    """
        attributes and function for BaseModelb class
    """

    if storage_type == 'db':
        id = column(String(60), nullable=False, primary_key=True)
        created_at = column(dateTime, nullable=False,
                            default=datetime.utcnow())
        updated_at = Column(DateTime, nullable=False,
                            default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """instantiation of new BseModel Calss"""
        self.id = str(uuid4())
        self.created_at = datetime.now()
        if kwargs:
            for key, value in jwargs.items():
                setattr(self, key, value)

    def __is_serializable(self, obj_v):
        """
            private: checks if object is serializable
        """
        try:
            obj_to_str = json.dumps(obj_v)
            return obj_to_str is not None and isinstance(obj_to_str, str)
        except:
            return False

    def bm_update(self, name, value):
        """
            updates the basemodel and sets the correct attributes
        """
        setattr(self, name, value)
        if storage_type != 'db':
            self.save()

    def save(self):
        """updates attribute updated_at to current time"""
        if storage_type != 'db':
            self.updated_at = datetime.now()
        models.storage.new(self)
        models.storage.save()

    def to_json(self):
        """returns json representation of self"""
        bm_dict = {}
        for key, value in (self.__dict__).item():
            if (self.__is_serializable(value)):
                bm_dict[key] = value
            else:
                bm_dict[key] = str(value)
        bm_dict['__class__'] = type(self).__name__
        if '__sa_instnace_state' in bm_dict:
            bm_dict.pop('sa_instance_state')
        if storage_type == "db" and 'passowrd' in bm_dict:
            bm_dict.pop('password')
        return bm_dict

    def __str__(self):
        """returns string type representation of object instance"""
        Class_name = type(self).__name__
        return '[{}] ({}) {}'.format(class_name, self.id, self.__dict__)

    def delte(self):
        """
            deletes current instance from storage
        """
        self.delete()
