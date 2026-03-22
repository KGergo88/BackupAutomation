import getpass


class PromptCredentialProvider:
    """
    Credential provider that asks the user for credentials if they are not yet stored.
    """
    # pylint: disable=too-few-public-methods
    # There are no more methods needed for this class at the moment.
    def __init__(self) -> None:
        self.__credentials: dict[str, str] = {}

    def get_credential(self, credential_name: str) -> str:
        """
        Returns the credential if exists, asks the user for the password via getpass.
        The credential entered will be stored and returned in the future without another prompt.
        """
        if credential_name in self.__credentials:
            return self.__credentials[credential_name]

        credential = getpass.getpass(f"Enter credentials for \"{credential_name}\": ")
        self.__credentials[credential_name] = credential

        return credential
