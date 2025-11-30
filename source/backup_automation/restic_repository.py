import pathlib

from enum import auto, Enum


class ResticRepositoryUriScheme(Enum):
    """
    Lists the supported repository URI schemes.
    """
    UNKNOWN = auto()
    LOCAL = auto()      # The repository URI points to a local directory
    SFTP = auto()       # The repository URI points to a remote directory that shall be accessed via SFTP


class ResticRepositoryUri:
    """
    Class to represent the URI of a restic repository.
    """
    URI_SCHEME_PREFIX_LOCAL = "local:"
    URI_SCHEME_PREFIX_SFTP = "sftp:"

    def __init__(self, raw_uri: str):
        raw_uri = raw_uri.strip()
        match raw_uri:
            case s if s.startswith(self.URI_SCHEME_PREFIX_LOCAL):
                self.__uri = raw_uri
                self.__scheme = ResticRepositoryUriScheme.LOCAL
                self.__path = self.__uri.removeprefix(self.URI_SCHEME_PREFIX_LOCAL)
            case s if s.startswith(self.URI_SCHEME_PREFIX_SFTP):
                self.__uri = raw_uri
                self.__scheme = ResticRepositoryUriScheme.SFTP
                self.__path = self.__uri.removeprefix(self.URI_SCHEME_PREFIX_SFTP)
            case _:
                self.__uri = ResticRepositoryUri.URI_SCHEME_PREFIX_LOCAL + raw_uri
                self.__scheme = ResticRepositoryUriScheme.LOCAL
                self.__path = raw_uri

    def __repr__(self) -> str:
        return f"ResticRepositoryUri({str(self.__uri)})"

    def __str__(self) -> str:
        return self.uri

    def is_sftp(self) -> bool:
        """
        Returns whether the repository is a SFTP repository.
        """
        return self.__scheme == ResticRepositoryUriScheme.SFTP

    def is_local(self) -> bool:
        """
        Returns whether the repository is a local repository.
        """
        return self.__scheme == ResticRepositoryUriScheme.LOCAL

    @property
    def uri(self) -> str:
        """
        The URI of the repository.
        """
        return self.__uri

    @property
    def path(self) -> str:
        """
        The path of the repository.
        """
        return self.__path

    @property
    def repository_name(self) -> str:
        """
        The name of the repository.
        """
        return pathlib.Path(self.__path).name


class ResticRepository:
    """
    Class to represent a restic repository.
    """
    def __init__(self, repository_id: str, repository_uri: ResticRepositoryUri, repository_password: str):
        self.__id = repository_id
        self.__uri = repository_uri
        self.__password = repository_password

    def __repr__(self) -> str:
        return f"ResticRepository({self.__uri})"

    @property
    def id(self) -> str:
        """
        The id of the repository.
        """
        return self.__id

    @property
    def uri(self) -> ResticRepositoryUri:
        """
        The URI of the repository.
        """
        return self.__uri

    @property
    def password(self) -> str:
        """
        The password of the repository.
        """
        return self.__password
