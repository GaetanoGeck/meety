"""The command-line interface program."""

import sys
from datetime import datetime

from meety import connect
from meety.cli import styles as styles
from meety.cli.args import add_argparser_arguments  # USED
from meety.cli.utils import (
    index_choice,
    print_indexed_names,
    yes_no_choice,
)
from meety.io import copy_to_clipboard
from meety.logging import log
from meety.meetings.rating import Ratings

name = "cli"


def run(args, loader):
    meetings = loader.meetings
    if args.stdin:
        msg = " ".join([
            "Reading meeting specification(s) from standard input",
            "[complete with Ctrl+D]",
        ])
        print(msg)
        spec = "".join(sys.stdin.readlines())
        loader.unload()
        meetings = add_meeting_from_spec(args, loader, spec)
    if args.url:
        spec = f"name: URL ({args.url})\nurl: {args.url}"
        loader.unload()
        meetings = add_meeting_from_spec(args, loader, spec)
    if args.list_connection_handlers:
        print(connect.handlers)
    elif args.list_meetings:
        _list_meeting_details(meetings)
    else:
        matches = _rate_and_match(args, meetings)
        if args.list_ratings:
            _show_ratings(matches)
        else:
            _show_and_connect(args, matches)


def add_meeting_from_spec(args, loader, spec):
    loader.unload()
    loader.add_runtime_specs(spec)
    args.all = True
    args.yes = True
    loader.reload()
    return loader.meetings


def _show_ratings(matches):
    print("Ratings (Q|T|x = matches query|time|not):")
    print("\n".join([f"  - {rm.debug_info()}" for rm in matches]))


def _rate_and_match(args, meetings):
    rating = Ratings(meetings)
    when = _get_datetime(args.datetime)
    rating.rate(args.query, when)
    return _get_matches(args, rating)


def _show_and_connect(args, matches):
    _show_meetings(matches)
    if not args.show_only:
        _choose_and_connect(args, matches)


def _choose_and_connect(args, matches):
    meeting = _choose_meeting(matches)
    if meeting:
        _try_to_connect_to_meeting(args, meeting)
    else:
        print("No meeting found. Goodbye!")


def _list_meeting_details(meetings):
    print("Meeting details:")
    for m in meetings:
        print(m.debug_info())


def _get_datetime(text):
    if not text:
        return datetime.now()

    when = _parse_datetime_argument(text)
    if not when:
        log.expected("format yyyy-mm-ddTHH:MM", "datetime", text)
        return None


def _parse_datetime_argument(text):
    try:
        when = datetime.strptime(text, "%Y-%m-%dT%H:%M")
    except ValueError:
        return None
    else:
        return when


def _get_matches(args, rating):
    if args.all:
        return rating.get_all()
    elif args.best:
        return rating.get_only_best()
    elif args.first:
        return rating.get_only_first()
    else:
        return rating.get_all_matching()


def _show_meetings(matches):
    count = len(matches)
    if count == 1:
        _show_single_meeting(matches[0])
    elif count > 1:
        _show_multiple_meetings(matches)


def _show_single_meeting(match):
    text = _print_rated_meeting(match)
    print(f"There's one matching meeting: {text}")


def _show_multiple_meetings(matches):
    print("There are multiple matches:")
    print_indexed_names(matches, _print_rated_meeting)
    print("Which one do you want to choose?", end=" ")


def _print_rated_meeting(rmeeting):
    name = str(rmeeting)
    style_name = rmeeting.match_style
    return styles.style(name, style_name)


def _choose_meeting(matches):
    count = len(matches)
    if count == 1:
        return matches[0].meeting
    if count > 1:
        index = index_choice(1, len(matches), "1", 3) - 1
        return matches[index].meeting


def _try_to_connect_to_meeting(args, meeting):
    if args.yes or _ask_to_connect():
        _connect_to_meeting(args, meeting)


def _connect_to_meeting(args, meeting):
    if args.copy_password:
        _copy_password(meeting)
    handler = _get_handler(meeting, args.choose_connection)
    if handler:
        _connect_with_handler(handler, args.test_run)


def _get_handler(meeting, choose):
    handlers = connect.applicable_handlers(meeting)
    log.debug(f"Handlers found: {handlers}")
    handler = _choose_handler(handlers, choose)
    log.debug(f"Handler chosen: {handler}")
    return handler


def _connect_with_handler(handler, test_run):
    connect.start(handler, test_run)
    if test_run:
        print(
            styles.bf("This is a test run. ")
            + "The following command would be used in a normal run."
            + f"\n\n{handler.cmd}"
        )


def _ask_to_connect():
    print("Really connect (y/N)?", end=" ")
    okay = yes_no_choice()
    print()
    if okay == "y":
        print("Fine, connecting ...")
        return True
    else:
        print("Okay, aborting. Goodbye!")
        return False


def _copy_password(meeting):
    password = meeting.data.get("password")
    if password:
        print("...Copied password to clipboard.")
        copy_to_clipboard(password)


def _choose_handler(handlers, choose_connection):
    if not handlers:
        print("Cannot find a connection handler!")
        return None
    if len(handlers) == 1 or not choose_connection:
        return handlers[0]

    return _choose_from_multiple_handlers(handlers)


def _choose_from_multiple_handlers(handlers):
    _print_multiple_handlers(handlers)
    return _ask_for_handler(handlers)


def _print_multiple_handlers(handlers):
    print("There are multiple connection handlers:")
    print_indexed_names([h.name for h in handlers])
    print("Which one do you want to choose?", end=" ")


def _ask_for_handler(handlers):
    index = index_choice(1, len(handlers), "1", 3) - 1
    return handlers[index]
