import json
import sys


class Dynamic:
    """A dynamic class whose properties can be configured from an external file."""

    def __init__(self):
        self.declared = []
        self.hidden = {}
        self.properties = {}
        self.read_properties()
        self.present()

    def read_properties(self):
        try:
            with open('properties.json', 'r') as properties:
                self.properties = json.load(properties)
                for item, value in self.properties['all'].items():
                    setattr(Dynamic, item, value)
                    setattr(self, item, None)
                    self.declared.append(item)
                self.key_conditions = self.properties["key_conditions"]
                self.value_conditions = self.properties["value_conditions"]
        except json.JSONDecodeError as error:
            print(error)
            sys.exit(1)

    def setattr_(self, name, value):
        if isinstance(getattr(Dynamic, name), list):
            if value not in getattr(Dynamic, name):
                raise ValueError(
                    f"Please enter a value for {name} among {getattr(Dynamic, name)}")
            if self.check_value_validity(name, value):
                setattr(self, name, value)
            else:
                raise ValueError("Please enter a valid choice.")
            return

        try:
            if getattr(Dynamic, name) == "int":
                value = int(value)
        except ValueError:
            raise ValueError("Please enter an integer value")

        try:
            if getattr(Dynamic, name) == "float":
                value = float(value)
        except ValueError:
            raise ValueError("Please enter a floating point value")

        setattr(self, name, value)

    def present(self):
        print("\n*********\n")

        for idx, item in enumerate(self.declared):
            if self.check_key_validity(item):
                if isinstance(getattr(Dynamic, item), list):
                    options = [value for value in getattr(
                        Dynamic, item) if self.check_value_validity(item, value)]
                else:
                    options = getattr(Dynamic, item)
                print(f"{idx} -> {item} ({options}) :  {getattr(self, item)}")

        print("Please enter your choice. Enter -1 to exit.")
        try:
            modify = int(input())
            if modify == -1:
                self.exit()
        except ValueError as error:
            print("Please enter an integer value.")
            self.present()

        try:
            item = self.declared[modify]
            if not self.check_key_validity(item):
                raise ValueError("Please enter a valid choice.")
            print(f"Please enter a value for {self.declared[modify]}.")
            value = input()
            self.setattr_(item, value)
            self.present()
        except ValueError as error:
            print(error)
            self.present()
        except IndexError as error:
            print("Please enter a valid choice.")
            self.present()
        except TypeError as error:
            print(error)
            self.present()

    def eval_expression(self, conditions):
        for condition in conditions:
            operand = condition[0]
            operator = condition[1]
            parameter = condition[2]
            operand_value = getattr(self, operand)
            if operand_value is None:
                return False
            if isinstance(parameter, str):
                check = f"'{operand_value}' {operator} '{parameter}'"
            else:
                check = f"{operand_value} {operator} {parameter}"

            if eval(check) is False:
                return False

        return True

    def check_key_validity(self, item):
        if item not in self.key_conditions:
            return True

        key_conditions = self.key_conditions[item]
        return self.eval_expression(key_conditions)

    def check_value_validity(self, item, value):
        if item not in self.value_conditions:
            return True

        value_condition_item = self.value_conditions[item]
        if value not in value_condition_item:
            return True

        value_conditions = value_condition_item[value]
        return self.eval_expression(value_conditions)

    def exit(self):
        for idx, item in enumerate(self.declared):
            if self.check_key_validity(item):
                if isinstance(getattr(Dynamic, item), list):
                    options = [value for value in getattr(
                        Dynamic, item) if self.check_value_validity(item, value)]
                else:
                    options = getattr(Dynamic, item)
                print(f"{idx} -> {item} ({options}) :  {getattr(self, item)}")

        sys.exit(0)


if __name__ == "__main__":
    dynamic = Dynamic()
    """
    Features:
    1. Display options dynamically in the menu.
    2. Separate 'number' format into int and float for better precision.

    Possible improvements:
    1. Code the program to be able to go back from an option
    2. Write out code to unset variables.
    3. Regarding expansion A2, if the conditions for a value are not met after the value is set, the value doesn't unset automatically.
    """