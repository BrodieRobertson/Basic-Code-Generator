class Parameter:
    def __init__(self, data_type, name, value=None):
        if isinstance(data_type, str):
            self._data_type = data_type
        else:
            raise TypeError(f'data_type must be a {type(str)} but instead is {type(name)}')

        if isinstance(name, str):
            self._name = name
        else:
            raise TypeError(f'fame must be a {type(str)} but instead is {type(name)}')

        self._value = value

    @property
    def data_type(self):
        return self._data_type

    @property
    def name(self):
        return self._name

    @property
    def value(self):
        return self._value


def test():
    print('Beginning Parameter Test')


def main():
    test()


if __name__ == '__main__':
    main()
