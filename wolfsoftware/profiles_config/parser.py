r"""
ConfigHandler: A class to handle configuration files with profiles, key-value pairs, and comments.

This module provides functionalities to:
    - Load and preprocess configuration files.
    - Handle comments and whitespace in configuration files.
    - Retrieve profiles and key-value pairs from the configuration.
    - Display the current configuration.
    - Convert the configuration to a dictionary format.

Classes:
    ConfigHandler:
        A class to manage and manipulate configuration files.

Usage example:
    config_handler = ConfigHandler("config.ini")
    print("All Profiles:", config_handler.list_profiles())
    print("Profile 'profile name 1':", config_handler.get_profile("profile name 1"))
    print("Value of 'some key' in 'profile name 1':", config_handler.get_value("profile name 1", "some key"))
    print("Current Config:\n" + config_handler.display_config())
    print("Config as dict:\n", config_handler.get_config())
"""

from typing import Dict, List, Optional

import configparser
import os
import re


class ConfigHandler:
    """
    A class to handle configuration files with profiles, key-value pairs, and comments.

    Attributes:
    -----------
    filepath : str
        Path to the configuration file.

    Methods:
    --------
    preprocess_file():
        Reads and preprocesses the configuration file to remove comments and extra spaces.

    load_config():
        Loads and processes the configuration file, checking for formatting errors and duplicates.

    get_config():
        Returns the entire configuration as a dictionary.

    get_profile(profile_name):
        Returns a dictionary of key-value pairs for a given profile.

    get_value(profile_name, key_name):
        Returns the value for a specific key in a given profile.

    list_profiles():
        Returns a list of all profile names in the configuration file.

    display_config():
        Returns the current configuration as a formatted string.
    """

    def __init__(self, filepath: str, preserve_case: Optional[bool] = False) -> None:
        """
        Initialise the ConfigHandler with the path to the configuration file.

        Arguments:
            filepath (str): Path to the configuration file.
        """
        self.filepath: str = filepath
        self.preserve_case: Optional[bool] = preserve_case
        self.config: configparser.RawConfigParser = configparser.RawConfigParser()
        if preserve_case:
            self.config.optionxform = str  # type: ignore [assignment, method-assign]
        self.load_config()

    def preprocess_file(self) -> str:
        """
        Read and preprocesses the configuration file to remove comments and extra spaces.

        Returns:
            str: A string of the preprocessed configuration file.
        """
        with open(self.filepath, 'r', encoding='UTF-8') as file:
            lines: List[str] = file.readlines()

        processed_lines: List = []

        for line in lines:
            # Remove comments starting with ; and #
            line = re.sub(r';.*$', '', line)
            line = re.sub(r'#.*$', '', line)
            stripped_line: str = line.strip()
            if stripped_line:
                processed_lines.append(stripped_line)

        return "\n".join(processed_lines)

    def load_config(self) -> None:
        """
        Load and processes the configuration file, checking for formatting errors and duplicates.

        Raises:
            FileNotFoundError: If the configuration file does not exist.
            ValueError: If there are duplicate keys in a section or parsing errors.
        """
        if not os.path.exists(self.filepath):
            raise FileNotFoundError(f"Config file '{self.filepath}' does not exist.")

        try:
            config_string: str = self.preprocess_file()
            self.config.read_string(config_string)

            # Create a new configparser instance to store cleaned data
            cleaned_config = configparser.ConfigParser()
            if self.preserve_case:
                cleaned_config.optionxform = str  # type: ignore [assignment, method-assign]

            seen_sections = set()
            for section in self.config.sections():
                clean_section: str = section.strip().lower() if not self.preserve_case else section.strip()
                if clean_section in seen_sections:
                    raise ValueError(f"Duplicate profile name '{clean_section}' found.")
                seen_sections.add(clean_section)
                if clean_section not in cleaned_config:
                    cleaned_config.add_section(clean_section)
                keys_seen = set()
                for key, value in self.config.items(section):
                    clean_key: str = key.strip()
                    clean_value: str = value.strip()
                    if clean_key in keys_seen:
                        raise ValueError(f"Duplicate key '{clean_key}' found in section '{clean_section}'")
                    keys_seen.add(clean_key)
                    cleaned_config.set(clean_section, clean_key, clean_value)

            self.config = cleaned_config

        except configparser.Error as e:
            raise ValueError(f"Error parsing config file: {e}") from e

    def get_config(self) -> Dict:
        """
        Return the entire configuration as a dictionary.

        Return:
            Dict: A dictionary representation of the entire configuration.
        """
        config_dict: Dict = {}

        for section in self.config.sections():
            config_dict[section] = dict(self.config.items(section))
        return config_dict

    def get_profile(self, profile_name: str) -> Dict[str, str]:
        """
        Return a dictionary of key-value pairs for a given profile.

        Arguments:
            profile_name (str): The name of the profile.

        Returns:
            Dict[str, str]: A dictionary of key-value pairs for the given profile.

        Raises:
            KeyError: If the profile is not found in the configuration.
        """
        profile_name = profile_name.strip()

        if profile_name in self.config:
            return dict(self.config.items(profile_name))
        raise KeyError(f"Profile '{profile_name}' not found")

    def get_value(self, profile_name: str, key_name: str) -> str:
        """
        Return the value for a specific key in a given profile.

        Arguments:
            profile_name (str): The name of the profile.
            key_name (str): The name of the key.

        Returns:
            str: The value associated with the key in the given profile.

        Raises:
            KeyError: If the profile or key is not found in the configuration.
        """
        profile_name = profile_name.strip()
        key_name = key_name.strip()

        if profile_name in self.config:
            profile: configparser.SectionProxy = self.config[profile_name]
            if key_name in profile:
                return profile[key_name]
            raise KeyError(f"Key '{key_name}' not found in profile '{profile_name}'")
        raise KeyError(f"Profile '{profile_name}' not found")

    def list_profiles(self) -> List[str]:
        """
        Return a list of all profile names in the configuration file.

        Returns:
            List[str]: A list of all profile names.
        """
        return self.config.sections()

    def display_config(self) -> str:
        """
        Return the current configuration as a formatted string.

        Returns:
            str: The formatted string representation of the configuration.
        """
        config_str: List = []

        for section in self.config.sections():
            config_str.append(f"[{section}]")
            for key, value in self.config.items(section):
                config_str.append(f"{key} = {value}")
            config_str.append("")
        return "\n".join(config_str).strip()


# Example usage
if __name__ == "__main__":
    config_handler = ConfigHandler("config.ini")
    print("All Profiles:", config_handler.list_profiles())
    print("Profile 'profile name 1':", config_handler.get_profile("profile name 1"))
    print("Value of 'some key' in 'profile name 1':", config_handler.get_value("profile name 1", "some key"))
    print("Current Config:\n" + config_handler.display_config())
    print("Config as dict:\n", config_handler.get_config())
