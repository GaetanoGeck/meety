import datetime
from contextlib import suppress

from meety.io import utils
from meety.io.datetime.weekday_translations import WeekdayTranslator
from meety.logging import log

_date_formats = []
_time_formats = []
_skip_words = []
_range_words = []
_list_words = []


def reset_options():
    _reset_options_date()
    _reset_options_time()
    _reset_options_skip_words()
    _reset_options_range_words()
    _reset_options_list_words()


def set_options(config, name):
    _set_options_date(config.get("date") or {})
    _set_options_time(config.get("time") or {})
    _set_options_weekday(config.get("weekday") or {}, name)
    _set_options_skip_words(config.get("skip words") or [])
    _set_options_range_words(config.get("range words") or [])
    _set_options_list_words(config.get("list words") or [])


def _reset_options_skip_words():
    global _skip_words
    _skip_words = []


def _set_options_skip_words(words):
    if isinstance(words, str):
        clean_words = [words]
    else:
        clean_words = words
    if not isinstance(clean_words, list):
        log.expected("string or list of strings", "skip words", words)
    for w in clean_words:
        if isinstance(w, str):
            _skip_words.append(f" {w.strip()} ")


def _reset_options_range_words():
    global _range_words
    _range_words = []


def _set_options_range_words(words):
    if isinstance(words, str):
        clean_words = [words]
    else:
        clean_words = words
    if not isinstance(clean_words, list):
        log.expected("string or list of strings", "range words", words)
    for w in clean_words:
        if isinstance(w, str):
            _range_words.append(f" {w.strip()} ")


def _reset_options_list_words():
    global _list_words
    _list_words = []


def _set_options_list_words(words):
    if isinstance(words, str):
        clean_words = [words]
    else:
        clean_words = words
    if not isinstance(clean_words, list):
        log.expected("string or list of strings", "list words", words)
    for w in clean_words:
        if isinstance(w, str):
            _list_words.append(f" {w.strip()} ")


def prepare_list_of_ranges(text):
    text = f" {text} "
    # prepend and append one space
    # to allow for matching words
    # at the beginning or the end

    text = utils.replace_words_by(text, _skip_words, " ")
    text = utils.replace_words_by(text, _range_words, " - ")
    text = utils.replace_words_by(text, _list_words, ", ")
    return text.strip()


def parse_timedelta(config):
    args = {k: int(v) for (k, v) in config.items()}
    try:
        delta = datetime.timedelta(**args)
    except TypeError as e:
        log.expected("valid arguments", "time delta", args)
        log.exception(e)
        return datetime.timedelta()
    else:
        return delta


def _reset_options_date():
    global _date_formats
    _date_formats = [
        "%Y-%m-%d",
        "%d.%m.%Y",
        "%d.%m.%y",
        "%d.%m.'%y",
    ]


def _set_options_date(config):
    formats = utils.expect_list_of_str(config.get("format"))
    for f in formats:
        _date_formats.append(f)


def parse_date(text, warn=True):
    clean_text = text.strip().casefold()
    for f in _date_formats:
        with suppress(ValueError):
            return datetime.datetime.strptime(clean_text, f)
    log.warning(f"Cannot parse date '{text}'.", warn)
    return None


def date_to_str(date):
    if date:
        return date.strftime("%Y-%m-%d")
    return "<UNDEFINED>"


def _reset_options_time():
    global _time_formats
    _time_formats = ["%H:%M", "%H.%M", "%H"]


def _set_options_time(config):
    formats = utils.expect_list_of_str(config.get("format"))
    for f in formats:
        _time_formats.append(f)


def parse_time(text, warn=True):
    clean_text = text.strip().casefold()
    for f in _time_formats:
        with suppress(ValueError):
            return datetime.datetime.strptime(clean_text, f).time()
    log.warning(f"Cannot parse time '{text}'.", warn)
    return None


def time_to_str(time):
    if time:
        return time.strftime("%H:%M")
    return "<UNDEFINED>"


def _reset_options_weekday():
    WeekdayTranslator.reset_options()


def _set_options_weekday(config, name):
    WeekdayTranslator.set_options(config.get("names") or {}, name)


def parse_weekday(text, warn=True):
    clean_text = str(text).strip().casefold()
    try:
        return WeekdayTranslator.get_number_by_name(clean_text)
    except KeyError:
        log.warning(f"Cannot parse weekday '{text}'.", warn)
        return None


def weekday_to_str(weekday):
    if weekday:
        name = WeekdayTranslator.get_name_by_number(weekday)
        return name or str(weekday)
    return "<UNDEFINED>"


reset_options()
