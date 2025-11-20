from backup_automation.backup_backend import BackupBackend
from backup_automation.playbook import PlaybookType
from backup_automation.restic import Restic


class BackupBackendFactory:
    # pylint: disable=too-few-public-methods
    # The class does not need more methods at the moment. This means that the class could
    # theoretically be replaced by a function, but implementing it like this helps with naming.
    """
    Class to create BackupBackend objects.
    """
    @staticmethod
    def create(playbook_type: PlaybookType, *args, **kwargs) -> BackupBackend:
        """
        Creates a BackupBackend object that belongs to the playbook_type.
        """
        match playbook_type:
            case PlaybookType.RESTIC:
                return Restic(*args, **kwargs)
            case _:
                raise ValueError(f"Unexpected playbook type: {playbook_type}")
