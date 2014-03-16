The repeat command
------------------

'repeat' is a dirt simple Python script to repeat a command
indefinitely, or for a fixed number of iterations.  I wrote
it because I got bored of writing::

    for ($i = 0; $i -lt 100; $i++) do { stuff; }

repeatedly in PowerShell, while trying to provoke threading-related
race conditions in test code.  It also lets me write the same line
on different platforms, without having to remember whether I'm in
bash, PowerShell, or a regular Windows CMD prompt.

Example usage::

    taniyama:Desktop mdickinson$ repeat 3 python -c "print 2+2"
    repeat: Repeating ['python', '-c', 'print 2+2'] 3 times.
    repeat: Starting run 0 of 3.
    4
    repeat: Run 0 of 3 completed.
    repeat: Starting run 1 of 3.
    4
    repeat: Run 1 of 3 completed.
    repeat: Starting run 2 of 3.
    4
    repeat: Run 2 of 3 completed.
    repeat: Exiting with returncode 0.

The script will stop as soon as the command being executed exits with a nonzero
return code, and will exit with that return code.  On successful completion it
will exit with return code 0.  Some day I may add an option to continue on
error, but I haven't needed that option yet.

More simply, omit the count argument to repeat indefinitely::

    taniyama:Desktop mdickinson$ repeat python -c "print 2+2"
    repeat: Repeating ['python', '-c', 'print 2+2'] forever.
    repeat: Starting run 0.
    4
    repeat: Run 0 completed.
    repeat: Starting run 1.
    4
    repeat: Run 1 completed.
    repeat: Starting run 2.
    4
    repeat: Run 2 completed.
    repeat: Starting run 3.
    4
    repeat: Run 3 completed.
    repeat: Starting run 4.
    <and so on>

In the unlikely case that your command starts with an integer, you can
disambiguate using a count of ``forever``: ``repeat forever python -c "print
2+2"``.  (That of course also means that in the unlikely event that your
command happens to start with ``forever``, you'll also need to use ``forever``
to disambiguate: ``repeat forever forever ...``.)

To silence the progress output, use the `-q` option::

    taniyama:Desktop mdickinson$ repeat -q python -c "print 2+2"
    4
    4
    4


Usage
-----

Type ``repeat --help`` to see options::

    taniyama:Desktop mdickinson$ repeat --help
    usage: repeat [-h] [-q] count ...

    Repeat a command forever or a fixed number of times.

    positional arguments:
      count        number of iterations, or 'forever'
      cmd          command to execute

    optional arguments:
      -h, --help   show this help message and exit
      -q, --quiet  suppress progress output


Installation
------------

Clone this repository, enter the top-level directory, and do a "python
setup.py install" (or "python setup.py develop" if you prefer)::

    git clone git@github.com:mdickinson/repeat.git
    cd repeat
    python setup.py develop

