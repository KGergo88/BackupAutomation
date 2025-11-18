from backup_automation.backup_backend import BackupBackend
from backup_automation.playbook import PlaybookType
from backup_automation.restic import Restic


class BackupBackendFactory:
    @staticmethod
    def create(playbook_type: PlaybookType, *args, **kwargs) -> BackupBackend:
        match playbook_type:
         case PlaybookType.RESTIC:
             return Restic(*args, **kwargs)
         case _:
             raise ValueError(f"Unexpected playbook type: {playbook_type}")
