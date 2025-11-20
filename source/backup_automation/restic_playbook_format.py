from dataclasses import dataclass

from backup_automation.playbook_format import PlaybookFormat


@dataclass
class ResticPlaybookFormat(PlaybookFormat):
    """
    Class to define the restic specific playbook format.
    It contains constants that can be used during parsing.
    """
    REPOSITORIES_KEY = "repositories"
    REPOSITORIES_NAME_KEY = "name"
    REPOSITORIES_URI_KEY = "uri"
    REPOSITORIES_PASSWORD_KEY = "password"
    REPOSITORIES_PASSWORD_VALUE_ENV_PREFIX = "env:"
    STEPS_KEY = "steps"
