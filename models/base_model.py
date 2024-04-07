#!/usr/bin/python3
"""Base class"""
import uuid
from datetime import datetime


class BaseModel:
    """Base class"""
    def __init__(self, *args, **kwargs):
        if kwargs:
            for key, value in kwargs.items():
                if key == "created_at" or key == "updated_at":
                    value = datetime.fromisoformat(value)
                if key != "__class__":
                    setattr(self, key, value)
        else:
            from models import storage
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            storage.new(self)

    def __str__(self):
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"

    def save(self):
        """Updates updated attr"""
        from models import storage
        self.updated_at = datetime.now()
        storage.save()

    def to_dict(self):
        """Returns dic containing all keys/values"""
        result = {}
        for key, value in self.__dict__.items():
            if key == "updated_at" or key == "created_at":
                value = datetime.isoformat(value)
            result[key] = value
        result["__class__"] = self.__class__.__name__
        return result
