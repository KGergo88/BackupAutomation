from dataclasses import dataclass


@dataclass(frozen=True)
class PlaybookFormat:
    """
    Class to define the playbook format.
    It contains constants that can be used during parsing.
    """
    TYPE_KEY = "type"
    TYPE_VALUE_RESTIC = "restic"
