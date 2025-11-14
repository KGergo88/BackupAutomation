import pathlib


class ResticRepository:
    def __init__(self, repository_name: str, repository_path: pathlib.Path, repository_password: str):
        self.__name = repository_name
        self.__path = repository_path
        self.__password = repository_password

    def __repr__(self):
        return f"ResticRepository({self.path})"

    @property
    def name(self) -> str:
        return self.__name

    @property
    def path(self) -> pathlib.Path:
        return self.__path

    @property
    def password(self) -> str:
        return self.__password
