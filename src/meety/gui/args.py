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
    parser.add_argument(
        "-X", "--window-xpos",
        help="set relative horizontal window position (between 0 and 1)",
        action="store",
        type=float,
        default=0.5,
    )
    parser.add_argument(
        "-Y", "--window-ypos",
        help="set relative vertical window position (between 0 and 1)",
        action="store",
        type=float,
        default=0.5,
    )
