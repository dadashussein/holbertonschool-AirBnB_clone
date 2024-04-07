#!/usr/bin/python3
"""FileStorage class"""
import json


class FileStorage:
    """FileStorage class"""
    __file_path = "file.json"
    __objects = {}

    @property
    def objects(self):
        return self.__objects

    @objects.setter
    def objects(self, value):
        self.__objects = value

    def all(self, cls=None):
        if cls:
            temp = {}
            for key, value in self.__objects.items():
                if cls.__name__ in key:
                    temp[key] = value
            return temp
        return self.__objects

    def new(self, obj):
        """ Add object to objects"""
        key = obj.__class__.__name__ + "." + obj.id
        self.__objects[key] = obj

    def save(self):
        """ Save objects to file"""
        ser_object = {}
        for key, obj in self.__objects.items():
            ser_object[key] = obj.to_dict()
        with open(self.__file_path, "w") as file:
            json.dump(ser_object, file)

    def reload(self):
        """ Reload objects from file"""
        from models.base_model import BaseModel
        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review

        classes = {
        "BaseModel": BaseModel,
        "User": User,
        "State": State,
        "City": City,
        "Amenity": Amenity,
        "Place": Place,
        "Review": Review
        }
        try:
            temp = {}
            with open(self.__file_path, "r") as file:
                temp = json.load(file)
                for key, value in temp.items():
                    self.all()[key] = classes[value['__class__']](**value)
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """Delete object instance"""
        if obj:
            key = obj.__class__.__name__ + '.' + obj.id
            if key in self.all():
                del self.all()[key]
            self.save()
