import pathlib

from abc import ABC, abstractmethod
from enum import auto, Enum

import utility

from backup_backend import BackupBackend
from playbook_exception import PlaybookException
from playbook_format import PlaybookFormat
from playbook_steps import PlaybookStep


class PlaybookType(Enum):
    RESTIC = auto()


class Playbook(ABC):
    @abstractmethod
    def __init__(self, steps: tuple[PlaybookStep]):
        pass

    @abstractmethod
    def execute(self, backup_backend: BackupBackend):
        pass

    @staticmethod
    def determine_playbook_type(playbook_path: pathlib.Path) -> PlaybookType:
        playbook_json = utility.read_json_file(playbook_path)

        if PlaybookFormat.TYPE_KEY not in playbook_json:
            raise PlaybookException(f"Missing \"{PlaybookFormat.TYPE_KEY}\" in playbook!")

        playbook_type = playbook_json[PlaybookFormat.TYPE_KEY]
        match playbook_type:
            case PlaybookFormat.TYPE_VALUE_RESTIC:
                return PlaybookType.RESTIC
            case _:
                raise PlaybookException(f"Unexpected playbook type: \"{playbook_type}\"")
