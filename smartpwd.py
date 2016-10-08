#!/usr/bin/python
"""Prints important pieces of cwd bound to a given number of characters."""

from __future__ import print_function

import os
import sys


def smartpwd(pwd, home, maxlen):
  """Modify pwd to show as much useful information as possible within maxlen."""
  if home and pwd.startswith(home):
    pwd = "~" + pwd[len(home):]
  if len(pwd) > maxlen:
    finalbslash = pwd.rfind("/")
    if finalbslash != -1:
      finaldir = pwd[finalbslash+1:]
      pwd = pwd[:max(0, maxlen-len(finaldir)-4)] + ".../" + finaldir
  return pwd


def main():
  cwd = os.getcwd()
  home = os.getenv("HOME", "")

  try:
    maxlen = int(os.getenv("PROMPT_LENGTH"))
  except TypeError:  # $PROMPT_LENGTH did not exist.
    maxlen = 40
  except ValueError:
    maxlen = 40
    print("$PROMPT_LENGTH exists, but isn't an int.", file=sys.stderr)

  print(smartpwd(cwd, home, maxlen), end="")


if __name__ == "__main__":
  main()
