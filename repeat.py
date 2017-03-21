from __future__ import unicode_literals

import argparse
import itertools
import subprocess
import sys

import six


PREFIX = "repeat: "

# Templates for output on failure and success.
FAILED = "{prefix}Run {run} failed with return code {returncode}.\n"
PASSED = "{prefix}Run {run} completed.\n"

count_descriptions = {
    None: "forever",
    1: "once",
    2: "twice",
}
count_description_default = "{count} times"


def repeat(cmd, count=None, verbose=True, keep_going=False,
           progress_stream=sys.stdout, prefix=PREFIX):
    """
    Run the given command (via subprocess) *count* times.

    If *count* is None (the default), run indefinitely.

    If *verbose* is true, write progress information to *progress_stream*.
    Each line of progress information is prefixed with *prefix*.

    Halt as soon as *cmd* exits abnormally if *keep_going* is false (the
    default). If *keep_going* is true, keep running until the desired number
    of iterations has been met.

    """
    if verbose:
        count_description = count_descriptions.get(
            count, count_description_default).format(count=count)
        progress_stream.write(
            "{prefix}Repeating {cmd} {count}.\n".format(
                prefix=prefix,
                cmd=cmd,
                count=count_description,
            )
        )

    if count is None:
        run_indices = itertools.count(1)
    else:
        run_indices = six.moves.range(1, count + 1)

    returncode = 0
    for index in run_indices:
        if verbose:
            if count is None:
                run_description = "{index}".format(index=index)
            else:
                run_description = "{index} of {count}".format(
                    index=index, count=count)
            progress_stream.write(
                "{prefix}Starting run {run}.\n".format(
                    prefix=prefix,
                    run=run_description,
                )
            )

        run_returncode = subprocess.call(cmd)

        if verbose:
            completion_message = FAILED if run_returncode != 0 else PASSED
            progress_stream.write(
                completion_message.format(
                    prefix=prefix,
                    run=run_description,
                    returncode=run_returncode,
                )
            )

        if run_returncode != 0:
            returncode = 1
            if not keep_going:
                break

    if verbose:
        progress_stream.write(
            "{prefix}Exiting with return code {returncode}.\n".format(
                prefix=prefix,
                returncode=returncode,
            )
        )
    return returncode


def parse_count(string):
    if string.lower() == 'forever':
        return None
    else:
        value = int(string)
        if value < 0:
            raise ValueError("{value} is negative".format(value=value))
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
        "-k", "--keep-going",
        action='store_true',
        default=False,
        help="keep running even if some iterations fail",
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

    returncode = repeat(
        cmd=args.cmd,
        count=count,
        verbose=not args.quiet,
        keep_going=args.keep_going,
        progress_stream=sys.stdout,
    )
    sys.exit(returncode)
