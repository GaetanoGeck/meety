import os
import shutil

import appdirs
import yaml

from meety import (
    connect,
    io,
    meetings,
    resources,
)
from meety.cli import styles as cli_styles
from meety.gui import styles as gui_styles
from meety.logging import log


class Config:
    """Configuration management for the application.

    The configuration may depend on multiple YAML files, loaded in
    a specific order. First, the internal "default" configuration,
    provided by the installed app, is loaded. Then, the user
    configuration is loaded, if found in the directory.

    Both these configuration files can activate and deactivate
    additional (internal) configurations: language-specific aspects
    and colour schemes for example.

    Later settings generally overwrite previous settings (some
    exceptions, e.g. for handlers, are described in the
    documentation).
    """

    PROGRAM = ""

    @classmethod
    def _ensure_user_config(cls, source, target):
        """Copy template to user config directory if it does not
        contain a configuration file.
        """
        if not os.path.isfile(target):
            log.info(
                f"Copying user configuration template to {target}."
            )
            shutil.copy(source, target)

    def __init__(self):
        """Prepare loading of settings. They will become effective
        only after `reload()` and `apply()`.
        """
        self._init_default_config()
        self._init_user_config()
        self._additional_configs = []

    def _init_default_config(self):
        self._defaults = PartialConfig(
            description="default",
            path=resources.get_config_path("defaults.yaml"),
            required=True
        )

    def _init_user_config(self):
        alternative_user_config = os.environ.get("MEETY_USER_CONFIG")
        if alternative_user_config is None:
            self._init_user_config_standard()
        else:
            self._init_user_config_alternative(alternative_user_config)

    def _init_user_config_standard(self):
        Config._ensure_user_config(
            resources.get_config_path("user.yaml"),
            user_config_path("config.yaml")
        )
        self._user = PartialConfig(
            description="user",
            path=user_config_path("config.yaml")
        )

    def _init_user_config_alternative(self, path):
        abspath = os.path.abspath(path)
        log.info(f"Using alternative user configuration file '{abspath}'.")
        self._user = PartialConfig(
            description="user",
            path=user_config_path(abspath)
        )

    def reload(self):
        """(Re-)Load the configuration from the predefined files."""
        self.defaults.load()
        self.user.load()
        self._load_additional_configs(
            self._determine_additional_configs()
        )

    def _determine_additional_configs(self):
        """Determine additional partial configurations based on
        the settings in the default and user configurations.
        """
        additionals = self.defaults.additional_configs.copy()
        additionals.update(self.user.additional_configs)
        return additionals

    def apply(self):
        """Apply all registered partial configurations."""
        self.defaults.apply()
        self.user.apply()
        for additional_config in self.additional_configs:
            additional_config.apply()

    def _load_additional_configs(self, additionals):
        for name, status in additionals.items():
            if io.str_is_true(status):
                self._load_additional_config(name)

    def _load_additional_config(self, name):
        filename = f"{name}.yaml"
        config = PartialConfig(
            description=name,
            path=resources.get_config_path(filename)
        )
        config.load()
        self._additional_configs.append(config)

    @property
    def defaults(self):
        """Return partial configuration for application defaults."""
        return self._defaults

    @property
    def user(self):
        """Return partial configuration by user."""
        return self._user

    @property
    def additional_configs(self):
        """Return additional partial configurations."""
        return self._additional_configs

    @property
    def all_partial_configs(self):
        """Return all partial configurations (defaults, user,
        additional).
        """
        return [self.defaults, self.user] + self.additional_configs

    def __str__(self):
        return "\n".join([str(c) for c in self.all_partial_configs])


class PartialConfig:
    """Manages the configuration provided by a single YAML file."""

    def __init__(self, description, path, required=False):
        """Prepare configuration for loading and application."""
        self._description = description
        self._path = path
        self._data = {}
        self._required = required

    @property
    def description(self):
        return self._description

    @property
    def data(self):
        return self._data

    @property
    def additional_configs(self):
        return io.expect_dict(self.data.get("additional_config"))

    @property
    def cli(self):
        return io.expect_dict(self.data.get("cli"))

    @property
    def cli_styles(self):
        return io.expect_dict(self.cli.get("styles"))

    @property
    def gui(self):
        return io.expect_dict(self.data.get("gui"))

    @property
    def gui_styles(self):
        return io.expect_dict(self.gui.get("styles"))

    @property
    def meetings(self):
        return io.expect_dict(self.data.get("meetings"))

    @property
    def connect(self):
        return io.expect_dict(self.data.get("connect"))

    def load(self):
        """Store loaded dictionary or empty dictionary, on failure."""
        self._data = self._load()

    def _load(self):
        status = "FAILED"
        config = {}
        try:
            with open(self._path) as cfile:
                config = yaml.load(cfile, Loader=yaml.BaseLoader)
                assert isinstance(config, dict)
        except FileNotFoundError:
            if self._required:
                log.warning(f"Cannot find configuration '{self.description}'.")
            else:
                log.warning(f"No configuration '{self.description}'.")
        except Exception as e:
            log.warning(f"Cannot read {self.description} configuration.")
            log.exception(e)
        else:
            status = "successful"
        finally:
            log.info(f"Load configuration '{self.description}': {status}")
            return config

    def app(self, app_name):
        return self.data.get(app_name, {})

    def args(self, app_name):
        """Return predefined list of command-line arguments for argparser."""
        arguments = self.app(app_name).get("args", [])
        split_args = []
        for argument in arguments:
            split_args.extend(argument.split(" "))
        return split_args

    def apply(self):
        """Apply configuration, pass information to the submodules."""
        connect.set_options(self.connect)
        meetings.set_options(self.meetings, self.description)
        cli_styles.set_options(self.cli_styles)
        gui_styles.set_options(self.gui_styles)

    def __str__(self):
        """Return description and textual representation of the dictionary."""
        return f"{self.description}:\n{self.data}"


def user_config_path(filename):
    """Return the path of the user file with the given name."""
    dir_path = appdirs.user_config_dir(Config.PROGRAM)
    os.makedirs(dir_path, exist_ok=True)
    return os.path.join(dir_path, filename)


def open_user_config(filename):
    """Return stream to the user file with the given name."""
    path = user_config_path(filename)
    return open(path)
