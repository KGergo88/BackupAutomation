from dataclasses import dataclass

from backup_automation.playbook_format import PlaybookFormat


@dataclass(frozen=True)
class ResticPlaybookFormat(PlaybookFormat):
    """
    Class to define the restic specific playbook format.
    It contains constants that can be used during parsing.
    """
    REPOSITORIES_KEY = "repositories"
    REPOSITORIES_ID_KEY = "id"
    REPOSITORIES_URI_KEY = "uri"
    REPOSITORIES_PASSWORD_KEY = "password"
    REPOSITORIES_PASSWORD_VALUE_ENV_PREFIX = "env:"
    REPOSITORIES_PASSWORD_VALUE_PROMPT_PREFIX = "prompt:"
    STEPS_KEY = "steps"
    STEPS_COMMAND_KEY = "command"
    STEPS_COMMAND_VALUE_BACKUP = "backup"
    STEPS_COMMAND_VALUE_COPY = "copy"
    STEPS_BACKUP_REPOSITORY_KEY = "repository"
    STEPS_BACKUP_SOURCE_PATH_KEY = "source_path"
    STEPS_BACKUP_TAGS_KEY = "tags"
    STEPS_COPY_SOURCE_REPOSITORY_KEY = "source_repository"
    STEPS_COPY_TARGET_REPOSITORY_KEY = "target_repository"
