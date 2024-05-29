<!-- markdownlint-disable -->
<p align="center">
    <a href="https://github.com/DevelopersToolbox/">
        <img src="https://cdn.wolfsoftware.com/assets/images/github/organisations/developerstoolbox/black-and-white-circle-256.png" alt="DevelopersToolbox logo" />
    </a>
    <br />
    <a href="https://github.com/DevelopersToolbox/profiles-config-package/actions/workflows/cicd.yml">
        <img src="https://img.shields.io/github/actions/workflow/status/DevelopersToolbox/profiles-config-package/cicd.yml?branch=master&label=build%20status&style=for-the-badge" alt="Github Build Status" />
    </a>
    <a href="https://github.com/DevelopersToolbox/profiles-config-package/blob/master/LICENSE.md">
        <img src="https://img.shields.io/github/license/DevelopersToolbox/profiles-config-package?color=blue&label=License&style=for-the-badge" alt="License">
    </a>
    <a href="https://github.com/DevelopersToolbox/profiles-config-package">
        <img src="https://img.shields.io/github/created-at/DevelopersToolbox/profiles-config-package?color=blue&label=Created&style=for-the-badge" alt="Created">
    </a>
    <br />
    <a href="https://github.com/DevelopersToolbox/profiles-config-package/releases/latest">
        <img src="https://img.shields.io/github/v/release/DevelopersToolbox/profiles-config-package?color=blue&label=Latest%20Release&style=for-the-badge" alt="Release">
    </a>
    <a href="https://github.com/DevelopersToolbox/profiles-config-package/releases/latest">
        <img src="https://img.shields.io/github/release-date/DevelopersToolbox/profiles-config-package?color=blue&label=Released&style=for-the-badge" alt="Released">
    </a>
    <a href="https://github.com/DevelopersToolbox/profiles-config-package/releases/latest">
        <img src="https://img.shields.io/github/commits-since/DevelopersToolbox/profiles-config-package/latest.svg?color=blue&style=for-the-badge" alt="Commits since release">
    </a>
    <br />
    <a href="https://github.com/DevelopersToolbox/profiles-config-package/blob/master/.github/CODE_OF_CONDUCT.md">
        <img src="https://img.shields.io/badge/Code%20of%20Conduct-blue?style=for-the-badge" />
    </a>
    <a href="https://github.com/DevelopersToolbox/profiles-config-package/blob/master/.github/CONTRIBUTING.md">
        <img src="https://img.shields.io/badge/Contributing-blue?style=for-the-badge" />
    </a>
    <a href="https://github.com/DevelopersToolbox/profiles-config-package/blob/master/.github/SECURITY.md">
        <img src="https://img.shields.io/badge/Report%20Security%20Concern-blue?style=for-the-badge" />
    </a>
    <a href="https://github.com/DevelopersToolbox/profiles-config-package/issues">
        <img src="https://img.shields.io/badge/Get%20Support-blue?style=for-the-badge" />
    </a>
</p>

## Overview

Profiles Config is a Python package designed to handle configuration files with profiles, key-value pairs, and comments. This package
provides functionalities to load and preprocess configuration files, manage comments and whitespace, retrieve profiles and key-value pairs,
display the current configuration, and convert the configuration to a dictionary format.

Like many of our packages this was developed as part of another project, but we felt others might be able to make use of it.

## Features

- **Load and preprocess configuration files**: Reads the configuration file, removes comments and extra spaces.
- **Handle comments and whitespace**: Processes configuration files to ensure clean and accurate data.
- **Retrieve profiles and key-value pairs**: Access specific profiles and their associated key-value pairs.
- **Display the current configuration**: Provides a formatted string representation of the current configuration.
- **Convert the configuration to a dictionary format**: Allows for easy manipulation and access of the configuration data.

## Installation

To install the `profiles-config` package, use pip:

```bash
pip install wolfsoftware.profiles-config
```

## Usage

Here is an example of how to use the `ConfigHandler` class from the `profiles-config` package:

```python
from wolfsoftware.profiles_config import ConfigHandler

# Example usage
if __name__ == "__main__":
    config_handler = ConfigHandler("config.ini")
    print("All Profiles:", config_handler.list_profiles())
    print("Profile 'profile name 1':", config_handler.get_profile("profile name 1"))
    print("Value of 'some key' in 'profile name 1':", config_handler.get_value("profile name 1", "some key"))
    print("Current Config:\n" + config_handler.display_config())
    print("Config as dict:\n", config_handler.get_config())
```

