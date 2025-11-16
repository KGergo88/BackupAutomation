from backup_backend import BackupBackend
from playbook import PlaybookType
from restic import Restic


class BackupBackendFactory:
    @staticmethod
    def create(playbook_type: PlaybookType, *args, **kwargs) -> BackupBackend:
        match playbook_type:
         case PlaybookType.RESTIC:
             return Restic(*args, **kwargs)
         case _:
             raise ValueError(f"Unexpected playbook type: {playbook_type}")
