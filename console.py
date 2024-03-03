#!/usr/bin/python3
"""Console module"""
import cmd
from models.base_model import BaseModel
from models import storage
from models.user import User
from models.city import City
from models.state import State
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class SysConsole(cmd.Cmd):
    """Console class"""
    prompt = '(hbnb) '
    __classes = ["BaseModel", "User", "State",
                 "City", "Amenity", "Place", "Review"]

    def do_quit(self, arg):
        """Quit command to exit program"""
        return True

    def do_EOF(self, arg):
        """EOF command to exit program"""
        return True

    def do_help(self, arg):
        """Help command"""
        return super().do_help(arg)

    def emptyline(self) -> bool:
        """Empty line"""
        return False

    def do_create(self, arg):
        """Create command"""
        if not arg:
            print("** class name missing **")
        elif arg not in self.__classes:
            print("** class doesn't exist **")
        else:
            new = eval(arg)()
            new.save()
            print(new.id)

    def do_show(self, arg):
        """Show model with id"""
        lines = arg.split(" ")
        if not arg:
            print("** class name missing **")
        elif lines[0] not in self.__classes:
            print("** class doesn't exist **")
        elif len(lines) < 2:
            print("** instance id missing **")
        else:
            key = lines[0] + "." + lines[1]
            if key in storage.all():
                print(storage.all()[key])
            else:
                print("** no instance found **")

    def do_destroy(self, arg):
        """Destroy instance"""
        lines = arg.split(" ")
        if not arg:
            print("** class name missing **")
        elif lines[0] not in self.__classes:
            print("** class doesn't exist **")
        elif len(lines) < 2:
            print("** instance id missing **")
        else:
            key = lines[0] + "." + lines[1]
            if key in storage.all():
                del storage.all()[key]
                storage.save()
            else:
                print("** no instance found **")

    def do_all(self, arg):
        """Print all string repr"""
        if not arg:
            print([str(value) for value in storage.all().values()])
        elif arg in self.__classes:
            print([str(value) for key, value in storage.all().items()
                   if key.startswith(arg)])
        else:
            print("** class doesn't exist **")

    def default(self, line):
        """Method default"""
        if '.' in line:
            args = line.split('.')
            class_name = args[0]
            command = args[1]
            if command == 'all()':
                self.do_all(class_name)
            elif command == 'count()':
                self.do_count(class_name)
            elif command.startswith('show'):
                instance_id = command.split('\"')[1]
                self.do_show(class_name + ' ' + instance_id)
            elif command.startswith('destroy'):
                instance_id = command.split('\"')[1]
                self.do_destroy(class_name + ' ' + instance_id)
            elif command.startswith('update'):
                instance_id = command.split('\"')[1]
                instance_key = command.split('\"')[3]
                instance_value = command.split()[-1].rstrip(')\"')
                self.do_update(class_name + ' ' + instance_id + ' ' +
                               instance_key + ' ' + instance_value)
        else:
            print("*** Unknown syntax: %s" % line)

    def do_count(self, arg):
        """Count instances"""
        count = 0
        for key in storage.all().keys():
            if arg in key:
                count += 1
        print(count)

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
            if key in storage.all():
                instance = storage.all()[key]
                attribute_name = lines[2]
                attribute_value = lines[3]
                if attribute_value.isdigit():
                    setattr(instance, attribute_name, int(attribute_value))
                elif attribute_value.replace('.', '', 1).isdigit():
                    setattr(instance, attribute_name, float(attribute_value))
                else:
                    attribute_value = attribute_value.strip('\"')
                    setattr(instance, attribute_name, str(attribute_value))
                instance.save()
            else:
                print("** no instance found **")


if __name__ == '__main__':
    SysConsole().cmdloop()
