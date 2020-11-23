import glob
import os

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

    @classmethod
    def _load_meeting_entries_from_file(cls, filename):
        """Try to load meetings from YAML file, return """
        data = cls._load_data_from_file(filename)
        return cls._create_meetings_from_data(data)

    @classmethod
    def _load_data_from_file(cls, filename):
        """Try to load data from YAML file, return empty dictionary on
        failure.
        """
        try:
            with open(filename) as file:
                return yaml.load(file, Loader=yaml.BaseLoader)
        except FileNotFoundError as e:
            log.warning(f"Meeting file '{filename}' does not found.")
            log.exception(e)
            return {}
        except Exception as e:
            log.warning(f"Failed to load meetings from '{filename}'")
            log.exception(e)
            return {}

    @classmethod
    def _create_meetings_from_data(cls, data):
        """Create meeting from a single entry or meetings from a list
        of entries."""
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

    def add_explicit_directories(self, directories):
        self._explicit_directories.extend(directories)

    def add_explicit_files(self, files):
        self._explicit_files.extend(files)

    @property
    def active_directories(self):
        if self.only_explicit:
            return self._explicit_directories
        return self._explicit_directories + Loader.implicit_directories

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

    def load(self):
        """Load from all explicitly and implicitly specified files if
        the file has not already been read.
        """
        files = self.all_files
        self._log_files_to_consider(files)
        for f in files:
            self._consider_to_load_from_file(f)

    def reload(self):
        """Reload data from already loaded files."""
        self._meetings = []
        for path in self._loaded_paths.all_paths():
            self.load_from_file(path)

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
            self._loaded_paths.add(filename)

    def load_from_file(self, filename):
        """Unconditionally load meetings from file and save them."""
        meetings = self._load_meeting_entries_from_file(filename)
        new_meetings = [m for m in meetings if m not in self._meetings]
        self._log_loading_stats(filename, meetings, new_meetings)
        self._meetings.extend(new_meetings)

    def _log_loading_stats(self, filename, meetings, new_meetings):
        num_read = len(meetings)
        num_new = len(new_meetings)
        details = [
            f"Adding only {num_new} new.",
            "Adding all.",
        ][num_read == num_new]
        log.info(
            f"Loaded {num_read} meetings from '{filename}'. "
            + details
        )


class LoadedPaths:
    """Remember absolute paths of files that have already been loaded."""
    def __init__(self):
        self._abspaths = set()

    def contains(self, path):
        abspath = os.path.abspath(path)
        if abspath in self._abspaths:
            return True
        else:
            return False

    def add(self, path):
        abspath = os.path.abspath(path)
        self._abspaths.add(abspath)

    def all_paths(self):
        return list(self._abspaths)
