'repeat' is a dirt simple Python script to repeat a command
indefinitely, or for a fixed number of iterations.  I wrote
it because I got bored of writing::

    for ($i = 0; $i -lt 100; $i++) do { stuff; }

repeatedly in PowerShell, while trying to provoke threading-related
race conditions in test code.

Example usage::

    PS C:\Users\mdickinson\Desktop> repeat -n 3 python -c "print 2+2"
    Starting run 0.
    4
    Run 0 completed.
    Starting run 1.
    4
    Run 1 completed.
    Starting run 2.
    4
    Run 2 completed.

Or even more simply, omit the count to repeat indefinitely::

    PS C:\Users\mdickinson\Desktop> repeat -n 3 python -c "print 2+2"
    Starting run 0.
    4
    Run 0 completed.
    Starting run 1.
    4
    Run 1 completed.
    Starting run 2.
    4
    Run 2 completed.
    Starting run 3.
    4
    Run 3 completed.
    Starting run 4.
    4
    Run 4 completed.
    Starting run 5.
    4
    Run 5 completed.
    Starting run 6.
    4
    Run 6 completed.
    Starting run 7.
    4
    Run 7 completed.
