import os

class TemporaryEnvironmentVariableSetter:
    def __init__(self, environment_variables: dict[str, str]):
        self.__environment_variables = environment_variables
        self.__previous_values: dict[str, str|None] = {}

    def __enter__(self):
        for name, value in self.__environment_variables.items():
            self.__previous_values[name] = os.getenv(name, None)
            os.environ[name] = value

    def __exit__(self, exc_type, exc_val, exc_tb):
        for name, value in self.__environment_variables.items():
            if self.__previous_values[name] is None:
                os.unsetenv(name)
                continue

            os.environ[name] = value
