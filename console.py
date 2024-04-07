#!/usr/bin/python3
"""Console module"""
import cmd
from os import getenv
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
        """Create an object of any class"""
        if not args:
            print("** class name missing **")
            return

        kwargs_dict = {}
        class_name = args.split()[0]
        params = args.split()[1:]

        if class_name not in self.__classes:
            print("** class doesn't exist **")
            return

        for param in params:
            key, value = param.split("=")
            try:
                value = int(value)
            except ValueError:
                try:
                    value = float(value)
                except ValueError:
                    value = " ".join(value.strip('"').split("_"))
            kwargs_dict[key] = value

        new_instance = self.__classes[class_name](**kwargs_dict)
        print(new_instance.id)
        new_instance.save()

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

    def do_all(self, args):
        """Shows all objects, or all objects of a class"""
        print_list = []

        if (getenv("HBNB_TYPE_STORAGE") != "db"):
            if args:
                args = args.split(" ")[0]  # remove possible trailing args
                if args not in self.__classes:
                    print("** class doesn't exist **")
                    return
                for k, v in storage._FileStorage__objects.items():
                    if k.split(".")[0] == args:
                        print_list.append(str(v))
            else:
                for k, v in storage._FileStorage__objects.items():
                    print_list.append(str(v))
        else:
            if args:
                args = args.split(" ")[0]  # remove possible trailing args
                if args not in self.__classes:
                    print("** class doesn't exist **")
                    return
                for k, v in storage.all(self.__classes[args]).items():
                    if k.split(".")[0] == args:
                        print_list.append(str(v))
            else:
                for k, v in storage.all().items():
                    print_list.append(str(v))

        print(print_list)

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
