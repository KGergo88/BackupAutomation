import pathlib
from abc import ABC, abstractmethod

from backup_automation.playbook import Playbook

class PlaybookParser(ABC):
    @abstractmethod
    def parse(self, playbook_path: pathlib.Path) -> Playbook:
        pass