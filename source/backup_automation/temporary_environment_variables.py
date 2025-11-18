import os


class TemporaryEnvironmentVariables:
    """
    Context manager to temporarily set environment variables.
    Restores original values (or unsets them) on exit.
    """
    def __init__(self, environment_variables: dict[str, str]):
        self._environment_variables = environment_variables
        self._previous_values: dict[str, str | None] = {}

    def __enter__(self):
        for name, value in self._environment_variables.items():
            self._previous_values[name] = os.environ.get(name)
            os.environ[name] = value

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        for name, previous_value in self._previous_values.items():
            if previous_value is None:
                os.environ.pop(name, None)
            else:
                os.environ[name] = previous_value
