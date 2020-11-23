"""Arguments for the graphical user interface."""


def add_argparser_arguments(parser):
    parser.add_argument(
        "-W", "--window-width",
        help="set window width",
        action="store",
        type=int,
        default=500,
    )
    parser.add_argument(
        "-H", "--window-height",
        help="set window height",
        action="store",
        type=int,
        default=400,
    )
