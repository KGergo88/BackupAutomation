import pathlib
from dataclasses import dataclass


@dataclass
class ResticRepository:
    path: pathlib.Path
    password: str

    def __repr__(self):
        return f"ResticRepository({self.path})"
