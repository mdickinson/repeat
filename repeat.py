import argparse
import itertools
import subprocess
import sys


def repeat(cmd, count=None):
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
        print "Starting run {}.".format(index)
        subprocess.check_call(cmd)
        print "Run {} completed.".format(index)


def nonnegative_int(string):
    value = int(string)
    if value < 0:
        raise argparse.ArgumentTypeError(
            "{} is negative".format(value)
        )
    return value


def main():
    parser = argparse.ArgumentParser(
        description="Repeat a command forever or a fixed number of times.",
    )
    parser.add_argument(
        "-n", "--count",
        type=nonnegative_int,
        default=None,
        help="Run for COUNT iterations",
    )
    parser.add_argument(
        "cmd",
        nargs=argparse.REMAINDER,
        help="Command to execute",
    )
    args = parser.parse_args()
    repeat(args.cmd, count=args.count)
