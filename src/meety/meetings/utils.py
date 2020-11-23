from meety.logging import log


def list_of_ranges(text):
    """Returns a list of ranges induced by a string.

    >>> list_of_ranges("1, 3-5")
    [['1'], ['3', '5']]
    """
    if text and isinstance(text, str):
        ranges = text.split(",")
        return [text_range(r) for r in ranges]
    return []


def text_range(text):
    """Split range of non-dash entries into list of stripped texts.
    Special care is taken on ranges of dates (which contain dashes).

    >>> text_range("foo")
    ['foo']
    >>> text_range("foo - bar")
    ['foo', 'bar']
    >>> text_range("foo-bar-baz")
    ['foo-bar-baz']
    >>> text_range("2020-01-21 - 2020-04-21")
    ['2020-01-21', '2020-04-21']
    """
    count = text.count("-")
    if count == 0:
        return [text.strip()]
    if count == 1:
        return [t.strip() for t in text.split("-")]
    elif count == 5:
        # date ranges:
        parts = [t.strip() for t in text.split("-")]
        return [
            "-".join(parts[0:3]),
            "-".join(parts[3:6])
        ]
    else:
        return [text]


def to_pair(entries, default=(None, None)):
    """Converts a list into a pair if it has at most two entries.
    Otherwise the default pair is returned.

    >>> to_pair([1])
    (1, 1)
    >>> to_pair([1, 2])
    (1, 2)
    >>> to_pair([1, 2, 3])
    (None, None)
    >>> to_pair([1, 2, 3], (8,9))
    (8, 9)
    """
    if len(entries) == 1:
        # make start point also end point
        return (entries[0], entries[0])
    if len(entries) == 2:
        return (entries[0], entries[1])
    else:
        log.expected("pair", "", entries)
        return default
