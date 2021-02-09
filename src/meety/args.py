import os

DEFAULT_MEETING_SPEC = os.path.join(
    os.path.expanduser("~"),
    "meetings.yaml"
)


def _add_argparser_common_arguments(parser, summary):
    parser.add_argument(
        "-f", "--file",
        dest="files",
        metavar="PATH",
        help="include meeting file",
        default=[],
        action="append",
    )
    parser.add_argument(
        "-d", "--directory",
        dest="directories",
        metavar="PATH",
        help="include YAML files in directory",
        default=[],
        action="append",
    )
    parser.add_argument(
        "-e", "--only-explicit",
        help="only include meeting files in the arguments",
        action="store_true",
    )
    parser.add_argument(
        "-p", "--copy-password",
        help="copy password to clipboard on connection",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "--init",
        dest="init",
        metavar="PATH",
        help="create template meeting specification",
        nargs="?",
        const=DEFAULT_MEETING_SPEC,
        type=str,
    )
    parser.add_argument(
        "--verbose",
        help="increase logging verbosity",
        action="store_true",
    )
    parser.add_argument(
        "--debug",
        help="increase logging verbosity even more",
        action="store_true",
    )
    parser.add_argument(
        "-v", "--version",
        action="version",
        version=summary,
    )
