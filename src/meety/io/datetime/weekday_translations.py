from contextlib import suppress

from meety.logging import log


class WeekdayTranslator:
    _translations = {}
    _preferred_languages = []

    @classmethod
    def reset_options(cls):
        cls._translations = {}
        cls._preferred_languages = []

    @classmethod
    def set_options(cls, config, name):
        WeekdayTranslation(name, config)

    @classmethod
    def add_translation(cls, translation):
        cls._translations[translation.language] = translation

    @classmethod
    def prefer(cls, language):
        cls._preferred_languages.append(language)

    @classmethod
    def all_languages(cls):
        return cls._translations.keys()

    @classmethod
    def ordered_languages(cls):
        for lang in cls._preferred_languages:
            yield lang
        for lang in cls.all_languages():
            if lang not in cls._preferred_languages:
                yield lang

    @classmethod
    def ordered_translations(cls):
        for lang in cls.ordered_languages():
            yield cls._translations[lang]

    @classmethod
    def get_name_by_number(cls, number):
        for trans in cls.ordered_translations():
            with suppress(KeyError):
                return trans.get_name_by_number(number)
        return str(number)

    @classmethod
    def get_number_by_name(cls, name):
        if not name:
            raise KeyError(name)
        clean_name = name.casefold()
        for trans in cls.ordered_translations():
            with suppress(KeyError):
                return trans.get_number_by_name(clean_name)
        try:
            value = int(name)
            assert 1 <= value <= 7
            return value
        except (ValueError, AssertionError):
            raise KeyError(name)

    @classmethod
    def debug_info(cls):
        return "\n".join([
            "Preferred languages:",
            cls._preferred_languages_to_str(),
            "Translations:",
            cls._translations_to_str(),
        ])

    @classmethod
    def _preferred_languages_to_str(cls):
        return "\n".join([
            f"  - {lang}"
            for lang in cls._preferred_languages
        ])

    @classmethod
    def _translations_to_str(cls):
        return "\n".join([
            f"{lang}\n--------------------\n{str(trans)}"
            for lang, trans in cls._translations.items()
        ])


class WeekdayTranslation:
    """Names for weekday numbers.
    Multiple names can be associated with a single number (for example,
    'Monday' and 'Mon' can be associated with integer 1). Each name
    can be translated to the associated integer but only the first name
    is returned on a given integer.
    """

    @classmethod
    def _ensure_valid_config(cls, config):
        valid_config = {}
        for entry in config.items():
            valid_entry = cls._ensure_valid_entry(entry)
            if valid_entry:
                num, names = valid_entry
                valid_config[num] = names
        return valid_config

    @classmethod
    def _ensure_valid_entry(cls, entry):
        num, names = entry
        num = int(num)
        if isinstance(names, str):
            return (num, [names])
        elif isinstance(names, list):
            return (num, names)
        else:
            log.expected(
                "string or list of strings",
                "names by number",
                names
            )
            return None

    def __init__(self, language, config):
        self._language = language
        config = self._ensure_valid_config(config)
        self._init_name_by_number(config)
        self._init_number_by_name(config)
        WeekdayTranslator.add_translation(self)

    def _init_name_by_number(self, config):
        self._name_by_number = {}
        for num, names in config.items():
            self._name_by_number[num] = names[0]

    def _init_number_by_name(self, config):
        self._number_by_name = {}
        for num, names in config.items():
            for name in names:
                clean_name = name.casefold()
                self._number_by_name[clean_name] = num

    @property
    def language(self):
        return self._language

    def get_name_by_number(self, number):
        return self._name_by_number[number]

    def get_number_by_name(self, name):
        return self._number_by_name[name]

    def __str__(self):
        return "\n".join([
            "Name by number:",
            self.name_by_number_to_str(),
            "Number by name:",
            self.number_by_name_to_str(),
        ])

    def name_by_number_to_str(self):
        return "\n".join([
            f"  {num}: {name}"
            for num, name in self._name_by_number.items()
        ])

    def number_by_name_to_str(self):
        return "\n".join([
            f"  {name}: {num}"
            for name, num in self._number_by_name.items()
        ])
