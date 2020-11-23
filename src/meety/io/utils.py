def expect_dict(datum, otherwise={}):
    if isinstance(datum, dict):
        return datum
    return otherwise


def expect_list(datum, otherwise=[]):
    if isinstance(datum, list):
        return datum
    return otherwise


def expect_list_of_str(datum, otherwise=[]):
    if isinstance(datum, str):
        return [datum]
    elif isinstance(datum, list):
        return [str(d) for d in datum]
    return otherwise


def str_is_true(text):
    clean_text = text.strip().casefold()
    return clean_text in ["yes", "true", "on"]


def str_is_false(text):
    return not str_is_true(text)


def replace_words_by(text, words, replacement):
    """
    Replace all given words by the replacement text.

    >>> replace_words_by('Monday and Friday', [' and '], ', ')
    'Monday, Friday'
    >>> replace_words_by('Monday und Friday', [' and '], ', ')
    'Monday und Friday'
    """
    for w in words:
        text = text.replace(w, replacement)
    return text
