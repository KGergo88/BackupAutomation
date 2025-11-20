from backup_automation.playbook import PlaybookType

from backup_automation.playbook_parser import PlaybookParser
from backup_automation.restic_playbook_parser import ResticPlaybookParser


class PlaybookParserFactory:
    @staticmethod
    def create(playbook_type: PlaybookType, *args, **kwargs) -> PlaybookParser:
        match playbook_type:
            case PlaybookType.RESTIC:
                return ResticPlaybookParser(*args, **kwargs)
            case _:
                raise ValueError(f"Unexpected playbook type: \"{playbook_type}\"")
