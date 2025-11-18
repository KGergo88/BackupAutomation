import pathlib

from enum import auto, Enum

from restic_playbook_format import ResticPlaybookFormat


class ResticRepositoryUriScheme(Enum):
    UNKNOWN = auto()
    LOCAL = auto()
    SFTP = auto()


class ResticRepositoryUri:
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

    def __repr__(self):
        return f"ResticRepositoryUri({str(self.__uri)})"

    def __str__(self):
        return self.uri

    def is_sftp(self) -> bool:
        return self.__scheme == ResticRepositoryUriScheme.SFTP

    def is_local(self) -> bool:
        return self.__scheme == ResticRepositoryUriScheme.LOCAL

    @property
    def uri(self) -> str:
        return self.__uri

    @property
    def path(self) -> str:
        return self.__path

    @property
    def repository_name(self) -> str:
        return pathlib.Path(self.__path).name


class ResticRepository:
    def __init__(self, repository_name: str, repository_uri: ResticRepositoryUri, repository_password: str):
        self.__name = repository_name
        self.__uri = repository_uri
        self.__password = repository_password

    def __repr__(self):
        return f"ResticRepository({self.__uri})"

    @property
    def name(self) -> str:
        return self.__name

    @property
    def uri(self) -> ResticRepositoryUri:
        return self.__uri

    @property
    def password(self) -> str:
        return self.__password
