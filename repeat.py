import argparse
import itertools
import subprocess


def repeat(cmd, count=None, verbose=True):
    """
    Run the given command (via subprocess) 'count' times.

    If count is None (the default), run indefinitely.

    Halts as soon as cmd exits abnormally.

    """
    if count is None:
        run_indices = itertools.count()
    else:
        run_indices = xrange(count)

    for index in run_indices:
        if verbose:
            print "Starting run {}.".format(index)
        subprocess.check_call(cmd)
        if verbose:
            print "Run {} completed.".format(index)


def parse_count(string):
    if string.lower() == 'forever':
        return None
    else:
        value = int(string)
        if value < 0:
            raise ValueError("{} is negative".format(value))
        return value


def main():
    parser = argparse.ArgumentParser(
        description="Repeat a command forever or a fixed number of times.",
        # Necessary to override the name on Windows, else we'll see
        # repeat-script.py here.
        prog="repeat",
    )
    parser.add_argument(
        "count",
        help="number of iterations, or 'forever'",
    )
    parser.add_argument(
        "-q", "--quiet",
        action='store_true',
        default=False,
        help="suppress progress output",
    )
    parser.add_argument(
        "cmd",
        nargs=argparse.REMAINDER,
        help="command to execute",
    )

    args = parser.parse_args()

    # Backwards compatibility: if we can't parse 'count', treat
    # it as the first part of the command.
    try:
        count = parse_count(args.count)
    except ValueError:
        count = None
        args.cmd.insert(0, args.count)

    repeat(args.cmd, count=count, verbose=not args.quiet)
