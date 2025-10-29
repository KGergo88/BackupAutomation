import os

class TemporaryEnvironmentVariableSetter:
    def __init__(self, variable: str, value: str):
        self.__variable_name = variable
        self.__value = value
        self.__previous_value = os.getenv(variable, None)

    def __enter__(self):
        os.environ[self.__variable_name] = self.__value

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.__previous_value is None:
            os.unsetenv(self.__variable_name)
            return

        os.environ[self.__variable_name] = self.__previous_value
