import contextlib
import pathlib
from abc import ABC

from backup_automation.playbook_steps import PlaybookStep
from backup_automation.restic.restic_backend import ResticBackend
from backup_automation.restic.restic_repository import ResticRepository


class ResticPlaybookStep(PlaybookStep, ABC):
    # pylint: disable=too-few-public-methods
    # The class does not need more methods at the moment. This means that the class could
    # theoretically be replaced by a function, but implementing it like this helps with naming.
    """
    Abstract class to represent a restic specific playbook step.
    """


class ResticPlaybookBackupStep(ResticPlaybookStep):
    # pylint: disable=too-few-public-methods
    # The class does not need more methods at the moment. This means that the class could
    # theoretically be replaced by a function, but implementing it like this helps with naming.
    """
    Class to represent the restic specific backup playbook step.
    """
    # pylint: disable=too-many-arguments
    # pylint: disable=too-many-positional-arguments
    # This class needs to represent a backup step with all its fields.
    def __init__(self,
                 backend: ResticBackend,
                 repository: ResticRepository,
                 source_path: pathlib.Path,
                 tags: tuple[str, ...],
                 working_dir: pathlib.Path | None):
        super().__init__()
        self.__backend = backend
        self.__repository = repository
        self.__source_path = source_path
        self.__tags = tags
        self.__working_dir = working_dir

    def execute(self) -> None:
        working_dir_context = contextlib.chdir(self.__working_dir) if self.__working_dir else contextlib.nullcontext()
        with working_dir_context:
            self.__backend.backup(self.__repository, self.__source_path, self.__tags)


class ResticPlaybookCopyStep(ResticPlaybookStep):
    # pylint: disable=too-few-public-methods
    # The class does not need more methods at the moment. This means that the class could
    # theoretically be replaced by a function, but implementing it like this helps with naming.
    """
    Class to represent the restic specific copy playbook step.
    """
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
