#!/usr/bin/python3
"""Console module"""
import cmd
from models.base_model import BaseModel
from models.__init__ import storage
from models.user import User
from models.city import City
from models.state import State
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class SysConsole(cmd.Cmd):
    """Console class"""
    prompt = '(hbnb) '
    __classes = {
        "BaseModel": BaseModel,
        "User": User,
        "State": State,
        "City": City,
        "Amenity": Amenity,
        "Place": Place,
        "Review": Review
    }

    def do_quit(self, arg):
        """Quit command to exit program"""
        exit()

    def do_EOF(self, arg):
        """EOF command to exit program"""
        print()
        exit()

    def do_help(self, arg):
        """Help command"""
        return super().do_help(arg)

    def emptyline(self):
        """Empty line"""
        pass

    def do_create(self, args):
        """Create an object of any class with given parameters"""
        args = args.split()
        if not args:
            print("** class name missing **")
            return
        elif args[0] not in self.__classes:
            print("** class doesn't exist **")
            return
        class_name = args[0]
        new_instance = self.__classes[class_name]()
        for arg in args[1:]:
            if "=" not in arg:
                continue
            key, value = arg.split("=", 1)
            if value[0] == value[-1] == '"':
                value = value[1:-1].replace('_', ' ').replace('\\', '"')
            elif '.' in value:
                value = float(value)
            else:
                value = int(value)
            setattr(new_instance, key, value)
        storage.save()
        print(new_instance.id)
        storage.save()

    def do_show(self, arg):
        """Show model with id"""
        lines = arg.partition(" ")
        c_name = lines[0]
        c_id = lines[2]
        if not c_name:
            print("** class name missing **")
            return

        if c_name not in self.__classes:
            print("** class doesn't exist **")
            return

        if not c_id:
            print("** instance id missing **")
            return

        key = c_name + "." + c_id
        try:
            print(storage._FileStorage__objects[key])
        except KeyError:
            print("** no instance found **")

    def do_destroy(self, arg):
        """Destroy specified object"""
        lines = arg.partition(" ")
        c_name = lines[0]
        c_id = lines[2]
        if not c_name:
            print("** class name missing **")
            return

        if c_name not in self.__classes:
            print("** class doesn't exist **")
            return

        if not c_id:
            print("** instance id missing **")
            return

        key = c_name + "." + c_id

        try:
            del storage.all()[key]
            storage.save()
        except KeyError:
            print("** no instance found **")

    def do_all(self, arg):
        """Show all objects"""
        if not arg:
            print([str(value) for value in storage.all().values()])
        elif arg in self.__classes:
            print([str(value) for key, value in storage.all().items()
                   if key.startswith(arg)])
        else:
            print("** class doesn't exist **")

    def default(self, line):
        """Method retrieve all instances"""
        if '.' in line:
            args = line.split('.')
            class_name = args[0]
            command = args[1]
            if command == 'all()':
                self.do_all(class_name)
        else:
            print("*** Unknown syntax: %s" % line)

    def do_update(self, arg):
        """Update att"""
        lines = arg.split(" ")
        if not arg:
            print("** class name missing **")
        elif lines[0] not in self.__classes:
            print("** class doesn't exist **")
        elif len(lines) < 2:
            print("** instance id missing **")
        elif len(lines) < 3:
            print("** attribute name missing **")
        elif len(lines) < 4:
            print("** value missing **")
        else:
            key = lines[0] + "." + lines[1]
            print(key)
            if key in storage.all():
                instance = storage.all()[key]
                attribute_name = lines[2]
                attribute_value = lines[3]
                setattr(instance, attribute_name, attribute_value)
                storage.save()
            else:
                print("** no instance found **")


if __name__ == '__main__':
    SysConsole().cmdloop()
