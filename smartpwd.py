#!/usr/bin/python
"""Prints important pieces of cwd bound to a given number of characters."""

from __future__ import print_function

import os
import sys


def smartpwd(pwd, home, maxlen):
  """Modify pwd to show as much useful information as possible within maxlen."""
  SEPERATOR = ".../"
  if pwd.startswith(home):
    pwd = "~" + pwd[len(home):]
  if len(pwd) > maxlen:
    head, tail = os.path.split(pwd)  # /dir/eir/fir -> ("/dir/eir", "fir")
    available_space = max(0, maxlen - len(tail) - len(SEPERATOR))
    pwd = SEPERATOR.join([head[:available_space], tail])
  return pwd


def main():
  cwd, home = os.getcwd(), os.getenv("HOME", "")
  try:
    maxlen = int(os.getenv("PROMPT_LENGTH"))
  except TypeError:  # $PROMPT_LENGTH did not exist.
    maxlen = 40
  except ValueError:
    maxlen = 40  # $PROMPT_LENGTH exists, but isn't an int.
  finally:
    print(smartpwd(cwd, home, maxlen), end="")


if __name__ == "__main__":
  main()
