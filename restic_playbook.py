import json
import pathlib


class ResticPlaybookException(Exception):
    pass


class ResticPlaybook:
    REPOSITORIES_KEY = "repositories"
    STEPS_KEY = "steps"

    def __init__(self, path: pathlib.Path):
        if not path.is_file():
            raise FileNotFoundError(path)

        with path.read_text() as file:
            self.__data = json.load(file)

        if type(self.data) != dict:
            raise

        if ResticPlaybook.REPOSITORIES_KEY not in self.__data:
            raise EnvironmentError(f"Missing \"{self.REPOSITORIES_KEY} in playbook: \"{path}\"")

        if ResticPlaybook.STEPS_KEY not in self.__data:
            raise EnvironmentError(f"Missing {self.STEPS_KEY} in playbook: \"{path}\"")


