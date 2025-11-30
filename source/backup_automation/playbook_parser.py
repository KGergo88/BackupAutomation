import pathlib

from abc import ABC, abstractmethod
from dataclasses import dataclass

from backup_automation.playbook import Playbook


@dataclass(frozen=True)
class PlaybookParserSettings:
    """
    Contains the settings available for playbook parsers.
    """
    no_interaction: bool


class PlaybookParser(ABC):
    # pylint: disable=too-few-public-methods
    # The class does not need more methods at the moment. This means that the class could
    # theoretically be replaced by a function, but implementing it like this helps with naming.
    """
    Abstract class to represent a playbook parser.
    Playbook parsers read playbook files from the disk, check them and parse them into an object.
    """
    @abstractmethod
    def parse(self, playbook_path: pathlib.Path) -> Playbook:
        """
        Parses a playbook from the playbook_path into a Playbook object.
        """
