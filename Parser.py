from Generator import *
from Parameter import Parameter
from sys import argv


class Parser:
    generator_commands = dict(JAVA=Java('', False))

    def __init__(self, input_file):
        """
        Constructs the Parser

        :param input_file: The name of the input file
        """
        self._input_file = input_file
        self._line_number = 1
        self._generator = None

    def parse_file(self):
        """
        Parses the input file and calls upon the generator to create the output
        """
        with open(self._input_file, 'rt') as file:
            for line in file:
                line_values = line.split()
                print(line_values)
                # If there's no values in the line
                if not line_values:
                    raise TypeError()

                # If command is a language command
                if line_values[0] in self.generator_commands.keys():
                    self.language_command(line_values)

                # If command is class command
                elif line_values[0] == 'C':
                    self.class_command(line_values)

                # If command is superclass command
                elif line_values[0] == 'S':
                    self.superclass_command(line_values)

                # If command is interface commands
                elif line_values[0] == 'I':
                    self.interface_command(line_values)

                # If command is class variable command
                elif line_values[0] == 'CV':
                    self.class_variable_command(line_values)

                # If command is constant command
                elif line_values[0] == 'CT':
                    self.constant_command(line_values)

                # If command is constructor command
                elif line_values[0] == 'CR':
                    self.constructor_command(line_values)

                # If the command is method command
                elif line_values[0] == 'M':
                    self.method_command(line_values)

                # If command is end command
                elif line_values[0] == 'E':
                    self._generator.end()

                # Invalid command
                else:
                    raise TypeError(f'Invalid command on line {self._line_number}')

                self._line_number += 1

    def language_command(self, line_values):
        """
        Calls the language command in the generator

        :param line_values: A line of the input file
        :raises TypeError: If less than 2 arguments in the line_values or more than 3
        """
        # Error if less than 2 arguments
        if len(line_values) < 2:
            raise TypeError(f'Not enough arguments in the language command on line: {self._line_number}')
        # Open generator without comments
        elif len(line_values) == 2:
            self._generator = self.generator_commands[line_values[0]]
            self._generator.file_name = line_values[1]
        # Open generator with comments
        elif len(line_values) == 3 and line_values[2] == 'GC':
            self._generator = self.generator_commands[line_values[0]]
            self._generator.file_name = line_values[1]
            self._generator.generate_comments = True
        # Error if more than 3 arguments
        else:
            raise TypeError(f'Too many arguments in language command on line: {self._line_number}')

    def class_command(self, line_values):
        """
        Calls the class command in the generator

        :param line_values: A line of the input file
        :raises TypeError: If less than 2 arguments in the line_values or more than 2
        """
        # Error if less than 2 arguments
        if len(line_values) < 2:
            raise TypeError(f'Not enough arguments in the class command on line: {self._line_number}')
        # Generate class name
        elif len(line_values) == 2:
            self._generator.class_name(line_values[1])
        # Error if more than 2 arguments
        else:
            raise TypeError(f'Too many arguments in the class command on line: {self._line_number}')

    def superclass_command(self, line_values):
        """
        Calls upon the superclass command in the generator

        :param line_values: A line of the input file
        :raises TypeError: If less 2 arguments in the line_values or more than 2
        """
        # Error is less than 2 errors
        if len(line_values) < 2:
            raise TypeError(f'Not enough arguments in the superclass command on line: {self._line_number}')
        # Generate superclass
        elif len(line_values) == 2:
            self._generator.superclass(line_values[1])
        # Error if more than 2 arguments
        else:
            raise TypeError(f'Too many arguments in the superclass command on line: {self._line_number}')

    def interface_command(self, line_values):
        """
        Calls upon the interface command in the generator

        :param line_values: A line of the input file
        :raises TypeError: If less than 2 arguments in the line_values or more than 2
        """
        # Error if less than 2 arguments
        if len(line_values) < 2:
            raise TypeError(f'Not enough arguments in the interface commands on line: {self._line_number}')
        # Generate interface
        elif len(line_values) == 2:
            self._generator.interface(*line_values[1].split(','))
        # Error if more than 2 arguments
        else:
            raise TypeError(f'Too many arguments in the interface commands on line: {self._line_number}')

    def class_variable_command(self, line_values):
        """
        Calls upon the class variable command in the generator

        :param line_values: A line of the input file
        :raises TypeError: If less than 3 arguments in the line_values or more than 4
        """
        # Error if less than 3 arguments
        if len(line_values) < 3:
            raise TypeError(f'Not enough arguments in the class variable command on line: {self._line_number}')
        # Generate class variable
        elif len(line_values) == 3:
            self._generator.variable(True, False, False, 'PUB', Parameter(line_values[1], line_values[2]))
        # Generate class variable and getters/setters
        elif len(line_values) == 4:
            getter = False
            setter = False
            if 'G' == line_values[3]:
                getter = True
            elif 'S' == line_values[3]:
                setter = True
            elif 'GS' == line_values[3]:
                getter = True
                setter = True
            elif 'SG' == line_values[3]:
                getter = True
                setter = True
            else:
                raise TypeError(f'Invalid command in class variable command on line: {self._line_number}')
            self._generator.variable(True, getter, setter, 'PUB', Parameter(line_values[1], line_values[2]))

        # Error if more than 4 arguments
        else:
            raise TypeError(f'Too many arguments in the class variable command on line: {self._line_number}')

    def constant_command(self, line_values):
        """
        Calls upon the constant command in the generator

        :param line_values: A line of the input file
        :raises TypeError: If less than 4 arguments in the line_values or more than 4
        """
        # Error if less than 4 arguments
        if len(line_values) < 4:
            raise TypeError(f'Not enough argument in the constant command on line: {self._line_number}')
        # Generate constant
        elif len(line_values) == 4:
            self._generator.constant('PUB', Parameter(line_values[1], line_values[2], line_values[3]))
        # Error if more than 4 arguments
        else:
            raise TypeError(f'Too many arguments in the constant command on line: {self._line_number}')

    def constructor_command(self, line_values):
        """
        Calls upon the constructor command in the generator

        :param line_values: A line of the input file
        :raises TypeError: If more than 2 arguments in the line_values
        """
        # Generate constructor with no arguments
        if len(line_values) == 1:
            self._generator.constructor()
        # Generate constructor with arguments
        elif len(line_values) == 2:
            parameter_list = self.generate_parameter_list(line_values[1])
            self._generator.constructor(*parameter_list)
        # Error if more than 2 arguments
        else:
            raise TypeError(f'Too many arguments in the constructor command on line: {self._line_number}')

    def method_command(self, line_values):
        """
        Calls upon the method command in the generator

        :param line_values: A line of the input file
        :raises TypeError: If less than 4 arguments in the line_values or more than 5
        """
        # Error if  less than 4 commands
        if len(line_values) < 4:
            raise TypeError(f'Not enough arguments in the method command on line: {self._line_number}')
        # Generate method with no arguments
        elif len(line_values) == 4:
            self._generator.method(line_values[1], line_values[2], line_values[3])
        # Generate method with arguments
        elif len(line_values) == 5:
            parameter_list = self.generate_parameter_list(line_values[4])
            self._generator.method(line_values[1], line_values[2], line_values[3], *parameter_list)
        # Error if more than 5 arguments
        else:
            raise TypeError(f'Too many arguments in the method command on line: {self._line_number}')

    def generate_parameter_list(self, input_parameters):
        """
        Generates a parameter list from a set of parameters

        :param input_parameters: A set of parameters
        :return:
        """
        parameters = input_parameters.split(',')
        parameter_list = list()
        for value in parameters:
            parameter = value.split(':')
            parameter_list.append(Parameter(parameter[0], parameter[1]))

        return parameter_list


def main():
    if len(argv) == 1:
        parser = Parser('ExampleInput.txt')
    else:
        parser = Parser(argv[1])

    parser.parse_file()


if __name__ == '__main__':
    main()
