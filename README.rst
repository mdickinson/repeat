The repeat command
------------------

**repeat** is a dirt simple Python script to repeat a command
indefinitely, or for a fixed number of iterations.  I wrote
it because I got bored of writing (for example)::

    $ for ($i = 1; $i -le 100; $i++) { echo "Run $i"; do_stuff; echo "Run $i complete" }

repeatedly in PowerShell, while trying to provoke threading-related race
conditions in test code.  What I *wanted* to write instead was something like::

    $ repeat 100 do_stuff

to repeat 100 times, or even just::

    $ repeat do_stuff

to repeat indefinitely.  **repeat** lets me do that.  It also lets me use the
same command regardless of environment, freeing me from having to remember
whether I'm in GNU Bash, PowerShell, or a regular Windows CMD prompt.

Example usage::

    $ repeat 3 python -c "print 2+2"
    repeat: Repeating ['python', '-c', 'print 2+2'] 3 times.
    repeat: Starting run 1 of 3.
    4
    repeat: Run 1 of 3 completed.
    repeat: Starting run 2 of 3.
    4
    repeat: Run 2 of 3 completed.
    repeat: Starting run 3 of 3.
    4
    repeat: Run 3 of 3 completed.
    repeat: Exiting with return code 0.

The script will stop as soon as the command being executed exits with a nonzero
return code, and will itself exit with that same return code.  On successful
completion it will exit with return code 0.  Some day I may add an option to
continue on error, but I haven't needed that option yet.

More simply, omit the count argument to repeat indefinitely::

    $ repeat python -c "print 2+2"
    repeat: Repeating ['python', '-c', 'print 2+2'] forever.
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
    4
    repeat: Run 4 completed.
    repeat: Starting run 5.
    <and so on>

You can also explicitly request indefinite repetitions with a count of
``forever``.  In the unlikely case that your command starts with an integer,
you'll *need* to use ``forever`` to avoid the beginning of the command being
interpreted as a count::

    $ repeat forever 999 ...

This of course also means that in the equally unlikely event that your command
happens to start with ``forever``, you'll *also* need to use ``forever``::

    $ repeat forever forever ....

To silence the progress output, use the ``-q`` option::

    $ repeat -q 3 python -c "print 2+2"
    4
    4
    4


Usage
-----

Type ``repeat --help`` to see options::

    $ repeat --help
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

    git clone git@github.com:mdickinson/repeat.git repeat
    cd repeat
    python setup.py develop

**repeat** runs on Python 2 (version 2.6 or later) and on Python 3 (version 3.2
or later).  It depends on the ``six`` package.  For Python 2.6, it also depends
on the PyPI version of ``argparse``.


License
-------

The **repeat** script is copyright (c) 2014 Mark Dickinson.

**repeat** is licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.  You may
obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed
under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
CONDITIONS OF ANY KIND, either express or implied.  See the License for the
specific language governing permissions and limitations under the License.