## Example Config File

```
[  profile name 1  ]
# This is a comment for some key
some key = some value

# This is a random comment
# This is a random comment also
[profile name 2]  # Comment 1
keys1 = value
keys2 = another value  # comment 2

[profile name 3]  # Comment 1
keys1 = value
keys2 = another value  # comment 2

# more comments
# comments to end the file
# more comments
```

> Note the spaces prefixing and suffixing the 'profile name 1' entry. These are stripped as part of the load and cleanse phase.

Once the config file has been loaded, parsed and cleansed the internal representation is a Python dictionary, which would look like this:

```
{
    'profile name 1': {
        'some key': 'some value'
    },
    'profile name 2': {
        'keys1': 'value',
        'keys2': 'another value'
    }, 
    'profile name 3': {
        'keys1': 'value', 
        'keys2': 'another value'
    }
}
```

If you use display_config() then the output would look like this:

```
[profile name 1]
some key = some value

[profile name 2]
keys1 = value
keys2 = another value

[profile name 3]
keys1 = value
keys2 = another value
```

## Class Documentation

### ConfigHandler

A class to manage and manipulate configuration files.

#### Attributes

- **filepath**: str - Path to the configuration file.

#### Methods

- **`__init__(self, filepath: str, preserve_case: Optional[bool] = False)`**: Initializes the ConfigHandler with the path to the configuration file.
- **`preprocess_file(self) -> str`**: Reads and preprocesses the configuration file to remove comments and extra spaces.
- **`load_config(self) -> None`**: Loads and processes the configuration file, checking for formatting errors and duplicates.
- **`get_config(self) -> Dict`**: Returns the entire configuration as a dictionary.
- **`get_profile(self, profile_name: str) -> Dict[str, str]`**: Returns a dictionary of key-value pairs for a given profile.
- **`get_value(self, profile_name: str, key_name: str) -> str`**: Returns the value for a specific key in a given profile.
- **`list_profiles(self) -> List[str]`**: Returns a list of all profile names in the configuration file.
- **`display_config(self) -> str`**: Returns the current configuration as a formatted string.

> If you set preserve_case=True it will preserve the case for both sections and keys, otherwise is will lowercase BOTH.

### Method Details

- **`__init__(self, filepath: str, preserve_case: Optional[bool] = False)`**:
  - Initializes the ConfigHandler with the path to the configuration file.
  - **Arguments**:
    - `filepath` (str): Path to the configuration file.
    - `preserve_case` Optional[bool]: Override the default and preserve case sensitivity for names.

- **`preprocess_file(self) -> str`**:
  - Reads and preprocesses the configuration file to remove comments and extra spaces.
  - **Returns**:
    - str: A string of the preprocessed configuration file.

- **`load_config(self) -> None`**:
  - Loads and processes the configuration file, checking for formatting errors and duplicates.
  - **Raises**:
    - `FileNotFoundError`: If the configuration file does not exist.
    - `ValueError`: If there are duplicate keys in a section or parsing errors.

- **`get_config(self) -> Dict`**:
  - Returns the entire configuration as a dictionary.
  - **Returns**:
    - Dict: A dictionary representation of the entire configuration.

- **`get_profile(self, profile_name: str) -> Dict[str, str]`**:
  - Returns a dictionary of key-value pairs for a given profile.
  - **Arguments**:
    - `profile_name` (str): The name of the profile.
  - **Returns**:
    - Dict[str, str]: A dictionary of key-value pairs for the given profile.
  - **Raises**:
    - `KeyError`: If the profile is not found in the configuration.

- **`get_value(self, profile_name: str, key_name: str) -> str`**:
  - Returns the value for a specific key in a given profile.
  - **Arguments**:
    - `profile_name` (str): The name of the profile.
    - `key_name` (str): The name of the key.
  - **Returns**:
    - str: The value associated with the key in the given profile.
  - **Raises**:
    - `KeyError`: If the profile or key is not found in the configuration.

- **`list_profiles(self) -> List[str]`**:
  - Returns a list of all profile names in the configuration file.
  - **Returns**:
    - List[str]: A list of all profile names.

- **`display_config(self) -> str`**:
  - Returns the current configuration as a formatted string.
  - **Returns**:
    - str: The formatted string representation of the configuration.

<br />
<p align="right"><a href="https://wolfsoftware.com/"><img src="https://img.shields.io/badge/Created%20by%20Wolf%20on%20behalf%20of%20Wolf%20Software-blue?style=for-the-badge" /></a></p>
