#!/usr/bin/python3
"""Unittest for base model"""
import unittest
import os
from models.base_model import BaseModel
from models import storage


class TestBaseModel(unittest.TestCase):
    """Class to test base model module"""

    def setUp(self):
        try:
            os.remove("file.json")
        except IOError:
            pass

    def test_base(self):
        """Test base case"""
        base_instance = BaseModel()
        self.assertIsInstance(base_instance, BaseModel)
        self.assertEqual(base_instance.__class__.__name__, "BaseModel")

    def test_str(self):
        """str method case"""
        base_instance = BaseModel()
        base_instance.name = "My First Model"
        base_instance.my_number = 89
        base_instance_str = base_instance.__str__()
        self.assertEqual(base_instance_str,
                         "[BaseModel] ({}) {}".format(base_instance.id,
                                                      base_instance.__dict__))

    def test_save(self):
        """save method cases"""
        base_instance = BaseModel()
        base_instance.save()
        self.assertNotEqual(base_instance.created_at, base_instance.updated_at)

    def test_save_storage(self):
        """save method case with storage"""
        base_model = BaseModel()
        base_model.name = "My_First_Model"
        base_model.my_number = 89
        base_model.save()
        self.assertTrue(os.path.exists("file.json"))
        self.assertIn("BaseModel." + base_model.id, storage.all())

    def test_to_dict(self):
        """to_dict method case"""
        base_instance = BaseModel()
        base_instance_dict = base_instance.to_dict()
        self.assertEqual(base_instance_dict["__class__"], "BaseModel")
        self.assertEqual(base_instance_dict["id"], base_instance.id)
        self.assertEqual(base_instance_dict["updated_at"],
                         base_instance.updated_at.isoformat())

    def test_init(self):
        """init method case"""
        my_model = BaseModel()
        my_new_model = BaseModel()
        self.assertNotEqual(my_model.id, my_new_model.id)


if __name__ == "__main__":
    unittest.main()
