import pathlib
from abc import ABC

from backup_automation.playbook_steps import PlaybookStep
from backup_automation.restic_backend import ResticBackend
from backup_automation.restic_repository import ResticRepository


class ResticPlaybookStep(PlaybookStep, ABC):
    # pylint: disable=too-few-public-methods
    # The class does not need more methods at the moment. This means that the class could
    # theoretically be replaced by a function, but implementing it like this helps with naming.
    """
    Abstract class to represent a restic specific playbook step.
    """
    STEPS_COMMAND_KEY = "command"


class ResticPlaybookBackupStep(ResticPlaybookStep):
    # pylint: disable=too-few-public-methods
    # The class does not need more methods at the moment. This means that the class could
    # theoretically be replaced by a function, but implementing it like this helps with naming.
    """
    Class to represent the restic specific backup playbook step.
    """
    REPOSITORY_KEY = "repository"
    SOURCE_PATH_KEY = "source_path"
    TAGS_KEY = "tags"

    def __init__(self,
                 backend: ResticBackend,
                 repository: ResticRepository,
                 source_path: pathlib.Path,
                 tags: tuple[str, ...]):
        super().__init__()
        self.__backend = backend
        self.__repository = repository
        self.__source_path = source_path
        self.__tags = tags

    def execute(self) -> None:
        self.__backend.backup(self.__repository, self.__source_path, self.__tags)


class ResticPlaybookCopyStep(ResticPlaybookStep):
    # pylint: disable=too-few-public-methods
    # The class does not need more methods at the moment. This means that the class could
    # theoretically be replaced by a function, but implementing it like this helps with naming.
    """
    Class to represent the restic specific copy playbook step.
    """
    SOURCE_REPOSITORY_KEY = "source_repository"
    TARGET_REPOSITORY_KEY = "target_repository"

    def __init__(self,
                 backend: ResticBackend,
                 source_repository: ResticRepository,
                 target_repository: ResticRepository):
        super().__init__()
        self.__backend = backend
        self.__source_repository = source_repository
        self.__target_repository = target_repository

    def execute(self) -> None:
        self.__backend.copy(self.__source_repository, self.__target_repository)
