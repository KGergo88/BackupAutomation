from abc import ABC, abstractmethod

from backup_backend import BackupBackend


class PlaybookStep(ABC):
    def execute(self, backup_backend: BackupBackend):
        return
