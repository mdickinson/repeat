import argparse
import itertools
import subprocess
import sys


count_descriptions = {
    None: "forever",
    1: "once",
    2: "twice",
}
count_description_default = "{count} times"


def repeat(cmd, count=None, verbose=True, prefix="repeat: "):
    """
    Run the given command (via subprocess) 'count' times.

    If *count* is None (the default), run indefinitely.

    If *verbose* is true, output progress information.  Progress
    information is prefixed with *prefix*.

    Halts as soon as cmd exits abnormally.

    """
    if verbose:
        count_description = count_descriptions.get(
            count, count_description_default).format(count=count)
        print "{}Repeating {} {}.".format(prefix, cmd, count_description)

    if count is None:
        run_indices = itertools.count()
    else:
        run_indices = xrange(count)

    for index in run_indices:
        if verbose:
            if count is None:
                run_description = "{index}".format(index=index)
            else:
                run_description = "{index} of {count}".format(
                    index=index, count=count)
            print "{}Starting run {}.".format(prefix, run_description)

        try:
            subprocess.check_call(cmd)
        except subprocess.CalledProcessError as exc:
            returncode = exc.returncode
            if verbose:
                print "{}Run {} failed with returncode {}.".format(
                    prefix, run_description, returncode)
            break
        else:
            if verbose:
                print "{}Run {} completed.".format(prefix, run_description)
    else:
        # All runs completed successfully.
        returncode = 0

    if verbose:
        print "{}Exiting with returncode {}.".format(prefix, returncode)
    return returncode


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

    returncode = repeat(args.cmd, count=count, verbose=not args.quiet)
    sys.exit(returncode)
