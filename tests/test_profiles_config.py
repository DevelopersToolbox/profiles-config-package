"""
This module contains a set of pytest tests for the profiles-config package,
specifically for the ConfigHandler class. These tests cover various functionalities
such as loading configuration files, retrieving profiles and key-value pairs,
and handling errors.

The tests use a temporary configuration file created during the test run
to validate the functionality of the ConfigHandler class.
"""

from typing import Dict, List

import pytest

from wolfsoftware.profiles_config import ConfigHandler


def test_init_config_handler(temp_config_file) -> None:
    """
    Test the initialization of the ConfigHandler class.

    Arguments:
        temp_config_file (Path): Path to the temporary configuration file.
    """
    handler = ConfigHandler(temp_config_file)
    assert str(handler.filepath) == str(temp_config_file)  # nosec: B101


def test_list_profiles(temp_config_file) -> None:
    """
    Test listing all profiles in the configuration file.

    Arguments:
        temp_config_file (Path): Path to the temporary configuration file.
    """
    handler = ConfigHandler(temp_config_file)
    profiles: List[str] = handler.list_profiles()

    assert profiles == ['profile1', 'profile2', 'profile3']  # nosec: B101


def test_get_profile(temp_config_file) -> None:
    """
    Test retrieving a profile from the configuration file.

    Arguments:
        temp_config_file (Path): Path to the temporary configuration file.
    """
    handler = ConfigHandler(temp_config_file)
    profile: Dict[str, str] = handler.get_profile('profile1')

    assert profile == {'key1': 'value1', 'key2': 'value2'}  # nosec: B101


def test_get_value(temp_config_file) -> None:
    """
    Test retrieving a value for a specific key in a profile.

    Arguments:
        temp_config_file (Path): Path to the temporary configuration file.
    """
    handler = ConfigHandler(temp_config_file)
    value: str = handler.get_value('profile1', 'key1')

    assert value == 'value1'  # nosec: B101


def test_get_profile_not_found(temp_config_file) -> None:
    """
    Test handling of non-existent profile retrieval.

    Arguments:
        temp_config_file (Path): Path to the temporary configuration file.
    """
    handler = ConfigHandler(temp_config_file)

    with pytest.raises(KeyError):
        handler.get_profile('nonexistent_profile')


def test_get_value_not_found(temp_config_file) -> None:
    """
    Test handling of non-existent key retrieval in a profile.

    Arguments:
        temp_config_file (Path): Path to the temporary configuration file.
    """
    handler = ConfigHandler(temp_config_file)

    with pytest.raises(KeyError):
        handler.get_value('profile1', 'nonexistent_key')


def test_get_value_profile_not_found(temp_config_file) -> None:
    """
    Test handling of key retrieval in a non-existent profile.

    Arguments:
        temp_config_file (Path): Path to the temporary configuration file.
    """
    handler = ConfigHandler(temp_config_file)

    with pytest.raises(KeyError):
        handler.get_value('nonexistent_profile', 'key1')


def test_get_config(temp_config_file) -> None:
    """
    Test retrieving the entire configuration as a dictionary.

    Arguments:
        temp_config_file (Path): Path to the temporary configuration file.
    """
    handler = ConfigHandler(temp_config_file)
    config_dict: Dict = handler.get_config()
    expected_dict: Dict[str, Dict[str, str]] = {
        'profile1': {'key1': 'value1', 'key2': 'value2'},
        'profile2': {'keya': 'valueA', 'keyb': 'valueB'},
        'profile3': {'keyx': 'valueX', 'keyy': 'valueY'}
    }

    assert config_dict == expected_dict  # nosec: B101


def test_get_config_preserve_case(temp_config_file) -> None:
    """
    Test retrieving the entire configuration as a dictionary with case sensitivity preserved.

    Arguments:
        temp_config_file (Path): Path to the temporary configuration file.
    """
    handler = ConfigHandler(temp_config_file, preserve_case=True)
    config_dict: Dict = handler.get_config()
    expected_dict: Dict[str, Dict[str, str]] = {
        'profile1': {'key1': 'value1', 'key2': 'value2'},
        'profile2': {'keyA': 'valueA', 'keyB': 'valueB'},
        'profile3': {'keyX': 'valueX', 'keyY': 'valueY'}
    }
    assert config_dict == expected_dict  # nosec: B101


def test_display_config(temp_config_file) -> None:
    """
    Test displaying the current configuration as a formatted string.

    Arguments:
        temp_config_file (Path): Path to the temporary configuration file.
    """
    handler = ConfigHandler(temp_config_file)
    config_str: str = handler.display_config()
    expected_str: str = """
[profile1]
key1 = value1
key2 = value2

[profile2]
keya = valueA
keyb = valueB

[profile3]
keyx = valueX
keyy = valueY
    """.strip()

    assert config_str == expected_str  # nosec: B101


def test_display_config_preserve_case(temp_config_file) -> None:
    """
    Test displaying the current configuration as a formatted string.

    Arguments:
        temp_config_file (Path): Path to the temporary configuration file.
    """
    handler = ConfigHandler(temp_config_file, preserve_case=True)
    config_str: str = handler.display_config()
    expected_str: str = """
[profile1]
key1 = value1
key2 = value2

[profile2]
keyA = valueA
keyB = valueB

[profile3]
keyX = valueX
keyY = valueY
    """.strip()

    assert config_str == expected_str  # nosec: B101


def test_preprocess_file(temp_config_file) -> None:
    """
    Test the preprocessing of the configuration file to remove comments and extra spaces.

    Arguments:
        temp_config_file (Path): Path to the temporary configuration file.
    """
    handler = ConfigHandler(temp_config_file)
    preprocessed_content: str = handler.preprocess_file()
    expected_content: str = """
[profile1]
key1 = value1
key2 = value2
[profile2]
keyA = valueA
keyB = valueB
[profile3]
keyX = valueX
keyY = valueY
    """.strip()

    assert preprocessed_content.strip() == expected_content  # nosec: B101
