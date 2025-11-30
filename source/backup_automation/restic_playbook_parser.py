import getpass
import os
import pathlib

from backup_automation.playbook import Playbook
from backup_automation.playbook_parser import PlaybookParser, PlaybookParserSettings
from backup_automation.restic_backend import ResticBackend
from backup_automation.restic_playbook import ResticPlaybook
from backup_automation.restic_playbook_exception import ResticPlaybookException
from backup_automation.restic_playbook_format import ResticPlaybookFormat
from backup_automation.restic_playbook_step_parser import ResticPlaybookStepParser
from backup_automation.restic_playbook_steps import ResticPlaybookStep
from backup_automation.restic_repository import ResticRepository, ResticRepositoryUri
from backup_automation.typehints import JsonDict, JsonList
from backup_automation.utility import read_json_file


class ResticPlaybookParser(PlaybookParser):
    # pylint: disable=too-few-public-methods
    # The class does not need more methods at the moment. This means that the class could
    # theoretically be replaced by a function, but implementing it like this helps with naming.
    """
    Class to represent a restic specific playbook parser.
    """
    def __init__(self,
                 backend: ResticBackend,
                 playbook_parser_settings: PlaybookParserSettings):
        self.__backend = backend
        self.__no_interaction = playbook_parser_settings.no_interaction
        self.__playbook_path: pathlib.Path | None = None
        self.__repositories: dict[str, ResticRepository] = {}
        self.__steps: list[ResticPlaybookStep] = []
        self.__format = ResticPlaybookFormat()

    def parse(self, playbook_path: pathlib.Path) -> Playbook:
        """
        Parses a playbook from the playbook_path into a ResticPlaybook object.
        """
        self.__playbook_path = playbook_path
        playbook_json = read_json_file(self.__playbook_path)

        self.__check_playbook_json(playbook_json)
        self.__parse_playbook_json(playbook_json)

        return ResticPlaybook(tuple(self.__steps))

    def __check_playbook_json(self, playbook_json: JsonDict) -> None:
        if not isinstance(playbook_json, dict):
            raise ResticPlaybookException("The playbook is not a valid JSON dictionary!")

        if self.__format.TYPE_KEY not in playbook_json:
            raise ResticPlaybookException(f"Missing \"{self.__format.TYPE_KEY}\" in playbook!")

        if playbook_json[self.__format.TYPE_KEY] != self.__format.TYPE_VALUE_RESTIC:
            raise ResticPlaybookException(f"Invalid playbook type: \"{playbook_json[self.__format.TYPE_KEY]}\". "
                                          f"Expected: \"{self.__format.TYPE_VALUE_RESTIC}\"")

        if self.__format.REPOSITORIES_KEY not in playbook_json:
            raise ResticPlaybookException(f"Missing \"{self.__format.REPOSITORIES_KEY} in playbook!")

        if not playbook_json[self.__format.REPOSITORIES_KEY]:
            raise ResticPlaybookException(
                f"No repositories defined in \"{self.__format.REPOSITORIES_KEY} in playbook!")

        for index, repository in enumerate(playbook_json[self.__format.REPOSITORIES_KEY]):
            self.__check_playbook_repository_json(repository, index)

        if self.__format.STEPS_KEY not in playbook_json:
            raise ResticPlaybookException(f"Missing {self.__format.STEPS_KEY} in playbook!")

        if not playbook_json[self.__format.STEPS_KEY]:
            raise ResticPlaybookException(f"No steps defined in \"{self.__format.STEPS_KEY} in playbook!")

        for index, step in enumerate(playbook_json[self.__format.STEPS_KEY]):
            self.__check_playbook_step_json(step, index)

    def __check_playbook_repository_json(self, playbook_repository_json: JsonDict, repository_index: int) -> None:
        def __check_for_key(repository_json: JsonDict, index: int, expected_keys: list[str]) -> None:
            for expected_key in expected_keys:
                if expected_key not in repository_json:
                    raise ResticPlaybookException(f"Missing \"{expected_key}\" for repository #{index + 1}")

        __check_for_key(playbook_repository_json, repository_index, [self.__format.REPOSITORIES_URI_KEY])

    def __check_playbook_step_json(self, playbook_step_json: JsonDict, step_index: int) -> None:
        def __check_for_key(step_json: JsonDict, index: int, expected_keys: list[str]) -> None:
            for expected_key in expected_keys:
                if expected_key not in step_json:
                    raise ResticPlaybookException(f"Missing \"{expected_key}\" for step #{index + 1}")

        __check_for_key(playbook_step_json, step_index, [self.__format.STEPS_COMMAND_KEY])

    def __parse_playbook_json(self, playbook_json: JsonDict) -> None:
        self.__parse_repositories_json(playbook_json[self.__format.REPOSITORIES_KEY])
        self.__parse_steps_json(playbook_json[self.__format.STEPS_KEY])

    def __parse_repositories_json(self, repositories_json: JsonList) -> None:
        for repository_json in repositories_json:
            raw_repository_uri = repository_json[self.__format.REPOSITORIES_URI_KEY]
            repository_uri = ResticRepositoryUri(raw_repository_uri)

            if repository_uri.is_local() and not pathlib.Path(repository_uri.path).is_dir():
                raise ResticPlaybookException(f"The repository path is not a valid directory: {repository_uri.path}")

            repository_id = repository_json.get(self.__format.REPOSITORIES_ID_KEY, repository_uri.repository_name)
            if repository_id in self.__repositories:
                raise ResticPlaybookException(f"The repository \"{repository_id}\" already exists!"
                                              f" This might be a duplicate repository."
                                              f" If not, please define a unique id for it.")

            password_value_from_playbook = repository_json.get(self.__format.REPOSITORIES_PASSWORD_KEY, None)
            repository_password = self.__resolve_repository_password(repository_id, password_value_from_playbook)

            repository = ResticRepository(repository_id, repository_uri, repository_password)
            self.__repositories[repository_id] = repository

    def __resolve_repository_password(self, repository_id: str, password_value: str | None) -> str:
        if not password_value:
            if self.__no_interaction:
                raise ResticPlaybookException(f"No password was provided for repository \"{repository_id}\"")
            return getpass.getpass(f"Enter password for restic repository \"{repository_id}\": ")

        if not password_value.lower().startswith(self.__format.REPOSITORIES_PASSWORD_VALUE_ENV_PREFIX):
            return password_value

        password_environment_variable = password_value[len(self.__format.REPOSITORIES_PASSWORD_VALUE_ENV_PREFIX):]
        if password_environment_variable not in os.environ:
            raise ResticPlaybookException(f"Environment variable \"{password_environment_variable}\""
                                          f" for repository \"{repository_id}\" is not defined!")
        return os.environ[password_environment_variable]

    def __parse_steps_json(self, steps_json: JsonList) -> None:
        step_parser = ResticPlaybookStepParser(self.__backend, self.__repository_lookup)
        for step_json in steps_json:
            step = step_parser.parse(step_json)
            self.__steps.append(step)

    def __repository_lookup(self, repository_id: str) -> ResticRepository:
        if repository_id in self.__repositories:
            return self.__repositories[repository_id]

        raise ResticPlaybookException(
            f"Unknown repository: \"{repository_id}\". The known repositories are: {list(self.__repositories.keys())}")
