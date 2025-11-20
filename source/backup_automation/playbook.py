import pathlib

from abc import ABC, abstractmethod
from enum import auto, Enum

from backup_automation.backup_backend import BackupBackend
from backup_automation.playbook_exception import PlaybookException
from backup_automation.playbook_format import PlaybookFormat
from backup_automation.playbook_steps import PlaybookStep
from backup_automation.utility import read_json_file


class PlaybookType(Enum):
    """
    Lists the supported playbook types.
    """
    RESTIC = auto()


class Playbook[BackupBackendT: BackupBackend](ABC):
    """
    Abstract class to represent a playbook.
    Playbooks orchestrate the backup operations.
    They contain steps and that execute an action on the BackupBackend.
    """
    @abstractmethod
    def __init__(self, steps: tuple[PlaybookStep]):
        pass

    @abstractmethod
    def execute(self, backup_backend: BackupBackendT):
        """
        Execute the playbook with the given backup backend.
        """

    @staticmethod
    def determine_playbook_type(playbook_path: pathlib.Path) -> PlaybookType:
        """
        Reads a playbook and determines it´s type.
        """
        playbook_json = read_json_file(playbook_path)

        if PlaybookFormat.TYPE_KEY not in playbook_json:
            raise PlaybookException(f"Missing \"{PlaybookFormat.TYPE_KEY}\" in playbook!")

        playbook_type = playbook_json[PlaybookFormat.TYPE_KEY]
        match playbook_type:
            case PlaybookFormat.TYPE_VALUE_RESTIC:
                return PlaybookType.RESTIC
            case _:
                raise PlaybookException(f"Unexpected playbook type: \"{playbook_type}\"")
