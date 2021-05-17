"""Arguments for the command-line interface."""


def add_argparser_arguments(parser):
    parser.add_argument(
        "-a", "--all",
        help="include all meetings",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "-t", "--test-run",
        help="print connect command, don't connect",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "-1", "--first",
        help="choose first if there are multiple meetings",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "-b", "--best",
        help="consider only best matching meetings",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "-y", "--yes",
        help="assume yes (don't ask to connect)",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "-s", "--show-only",
        help="show only matches, don't connect",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "-c", "--choose-connection",
        help="ask for connection handler, if multiple",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "--list-connection-handlers",
        help="list only active connection handlers",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "--list-meetings",
        help="list only meeting details",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "--list-ratings",
        help="list only ratings",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "-i", "--stdin",
        help="consider specification from standard input only",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "-u", "--url",
        help="connect via the the given url",
        action="store",
        type=str,
    )
    parser.add_argument(
        "--datetime",
        help="use given datetime instead of current",
        action="store",
        default=None,
    )
    parser.add_argument(
        "query",
        help="search phrase",
        nargs="*",
        default=["*"],
    )
