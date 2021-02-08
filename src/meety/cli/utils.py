"""Some utility functions for the command-line interface."""

from meety.cli import styles


def print_indexed_names(items, name_func=styles.bf_str):
    max_index = len(items)
    digits = len(str(max_index))
    for index, item in enumerate(items, 1):
        name = name_func(item)
        print(f"  [{index:{digits}}] {name}")


def input_choice(valid_answers, default_answer, tries=3):
    for count in range(0, tries):
        if count > 0:
            print("Try again: ", end="")
        answer = input_choice_once(valid_answers, default_answer)
        if answer:
            return answer
        print("Unrecognised answer.", end=" ")
    return default_answer


def input_choice_once(valid_answers, default_answer):
    answer = input()
    if answer in valid_answers:
        return answer
    elif answer.strip() == "":
        return default_answer
    else:
        return None


def index_choice(start_index, end_index, default_answer, tries=3):
    valid_indices = range(start_index, end_index + 1)
    valid_answers = [str(i) for i in valid_indices]
    answer = input_choice(valid_answers, default_answer, tries)
    return int(answer)


def yes_no_choice(default_answer='n', tries=3):
    return input_choice(
        ['y', 'Y', 'n', 'N'],
        default_answer,
        tries
    ).lower()
