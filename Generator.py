from abc import ABC, abstractmethod
from Parameter import Parameter


class Generator(ABC):
    def __init__(self, file_name, generate_comments):
        self._file_name = file_name
        self._generate_comments = generate_comments
        self._output = dict()

    @abstractmethod
    def method(self, access_level, return_type, name):
        pass

    @abstractmethod
    def variable(self, mutable, generate_getter, generate_setter, access_level, parameter):
        pass

    @abstractmethod
    def end(self):
        pass

    @property
    def file_name(self):
        return self._file_name

    @file_name.setter
    def file_name(self, value):
        self._file_name = value

    @property
    def generate_comments(self):
        return self._generate_comments

    @generate_comments.setter
    def generate_comments(self, value):
        self._generate_comments = value


class ObjectOriented(Generator):
    @abstractmethod
    def class_name(self, name):
        pass

    @abstractmethod
    def superclass(self, name):
        pass

    @abstractmethod
    def interface(self, *args):
        pass

    @abstractmethod
    def constructor(self, *args):
        pass

    @abstractmethod
    def method(self, access_level, return_type, name):
        pass

    @abstractmethod
    def variable(self, mutable, generate_getter, generate_setter, access_level, parameter):
        pass

    @abstractmethod
    def end(self):
        pass


class Java(ObjectOriented):
    HEADER = 'header'
    CLASS = 'class'
    VARIABLE = 'variable'
    CONSTRUCTOR = 'constructor'
    METHOD = 'method'
    CLASS_END = 'class_end'
    types = dict(bool='boolean', str='String')
    levels = dict(PUB='public', PRI='private', PRO='protected')

    def __init__(self, file_name, generate_comments):
        """
        Constructs a Java generator

        :param file_name: The name of the output file
        :param generate_comments: Whether comments should be generated or not
        """
        super().__init__(file_name, generate_comments)

    def header_comment(self):
        """
        Generates the class header comment

        :return: A header comment
        """
        comment = '/**\n *\n */\n'
        return comment

    def comment(self):
        """
        Generates the comment for a method and variable

        :return: A comment
        """
        comment = '\n\t/**\n\t *\n\t */'
        return comment

    def class_name(self, name):
        """
        Generates a class definition

        :param name: The name of the class
        :return: A Java class definition
        """
        if self._generate_comments:
            self._output[self.HEADER] = self.header_comment()
        if name != self._file_name:
            raise ValueError()
        self._output[self.CLASS] = f'public class {name} ' + '\n{\n'

    def superclass(self, name):
        """
        Generates a class definition with a superclass

        :param name: The name of the superclass
        :return: A Java class definition with a super class
        """
        class_value = self.class_value()
        self._output[self.CLASS] = f'{class_value} extends {name} ' + '\n{\n'

    def interface(self, *args):
        """
        Generates a class definition with interfaces

        :param args: The interface names
        :return: A Java class definition with a interfaces
        """
        class_value = self.class_value()
        class_value += ' implements '
        for interface in args:
            class_value += interface
            if args.index(interface) < len(args) - 1:
                class_value += ', '
        self._output[self.CLASS] = class_value + '\n{\n'

    def class_value(self):
        """
        Cleans the bracket off a class definition

        :return: A Java class definition without the bracket
        """
        class_value = self._output[self.CLASS]
        class_value = class_value[0:len(class_value) - 4]
        return class_value

    def constructor(self, *args):
        """
        Generates a constructors

        :param args: The arguments for the constructor
        :return: A Java constructor definition
        """
        constructor = ''
        if self._generate_comments:
            constructor += self.comment()
        constructor += f'\n\tpublic {self._file_name}({self.build_parameter_list(args)})\n\t' + '{\n\n\t}\n'
        self.add_to_output(self.CONSTRUCTOR, constructor)

    def method(self, access_level, return_type, name, *args):
        """
        Generates a method

        :param access_level: The access level of the method
        :param return_type: The return type of the method
        :param name: The name of the method
        :param args: The arguments of the method
        :return: A Java method definition
        """
        language_level = self.lookup_level(access_level)
        language_return_type = self.lookup_type(return_type)
        no_return = '\n\n\t'
        if language_return_type in ('byte', 'short', 'int', 'float', 'double', 'long'):
            return_value = '0'
        elif language_return_type == 'boolean':
            return_value = 'false'
        elif language_return_type == 'char':
            return_value = "''"
        else:
            return_value = 'null'

        return_statement = f'\n\t\treturn {return_value};\n\t'
        method = ''

        if self._generate_comments:
            method += self.comment()
        method += f'\n\t{language_level} {language_return_type} {name}' \
                  f'({self.build_parameter_list(args)})\n\t' + '{' + \
                  f'{no_return if language_return_type == "void" else return_statement}' + '}\n'

        self.add_to_output(self.METHOD, method)

    def constant(self, access_level, values):
        """
        Generates a constant

        :param access_level: The access level of the parameter
        :param values: The values of the constant
        :return: A Java constant
        """
        self.variable(False, False, False, access_level, values)

    def variable(self, mutable, generate_getter, generate_setter, access_level, values):
        """
        Generates a variable

        :param mutable: Whether the value of the variable can be changed
        :param generate_getter: Whether a getter is generated
        :param generate_setter: Whether a setter is generated
        :param access_level: The access level on the variable
        :param values: The values of the variable
        :return: A Java variable
        """
        language_access_level = self.lookup_level(access_level)
        parameter_type = self.lookup_type(values.data_type)
        variable = ''

        if self._generate_comments:
            variable += self.comment() + '\n'
        variable += f'\t{language_access_level} {"" if mutable else "static final "}{parameter_type} ' \
                    + f'{values.name}{" = " + values.value if values.value else ""};\n'
        self.add_to_output(self.VARIABLE, variable)
        if generate_getter:
            self.method('PUB', f'{parameter_type}', f'get{values.name.capitalize()}')
        if generate_setter:
            self.method('PUB', 'void', f'set{values.name.capitalize()}', Parameter(f'{parameter_type}', 'value'))

    def end(self):
        """
        Completes the document and outputs it
        """
        self._output[self.CLASS_END] = '}'
        with open(f'{self._file_name}.java', 'wt') as file:
            if self._output.get(self.HEADER):
                file.write(self._output[self.HEADER])
            if self._output.get(self.CLASS):
                file.write(self._output[self.CLASS])
            if self._output.get(self.VARIABLE):
                file.write(self._output[self.VARIABLE])
            if self._output.get(self.CONSTRUCTOR):
                file.write(self._output[self.CONSTRUCTOR])
            if self._output.get(self.METHOD):
                file.write(self._output[self.METHOD])
            if self._output.get(self.CLASS_END):
                file.write(self._output[self.CLASS_END])

        print('Output Complete')

    def add_to_output(self, key, output):
        """
        Adds a value to a section of the output

        :param key: The section of the output
        :param output: The value being added
        """
        all_key = self._output.get(key)
        if all_key:
            all_key += output
            self._output[key] = all_key
        else:
            self._output[key] = output

    def lookup_type(self, key):
        """
        Looks up a Java equivalent of a parser type

        :param key: The parser type
        :return: The Java type
        """
        lookup_type = self.types.get(key)
        data_type = lookup_type if lookup_type else key
        return data_type

    def lookup_level(self, key):
        """
        Looks up a Java equivalent access level of a parser access level

        :param key: The parser level
        :return: The Java access level
        """
        lookup_level = self.levels.get(key)
        access_level = lookup_level if lookup_level else ''
        return access_level

    def build_parameter_list(self, parameters):
        """
        Builds a parameter list from a set of parameters

        :param parameters: The parameters
        :return: The parameter list
        """
        parameter_list = ''
        for parameter in parameters:
            data_type = self.lookup_type(parameter.data_type)
            parameter_list += f'{data_type} {parameter.name}'

            if parameters.index(parameter) < len(parameters) - 1:
                parameter_list += ', '

        return parameter_list


if __name__ == '__main__':
    x = Java('Test', True)
    x._file_name = 'BillyBob'
    x.class_name('BillyBob')
    x.superclass('Object')
    x.interface('Cloneable', 'Serializable')
    x.constructor(Parameter('str', 'test'), Parameter('Object', 'anotherTest'))
    x.constructor(Parameter('str', 'test'))
    x.variable(False, False, False, 'PUB', Parameter('Integer', 'firstVariable', '10'))
    x.variable(True, True, True, 'PRI', Parameter('int', 'secondVariable', '10'))
    x.method('PUB', 'str', 'testMethod', Parameter('str', 'test'), Parameter('Object', 'anotherTest'))
    x.end()
    print(x._output[x.CLASS], end='')
    print(x._output[x.VARIABLE], end='')
    print(x._output[x.CONSTRUCTOR], end='')
    print(x._output[x.METHOD], end='')
    print(x._output[x.CLASS_END], end='')
