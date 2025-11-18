from playbook import PlaybookType

from playbook_parser import PlaybookParser
from restic_playbook_parser import ResticPlaybookParser


class PlaybookParserFactory:
    @staticmethod
    def create(playbook_type: PlaybookType, *args, **kwargs) -> PlaybookParser:
        match playbook_type:
            case PlaybookType.RESTIC:
                return ResticPlaybookParser(*args, **kwargs)
            case _:
                raise ValueError(f"Unexpected playbook type: \"{playbook_type}\"")
