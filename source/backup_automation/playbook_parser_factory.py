from backup_automation.playbook import PlaybookType

from backup_automation.playbook_parser import PlaybookParser
from backup_automation.restic_playbook_parser import ResticPlaybookParser


class PlaybookParserFactory:
    # pylint: disable=too-few-public-methods
    # The class does not need more methods at the moment. This means that the class could
    # theoretically be replaced by a function, but implementing it like this helps with naming.
    """
    Class to create PlaybookParser objects.
    """
    @staticmethod
    def create(playbook_type: PlaybookType, *args, **kwargs) -> PlaybookParser:
        """
        Creates a PlaybookParser object that belongs to the playbook_type.
        """
        match playbook_type:
            case PlaybookType.RESTIC:
                return ResticPlaybookParser(*args, **kwargs)
            case _:
                raise ValueError(f"Unexpected playbook type: \"{playbook_type}\"")
