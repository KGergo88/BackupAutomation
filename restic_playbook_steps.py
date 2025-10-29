import pathlib
from abc import ABC, abstractmethod
from typing import Callable

from restic import Restic
from restic_playbook_exception import ResticPlaybookException
from restic_repository import ResticRepository


class ResticPlaybookStep(ABC):
    STEPS_COMMAND_KEY = "command"
    @abstractmethod
    def execute(self, restic: Restic):
        return


class ResticPlaybookBackupStep(ResticPlaybookStep):
    REPOSITORY_KEY = "repository"
    SOURCE_PATH_KEY = "source_path"
    TAGS_KEY = "tags"

    def __init__(self, repository: ResticRepository, source_path: pathlib.Path, tags: tuple[str, ...]):
        super().__init__()
        self.__repository = repository
        self.__source_path = source_path
        self.__tags = tags

    def execute(self, restic: Restic):
        restic.backup(self.__repository, self.__source_path, self.__tags)
