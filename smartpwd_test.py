#!/usr/bin/python
"""Tests for smartpwd."""

from __future__ import print_function

import unittest

from smartpwd import smartpwd


class SmartpwdTest(unittest.TestCase):

  def testJustHomeAsCwd(self):
    cwd = "/usr/home"
    home = "/usr/home"
    maxlen = 16

    actual = smartpwd(cwd, home, maxlen)
    expected = "~"

    self.assertEqual(expected, actual)

  def testJustHomeAsCwdButWithLongIntermediateDirectoryName(self):
    cwd = "/usr/home/reallylikeuneccesarilylongdirectoryname/shortdir1"
    home = "/usr/home"
    maxlen = 16

    actual = smartpwd(cwd, home, maxlen)
    expected = "~/r.../shortdir1"

    self.assertEqual(expected, actual)

  def testDirectoryThatFitsSnuggly(self):
    cwd = "/etc/shortdir1"
    home = ""  # Not used.
    maxlen = 16

    actual = smartpwd(cwd, home, maxlen)
    expected = cwd

    self.assertEqual(expected, actual)

  def testReallyLongInitialDirectory(self):
    cwd = "/reallylikeuneccesarliylongdirectoryname/shortdir1/shortdir2"
    home = ""  # Not used.
    maxlen = 16

    actual = smartpwd(cwd, home, maxlen)
    expected = "/re.../shortdir2"

    self.assertEqual(expected, actual)

  def testReallyLongFinalDirectory(self):
    cwd = "/shortdir1/shortdir2/reallylikeuneccesarliylongdirectoryname"
    home = ""  # Not used.
    maxlen = 16

    actual = smartpwd(cwd, home, maxlen)
    expected = ".../reallylikeuneccesarliylongdirectoryname"  # N.B. this is the
                                                              # only case where
    self.assertEqual(expected, actual)                        # we ignore
                                                              # maxlen.

  def testReallyLongIntermediateDirectory(self):
    cwd = "/shortdir1/reallylikeuneccesarliylongdirectoryname/shortdir2"
    home = ""  # Not used.
    maxlen = 16

    actual = smartpwd(cwd, home, maxlen)
    expected = "/sh.../shortdir2"

    self.assertEqual(expected, actual)


if __name__ == "__main__":
  unittest.main()
