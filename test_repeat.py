from __future__ import unicode_literals

import io
import subprocess
import sys
import unittest

if sys.version_info >= (3, 3):
    import unittest.mock as mock
else:
    import mock

import repeat


class MockCheckCall(object):
    def __init__(self, returncodes):
        self.returncodes = iter(returncodes)

    def __call__(self, cmd):
        returncode = next(self.returncodes)
        if returncode == 0:
            return 0
        else:
            raise subprocess.CalledProcessError(
                returncode=returncode,
                cmd=cmd,
            )


class TestRepeat(unittest.TestCase):
    """
    Tests for the 'repeat' function.

    """
    def setUp(self):
        self.mock_stdout = io.StringIO()
        self.mock_cmd = ["do", "something"]

    def tearDown(self):
        pass

    def test_repeat_ten_times(self):
        with mock.patch('repeat.subprocess.check_call') as m:
            returncode = repeat.repeat(
                self.mock_cmd, count=10, progress_stream=self.mock_stdout)
        self.assertEqual(returncode, 0)
        self.assertEqual(m.call_count, 10)
        for args, kwargs in m.call_args_list:
            self.assertEqual(len(args), 1)
            self.assertEqual(args[0], self.mock_cmd)
            self.assertFalse(kwargs)

    def test_repeat_zero_times(self):
        with mock.patch('repeat.subprocess.check_call') as m:
            returncode = repeat.repeat(
                self.mock_cmd, count=0, progress_stream=self.mock_stdout)
        self.assertEqual(returncode, 0)
        self.assertFalse(m.called)

    def test_abort_on_failure(self):
        with mock.patch('repeat.subprocess.check_call') as m:
            m.side_effect = MockCheckCall(returncodes=[0, 7])
            returncode = repeat.repeat(
                self.mock_cmd, count=10, progress_stream=self.mock_stdout)
        self.assertEqual(returncode, 7)
        self.assertEqual(m.call_count, 2)
