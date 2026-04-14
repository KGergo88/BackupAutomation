from typing import Type, TypeVar

from backup_automation.typehints import JsonDict, JsonDictKey


T = TypeVar("T")


class JsonConfigException(Exception):
    """
    Exception to raise when restic playbook related errors happen.
    """


def __get_config_value(configuration: JsonDict, key: JsonDictKey, expected_type: Type[T]) -> T:
    value = configuration[key]
    if not isinstance(value, expected_type):
        raise JsonConfigException(f"Expected type {expected_type} for key {key} but got {type(value)} instead.")

    return value


def get_optional_config_value(configuration: JsonDict, key: JsonDictKey, expected_type: Type[T]) -> T | None:
    """
    Returns value from configuration if key is present, returns None otherwise.
    If the key is present but the value is not of the expected type, raises JsonConfigException.
    """
    if key not in configuration:
        return None

    return __get_config_value(configuration, key, expected_type)


def get_required_config_value(configuration: JsonDict, key: JsonDictKey, expected_type: Type[T]) -> T:
    """
    Returns value from configuration if key is present, raises JsonConfigException otherwise.
    If the key is present but the value is not of the expected type, raises JsonConfigException.
    """
    if key not in configuration:
        raise JsonConfigException(f"Missing required key in configuration: {key}")

    return __get_config_value(configuration, key, expected_type)
