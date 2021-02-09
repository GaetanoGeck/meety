import yaml

from meety.io import is_url
from meety.logging import log
from meety.meetings.preferences import (
    TimeMatchDescription,
    TimePreference,
)


class Meeting:
    """Meetings require a name (for reference), can have a password,
    connection information and multiple time preferences.

    The `data` dictionary can comprise further keys that might be
    ignored by Meety.
    """

    @classmethod
    def is_meeting_entry(cls, data):
        """Test whether the given data is a dictionary that contains
        an entry 'name'.
        """
        return (
            isinstance(data, dict)
            and "name" in [k.casefold() for k in data.keys()]
        )

    def __init__(self, data, clean_data):
        """Initialize meeting by dictionary `data`."""
        self._input_data = data,
        self._clean_data = clean_data
        self._name = self._clean_data.get("name")
        self._password = self._clean_data.get("password")

        self._init_preferences()
        self._init_query_entries()
        self._init_url_entries()

    def _init_preferences(self):
        self._preferences = []
        values = self._clean_data.get("prefer") or []
        if not isinstance(values, list):
            # wrap a single entry in a list:
            values = [values]
        for value in values:
            if isinstance(value, dict):
                pref = TimePreference.from_dict(value)
            elif isinstance(value, str):
                pref = TimePreference.from_str(value)
            else:
                log.expected(
                    "string or dictionary",
                    "time preference specification",
                    value
                )
                pref = None
            if pref and pref.is_nontrivial:
                self._preferences.append(pref)

    def _init_query_entries(self):
        self._query_entries = []
        # keep all simple values as query entries:
        for (key, value) in self._clean_data.items():
            if not isinstance(value, (list, dict)):
                self._query_entries.append(str(value).casefold())

    def _init_url_entries(self):
        self._urls = []
        for (key, value) in self._clean_data.items():
            if isinstance(value, str) and is_url(value):
                self._urls.append(value)

    @property
    def name(self):
        return self._name or "<UNNAMED>"

    @property
    def password(self):
        return self._password

    @property
    def preferences(self):
        return self._preferences

    @property
    def input_data(self):
        return self._input_data

    def input_data_to_str(self):
        return yaml.dump(
            self.input_data[0],
            default_flow_style=False
        )

    @property
    def data(self):
        return self._clean_data

    def data_to_str(self):
        return yaml.dump(
            self.data,
            default_flow_style=False
        )

    @property
    def query_entries(self):
        return self._query_entries

    @property
    def urls(self):
        return self._urls

    def match_time(self, when):
        """Tests whether any of the time preferences is matched for the
        given datetime `when`.
        """
        otherwise = [TimeMatchDescription.NOT_MATCHING]
        return max([p.match(when) for p in self.preferences] + otherwise)

    def match_query(self, query):
        """Computes the sum of matching query items."""
        clean_query = self._clean_query(query)
        return sum([
            any([(q in e) for e in self.query_entries])
            for q in clean_query
        ])

    @classmethod
    def _clean_query(cls, query):
        """Strip and casefold all query items."""
        return [
            non_empty.casefold() for non_empty in [
                q.strip() for q in query
            ]
            if len(non_empty) > 0
        ]

    def __str__(self):
        return self.name

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.data == other.data
        return False

    def __hash__(self):
        kvs = sorted([
            str(k) + ":" + str(v)
            for k, v in self._clean_data.items()
        ], key=lambda kv: kv[0])
        return "\n".join(kvs).__hash__()

    def debug_info(self):
        return "\n".join([
            self._debug_info_base(),
            self._debug_info_prefs(),
            self._debug_info_others(),
            ""
        ])

    def _debug_info_base(self):
        p = len(self._preferences)
        return "\n".join([
            "Meeting:",
            f"  - name: {self.name}",
            f"  - password: {'yes <HIDDEN>' if self.password else 'no'}",
            f"  - preferences ({p})",
        ])

    def _debug_info_prefs(self):
        return "\n\n".join([
            f"{pref}" for pref in self._preferences
        ])

    def _debug_info_others(self):
        others = []
        for (k, v) in self.data.items():
            if k not in ["name", "password", "prefer"]:
                others.append(f"  - {k}: {v}")
        return "\n".join(others)
