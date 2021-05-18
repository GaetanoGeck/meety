import glob
import os
from collections import (
    OrderedDict,
    namedtuple,
)

import yaml

from meety import io
from meety.logging import log
from meety.meetings.meeting import Meeting


class Loader:
    """Manages file selection and loading.

    There are implicit directories, provided by default, and explicit
    directories, provided by the user. The loader will consider all YAML files
    (by extension) in the explicit directories and, if not disabled, also in
    the implicit directories.
    Additionally, the loader will consider all explicitly specified YAML files.
    """

    implicit_directories = [
        os.getcwd(),
        os.path.expanduser("~"),
    ]

    @classmethod
    def _yaml_files_in_directories(cls, directories):
        """Returns paths to all files with extension 'yaml' or 'yml' in
        the given list of directories.
        """
        files = []
        for directory in directories:
            files.extend(cls._yaml_files_in_directory(directory))
        return files

    @classmethod
    def _yaml_files_in_directory(cls, directory):
        """Returns paths to all files with extension 'yaml' or 'yml' in
        the given directory.
        """
        def files_in_by_extension(directory, ext):
            return glob.glob(os.path.join(directory, f"*.{ext}"))
        return (
            files_in_by_extension(directory, "yaml")
            + files_in_by_extension(directory, "yml")
        )

    def _load_meeting_entries_from_file(self, filename):
        """Try to load meetings from YAML file, return list of meetings"""
        data = self._load_data_from_file(filename)
        return self._create_meetings_from_data(data)

    def _load_meeting_entries_from_spec(self, spec):
        """Try to load meetings from YAML specification,
        return list of meetings.
        """
        data = self._load_data_from_spec(spec)
        new_meetings = self._create_meetings_from_data(data)
        self._meetings.extend(new_meetings)

    def _load_data_from_file(self, filename):
        """Try to load data from YAML file, return empty dictionary on
        failure.
        """
        try:
            with open(filename) as file:
                return yaml.load(file, Loader=yaml.BaseLoader)
        except FileNotFoundError as e:
            self._loaded_paths.fail_on(filename, "does not exist")
            log.warning(f"Meeting file '{filename}' does not exist.")
            log.exception(e, warn=False)
            return None
        except Exception as e:
            self._loaded_paths.fail_on(filename, "failed to parse")
            log.warning(f"Failed to load meetings from '{filename}'")
            log.exception(e)
            return None

    def _load_data_from_spec(self, text):
        try:
            return yaml.load(text, Loader=yaml.BaseLoader)
        except Exception as e:
            log.warning(f"Failed to load temporary meetings from '{text}'")
            log.exception(e)
            return None

    @classmethod
    def _create_meetings_from_data(cls, data):
        """Create meeting from a single entry or meetings from a list
        of entries."""
        if data is None:
            return None
        meetings = []
        if not isinstance(data, list):
            data = [data]
        for d in data:
            m = cls._create_meeting_from_data(d)
            if m:
                meetings.append(m)
        return meetings

    @classmethod
    def _create_meeting_from_data(cls, data):
        """Create a meeting from a single entry."""
        clean_data = io.process(data)
        if Meeting.is_meeting_entry(clean_data):
            return Meeting(data, clean_data)

    def __init__(self):
        """Start with no explicit directories and files but with
        implicit directories enabled."""
        self._explicit_directories = []
        self._explicit_files = []
        self.only_explicit = False
        self._loaded_paths = LoadedPaths()
        self._meetings = []
        self._yaml_runtime_specs = []

    def add_explicit_directories(self, directories):
        clean_dirs = [os.path.expanduser(d) for d in directories]
        self._explicit_directories.extend(clean_dirs)

    def add_explicit_files(self, files):
        clean_files = [os.path.expanduser(f) for f in files]
        self._explicit_files.extend(clean_files)

    @property
    def active_directories(self):
        if self.only_explicit:
            return set(self._explicit_directories)
        return set(self._explicit_directories + Loader.implicit_directories)

    @property
    def explicit_files(self):
        return self._explicit_files

    @property
    def implicit_files(self):
        return Loader._yaml_files_in_directories(self.active_directories)

    @property
    def all_files(self):
        return self.explicit_files + self.implicit_files

    @property
    def loaded_paths(self):
        return self._loaded_paths

    @property
    def meetings(self):
        return self._meetings

    def unload(self):
        self._meetings = []
        self._loaded_paths.remove_all()

    def load(self):
        """Load from all explicitly and implicitly specified files if
        the file has not already been read.
        """
        files = self.all_files
        self._log_files_to_consider(files)
        for f in files:
            self._consider_to_load_from_file(f)

    def add_file(self, filename):
        self._consider_to_load_from_file(filename)

    def add_runtime_specs(self, text):
        self._yaml_runtime_specs.append(text)

    def reload(self):
        """Reload data from already loaded files."""
        self._meetings = []
        for path in self._loaded_paths.all_paths:
            self.load_from_file(path)
        for spec in self._yaml_runtime_specs:
            self._load_meeting_entries_from_spec(spec)

    def _log_files_to_consider(self, files):
        if not files:
            log.warning("No YAML files to consider!")
        else:
            log.info("Will consider the following YAML files:")
            log.info("\n".join([f"  - {f}" for f in files]))

    def _consider_to_load_from_file(self, filename):
        """Load from file if it has not already been loaded."""
        if self._loaded_paths.contains(filename):
            log.info(f"Skipping file '{filename}', already read.")
        else:
            self.load_from_file(filename)

    def load_from_file(self, filename):
        """Unconditionally load meetings from file and save them."""
        all_meetings = self._load_meeting_entries_from_file(filename)
        if all_meetings is not None:
            new_meetings = [
                m for m in all_meetings
                if m not in self._meetings
            ]
            self._log_loading_stats(
                filename,
                len(new_meetings),
                len(all_meetings),
            )
            self._meetings.extend(new_meetings)

    def _log_loading_stats(self, filename, num_new, num_all):
        details = [
            f"Adding only {num_new} new.",
            "Adding all.",
        ][num_new == num_all]
        log.info(
            f"Loaded {num_all} meetings from '{filename}'. "
            + details
        )
        self._loaded_paths.succeed_on(filename, num_new, num_all)


LoadStatus = namedtuple("LoadStatus", "new all")


class LoadedPaths:
    """Remember absolute paths of files that have already been loaded."""

    def __init__(self):
        self._status = OrderedDict()

    def contains(self, path):
        abspath = os.path.abspath(path)
        return abspath in self._status

    @property
    def all_paths(self):
        return list(self._status.keys())

    @property
    def all_failures(self):
        return {
            k: v for (k, v) in self._status.items()
            if isinstance(v, str)
        }

    def status(self, path):
        info = self._status.get(path) or "unknown"
        if isinstance(info, LoadStatus):
            return f"added {info.new} of {info.all}"
        else:
            return info

    def succeed_on(self, path, new_entries, all_entries):
        abspath = os.path.abspath(path)
        self._status[abspath] = LoadStatus(new_entries, all_entries)

    def fail_on(self, path, msg=None):
        abspath = os.path.abspath(path)
        self._status[abspath] = msg

    def remove_all(self):
        self._status.clear()
