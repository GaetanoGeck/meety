import pytest

from meety.io.datetime.weekday_translations import (
    WeekdayTranslation,
    WeekdayTranslator,
)

lang_en = {
    "1": ["Monday", "Mon"],
    "2": ["Tuesday", "Tue"],
    "3": ["Wednesday", "Wed"],
    "4": ["Thursday", "Thu"],
    "5": ["Friday", "Fri"],
    "6": ["Saturday", "Sat"],
    "7": ["Sunday", "Sun"],
}
lang_de = {
    "1": ["Montag", "Mo"],
    "2": ["Dienstag", "Di"],
    "3": ["Mittwoch", "Mi"],
    "4": ["Donnerstag", "Do"],
    "5": ["Freitag", "Fr"],
    "6": ["Samstag", "Sa"],
    "7": ["Sonntag", "So"],
}


@pytest.mark.parametrize("number, expected", [
    (1, "Monday"),
    (2, "Tuesday"),
    (3, "Wednesday"),
    (4, "Thursday"),
    (5, "Friday"),
    (6, "Saturday"),
    (7, "Sunday"),
])
def test_english_name_by_number(number, expected):
    WeekdayTranslator.reset_options()
    WeekdayTranslation("lang_en", lang_en)
    got_name = WeekdayTranslator.get_name_by_number(number)
    assert got_name == expected


@pytest.mark.parametrize("number, expected", [
    (1, "1"),
    (2, "2"),
    (3, "3"),
    (4, "4"),
    (5, "5"),
    (6, "6"),
    (7, "7"),
])
def test_empty_name_by_number(number, expected):
    WeekdayTranslator.reset_options()
    got_name = WeekdayTranslator.get_name_by_number(number)
    assert got_name == expected


@pytest.mark.parametrize("number, expected", [
    (1, "Monday"),
    (2, "Tuesday"),
    (3, "Wednesday"),
    (4, "Thursday"),
    (5, "Friday"),
    (6, "Saturday"),
    (7, "Sunday"),
])
def test_EN_DE_name_by_number(number, expected):
    WeekdayTranslator.reset_options()
    WeekdayTranslation("lang_en", lang_en)
    WeekdayTranslation("lang_de", lang_de)
    got_name = WeekdayTranslator.get_name_by_number(number)
    assert got_name == expected


@pytest.mark.parametrize("number, expected", [
    (1, "Montag"),
    (2, "Dienstag"),
    (3, "Mittwoch"),
    (4, "Donnerstag"),
    (5, "Freitag"),
    (6, "Samstag"),
    (7, "Sonntag"),
])
def test_EN_DE_name_by_number_prefer_DE(number, expected):
    WeekdayTranslator.reset_options()
    WeekdayTranslator.prefer("lang_de")
    WeekdayTranslation("lang_en", lang_en)
    WeekdayTranslation("lang_de", lang_de)
    got_name = WeekdayTranslator.get_name_by_number(number)
    assert got_name == expected


@pytest.mark.parametrize("name, expected", [
    ("1", 1),
    ("Monday", 1),
    ("monday", 1),
    ("MONDAY", 1),
    ("Mon", 1),
    ("Montag", 1),
    ("Mo", 1),
    ("2", 2),
    ("Tuesday", 2),
    ("Tue", 2),
    ("Dienstag", 2),
    ("Di", 2),
    ("3", 3),
    ("Wednesday", 3),
    ("Wed", 3),
    ("Mittwoch", 3),
    ("Mi", 3),
    ("4", 4),
    ("Thursday", 4),
    ("Thu", 4),
    ("Donnerstag", 4),
    ("Do", 4),
    ("5", 5),
    ("Friday", 5),
    ("Fri", 5),
    ("Freitag", 5),
    ("Fr", 5),
    ("6", 6),
    ("Saturday", 6),
    ("Sat", 6),
    ("Samstag", 6),
    ("Sa", 6),
    ("7", 7),
    ("Sunday", 7),
    ("Sun", 7),
    ("Sonntag", 7),
    ("So", 7),
])
def test_english_number_by_name(name, expected):
    WeekdayTranslator.reset_options()
    WeekdayTranslation("lang_en", lang_en)
    WeekdayTranslation("lang_de", lang_de)
    print(WeekdayTranslator)
    got_number = WeekdayTranslator.get_number_by_name(name)
    assert got_number == expected


@pytest.mark.parametrize("name", [
    None,
    "",
    "someday",
])
def test_english_number_by_name_exception(name):
    WeekdayTranslator.reset_options()
    WeekdayTranslation("lang_en", lang_en)
    with pytest.raises(KeyError):
        WeekdayTranslator.get_number_by_name(name)
