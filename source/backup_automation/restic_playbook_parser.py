import getpass
import os
import pathlib

from typing import Any

import backup_automation.utility as utility

from backup_automation.playbook_parser import PlaybookParser
from backup_automation.restic_playbook import ResticPlaybook
from backup_automation.restic_playbook_exception import ResticPlaybookException
from backup_automation.restic_playbook_format import ResticPlaybookFormat
from backup_automation.restic_playbook_step_parser import ResticPlaybookStepParser
from backup_automation.restic_playbook_steps import ResticPlaybookStep
from backup_automation.restic_repository import ResticRepository, ResticRepositoryUri


class ResticPlaybookParser(PlaybookParser):
    def __init__(self, no_interaction: bool = False):
        self.__no_interaction = no_interaction
        self.__playbook_path: pathlib.Path|None = None
        self.__repositories: dict[str, ResticRepository] = {}
        self.__steps: list[ResticPlaybookStep] = []

    def parse(self, playbook_path: pathlib.Path):
        self.__playbook_path = playbook_path
        playbook_json = utility.read_json_file(self.__playbook_path)

        self.__check_playbook_json(playbook_json)
        self.__parse_playbook_json(playbook_json)

        return ResticPlaybook(tuple(self.__steps))

    def __check_playbook_json(self, playbook_json: Any):
        if not isinstance(playbook_json, dict):
            raise ResticPlaybookException("The playbook is not a valid JSON dictionary!")

        if ResticPlaybookFormat.TYPE_KEY not in playbook_json:
            raise ResticPlaybookException(f"Missing \"{ResticPlaybookFormat.TYPE_KEY}\" in playbook!")

        if playbook_json[ResticPlaybookFormat.TYPE_KEY] != ResticPlaybookFormat.TYPE_VALUE_RESTIC:
            raise ResticPlaybookException(f"Invalid playbook type: \"{playbook_json[ResticPlaybookFormat.TYPE_KEY]}\". "
                                          f"Expected: \"{ResticPlaybookFormat.TYPE_VALUE_RESTIC}\"")

        if ResticPlaybookFormat.REPOSITORIES_KEY not in playbook_json:
            raise ResticPlaybookException(f"Missing \"{ResticPlaybookFormat.REPOSITORIES_KEY} in playbook!")

        if not playbook_json[ResticPlaybookFormat.REPOSITORIES_KEY]:
            raise ResticPlaybookException(f"No repositories defined in \"{ResticPlaybookFormat.REPOSITORIES_KEY} in playbook!")

        for index, repository in enumerate(playbook_json[ResticPlaybookFormat.REPOSITORIES_KEY]):
            self.__check_playbook_repository_json(repository, index)

        if ResticPlaybookFormat.STEPS_KEY not in playbook_json:
            raise ResticPlaybookException(f"Missing {ResticPlaybookFormat.STEPS_KEY} in playbook!")

        if not playbook_json[ResticPlaybookFormat.STEPS_KEY]:
            raise ResticPlaybookException(f"No steps defined in \"{ResticPlaybookFormat.STEPS_KEY} in playbook!")

        for index, step in enumerate(playbook_json[ResticPlaybookFormat.STEPS_KEY]):
            self.__check_playbook_step_json(step, index)

    @staticmethod
    def __check_playbook_repository_json(playbook_repository_json: dict, repository_index: int):
        def __check_for_key(repository_json: dict, index: int, expected_keys: list[str]):
            for expected_key in expected_keys:
                if expected_key not in repository_json:
                    raise ResticPlaybookException(f"Missing \"{expected_key}\" for repository #{index + 1}")

        __check_for_key(playbook_repository_json, repository_index, [ResticPlaybookFormat.REPOSITORIES_URI_KEY])

    @staticmethod
    def __check_playbook_step_json(playbook_step_json: dict, step_index: int):
        def __check_for_key(step_json: dict, index: int, expected_keys: list[str]):
            for expected_key in expected_keys:
                if expected_key not in step_json:
                    raise ResticPlaybookException(f"Missing \"{expected_key}\" for step #{index + 1}")

        __check_for_key(playbook_step_json, step_index, [ResticPlaybookStep.STEPS_COMMAND_KEY])

    def __parse_playbook_json(self, playbook_json: dict):
        self.__parse_repositories_json(playbook_json[ResticPlaybookFormat.REPOSITORIES_KEY])
        self.__parse_steps_json(playbook_json[ResticPlaybookFormat.STEPS_KEY])

    def __parse_repositories_json(self, repositories_json: list):
        for repository_json in repositories_json:
            raw_repository_uri = repository_json[ResticPlaybookFormat.REPOSITORIES_URI_KEY]
            repository_uri = ResticRepositoryUri(raw_repository_uri)

            if repository_uri.is_local() and not pathlib.Path(repository_uri.path).is_dir():
                    raise ResticPlaybookException(f"The repository path is not a valid directory: {repository_uri.path}")

            repository_name = repository_json.get(ResticPlaybookFormat.REPOSITORIES_NAME_KEY, repository_uri.repository_name)
            if repository_name in self.__repositories:
                raise ResticPlaybookException(f"The repository \"{repository_name}\" already exists!"
                                              f" This might be a duplicate repository."
                                              f" If not, please define a unique name for it.")

            password_value_from_playbook = repository_json.get(ResticPlaybookFormat.REPOSITORIES_PASSWORD_KEY, None)
            repository_password = self.__resolve_repository_password(repository_name, password_value_from_playbook)

            repository = ResticRepository(repository_name, repository_uri, repository_password)
            self.__repositories[repository_name] = repository

    def __resolve_repository_password(self, repository_name, password_value_from_playbook: str|None) -> str:
        if not password_value_from_playbook:
            if self.__no_interaction:
                raise ResticPlaybookException(f"No password was provided for repository \"{repository_name}\"")
            return getpass.getpass(f"Enter password for restic repository \"{repository_name}\": ")

        if not password_value_from_playbook.lower().startswith(ResticPlaybookFormat.REPOSITORIES_PASSWORD_VALUE_ENV_PREFIX):
            return password_value_from_playbook

        password_environment_variable = password_value_from_playbook[len(ResticPlaybookFormat.REPOSITORIES_PASSWORD_VALUE_ENV_PREFIX):]
        if password_environment_variable not in os.environ:
            raise ResticPlaybookException(f"Environment variable \"{password_environment_variable}\""
                                          f" for repository \"{repository_name}\" is not defined!")
        return os.environ[password_environment_variable]

    def __parse_steps_json(self, steps_json: list):
        step_parser = ResticPlaybookStepParser(self.__repository_lookup)
        for index, step_json in enumerate(steps_json):
            step = step_parser.parse(step_json)
            self.__steps.append(step)

    def __repository_lookup(self, repository_name: str) -> ResticRepository:
        if repository_name in self.__repositories:
            return self.__repositories[repository_name]

        raise ResticPlaybookException(
            f"Unknown repository: \"{repository_name}\". The known repositories are: {list(self.__repositories.keys())}")
