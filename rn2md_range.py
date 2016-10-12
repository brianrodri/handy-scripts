#!/usr/bin/env python3
"""Outputs a range of RedNotebook dates in Markdown format."""

from __future__ import print_function

import codecs
import datetime
import iterutils
import os
import re
import yaml

from rn2md import *


DATA_DIR = os.path.expanduser("~/.rednotebook/data")
FILE_PATTERN = re.compile(r'(\d{4})-(\d{2})\.txt$')
DATE_PATTERN = re.compile(r'(\d{4})-(\d{2})-(\d{2})')


def MakeDateFromFileMatch(m):
  year = int(m.group(1))
  month = int(m.group(2))
  assert month in range(1, 13)
  return datetime.date(year=year, month=month, day=1)


def MakeDateFromDateMatch(m):
  year = int(m.group(1))
  month = int(m.group(2))
  assert month in range(1, 13)
  day = int(m.group(3))
  assert day in range(1, 32)
  return datetime.date(year=year, month=month, day=day)


def ParseDateRanges(s):
  for matches in iterutils.grouper(2, DATE_PATTERN.finditer(s)):
    if not all(matches):
      raise StopIteration
    beg, end = sorted(map(MakeDateFromDateMatch, matches))
    yield beg, end


def ExpandDateRange(beg, end):
  span = end - beg
  for n in range(int(span.days) + 1):
    yield beg + datetime.timedelta(n)


def BuildMonthPaths():
  for file in sorted(os.listdir(DATA_DIR)):
    match = FILE_PATTERN.match(file)
    if match:
      path = os.path.join(DATA_DIR, file)
      yield (path, MakeDateFromFileMatch(match))


def LoadDaysFromPath(path, date):
  with codecs.open(path, "rb", encoding="utf-8") as month_file:
    contents = yaml.load(month_file, Loader=yaml.CLoader)
    return {date.replace(day=d): contents[d]["text"] for d in contents}


def BuildDailyLogDict():
  collection = dict()
  for month in (LoadDaysFromPath(*p) for p in BuildMonthPaths()):
    collection.update(month)
  return collection


def FormatDay(day, database):
  rn2md = ComposeLeft(TranslateHeaders(padding=1), TranslateImages(),
                      TranslateLinks(), TranslateItalics(), TranslateLists(),
                      TranslateStrikethroughs(), EscapeInnerUnderscores())
  head = day.strftime("%b %d, %Y")
  body = map(lambda line: line.rstrip(), database[day].split("\n"))
  formatted_head = "# " + head
  formatted_body = "\n".join(map(rn2md, body))
  if formatted_body:
    return formatted_head + "\n" + formatted_body
  else:
    return formatted_head


def main():
  database = BuildDailyLogDict()
  for beg, end in ParseDateRanges(sys.stdin.read()):
    relevant_days = (d for d in ExpandDateRange(beg, end) if d in database)
    print("\n\n\n".join(FormatDay(day, database) for day in relevant_days))


if __name__ == '__main__':
  main()
