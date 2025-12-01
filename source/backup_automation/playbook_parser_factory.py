import pathlib

from enum import Enum, auto

from backup_automation.backend import BackendSettings
from backup_automation.playbook_exception import PlaybookException
from backup_automation.playbook_format import PlaybookFormat
from backup_automation.playbook_parser import PlaybookParser, PlaybookParserSettings
from backup_automation.restic.restic_backend import ResticBackend
from backup_automation.restic.restic_playbook_parser import ResticPlaybookParser
from backup_automation.utility import read_json_file


class PlaybookType(Enum):
    """
    Lists the supported playbook types.
    """
    RESTIC = auto()


class PlaybookParserFactory:
    # pylint: disable=too-few-public-methods
    # The class does not need more methods at the moment. This means that the class could
    # theoretically be replaced by a function, but implementing it like this helps with naming.
    """
    Class to create PlaybookParser objects.
    """
    @staticmethod
    def create_from_file(playbook_path: pathlib.Path,
                         playbook_parser_settings: PlaybookParserSettings,
                         backend_settings: BackendSettings) -> PlaybookParser:
        """
        Creates a PlaybookParser object that belongs to the playbook.
        The playbook type is determined based on the the playbook file.
        """
        playbook_type = PlaybookParserFactory.determine_playbook_type(playbook_path)
        return PlaybookParserFactory.create(playbook_type, playbook_parser_settings, backend_settings)

    @staticmethod
    def create(playbook_type: PlaybookType,
               playbook_parser_settings: PlaybookParserSettings,
               backend_settings: BackendSettings) -> PlaybookParser:
        """
        Creates a PlaybookParser object that belongs to the playbook_type.
        """
        match playbook_type:
            case PlaybookType.RESTIC:
                backend = ResticBackend(backend_settings)
                return ResticPlaybookParser(backend, playbook_parser_settings)
            case _:
                raise ValueError(f"Unexpected playbook type: \"{playbook_type}\"")

    @staticmethod
    def determine_playbook_type(playbook_path: pathlib.Path) -> PlaybookType:
        """
        Reads a playbook and determines it´s type.
        """
        playbook_json = read_json_file(playbook_path)

        if PlaybookFormat.TYPE_KEY not in playbook_json:
            raise PlaybookException(f"Missing \"{PlaybookFormat.TYPE_KEY}\" in playbook!")

        playbook_type = playbook_json[PlaybookFormat.TYPE_KEY]
        match playbook_type:
            case PlaybookFormat.TYPE_VALUE_RESTIC:
                return PlaybookType.RESTIC
            case _:
                raise PlaybookException(f"Unexpected playbook type: \"{playbook_type}\"")
