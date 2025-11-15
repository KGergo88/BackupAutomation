import pathlib
from abc import ABC, abstractmethod

from restic import Restic
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


class ResticPlaybookCopyStep(ResticPlaybookStep):
    SOURCE_REPOSITORY_KEY = "source_repository"
    TARGET_REPOSITORY_KEY = "target_repository"

    def __init__(self, source_repository: ResticRepository, target_repository: ResticRepository):
        super().__init__()
        self.__source_repository = source_repository
        self.__target_repository = target_repository

    def execute(self, restic: Restic):
        restic.copy(self.__source_repository, self.__target_repository)
