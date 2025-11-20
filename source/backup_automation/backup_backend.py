from abc import ABC

class BackupBackend(ABC):
    # pylint: disable=too-few-public-methods
    # It is not known at the moment what could be the shared content between backend classes.
    # This abstraction is neded in order to be able to generalize the backend automation.
    """
    The backup backend classes shall inherit from this class.
    These are the representation of the different backup software supported by this project.
    """
