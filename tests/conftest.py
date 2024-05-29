"""
This module provides pytest fixtures for mocking HTTP requests in tests for the Profiles Config package.

Dependencies:
    - pytest: Used for writing and running tests.

Functions:
    - temp_config_file: Creates a temporary config file for testing.
"""

from typing import Any

import pytest

# Test configuration content
config_content = """
[profile1]
key1 = value1
key2 = value2

[profile2]
keyA = valueA
keyB = valueB

; This is a comment
# This is another comment

[profile3]
keyX = valueX
keyY = valueY
"""


@pytest.fixture
def temp_config_file(tmp_path) -> Any:
    """
    Create a temporary config file for testing.

    Arguments:
        tmp_path (Path): Path provided by pytest to create temporary files.

    Returns:
        Path: Path to the temporary configuration file.
    """
    config_file: Any = tmp_path / "config.ini"
    config_file.write_text(config_content)
    return config_file
