#!/usr/bin/env python3
import random
import smtplib
import sys

from collections import defaultdict, namedtuple
from email.mime.text import MIMEText
from getpass import getpass
from itertools import combinations, groupby, product


def BijectionsOf(domain, codomain=None, relations=None):
  """Return all subsets of relations which create 1-to-1 mappings."""
  if codomain is None:
    codomain = domain
  if relations is None:
    relations = set(product(domain, codomain))
    if codomain is domain:
      relations -= set(zip(domain, domain))
  elif not all(x in domain and y in codomain for x, y in relations):
    raise ValueError("relations contains an undefined pair.")

  mapping = defaultdict(set)
  for x, y in relations:
    mapping[x].add(y)
  for ys in product(*mapping.values()):
    if len(set(ys)) == len(domain):
      yield tuple(zip(mapping.keys()))


def main():
  # Fetch input.
  Participant = namedtuple("Participant", "name, email")
  members = set()
  print("Enter one participant per line w/ the format: \"name, e-mail\"")
  for line in sys.stdin.readlines():
    data = line.split(",", 1)
    name, email = data[0].strip(), data[1].strip()
    members.add(Participant(name, email))

  # Choose a random group of members.
  try:
    group = random.choice(BijectionsOf(members))
  except ValueError:
    print("No matches.", file=sys.stderr)
    sys.exit()

  # Send out the e-mails.
  subject = "Secret Santa 2016!"
  body = "Hey {} you got {}, and the spending limit this year is $40!"
  messenger, password = input("E-Mail: "), getpass()
  with smtplib.SMTP("smtp.gmail.com:587") as server:
    server.ehlo()
    server.starttls()
    server.login(messenger, password)
    for santa, santee in group:
      msg = MIMEText(body.format(santa.name, santee.name))
      msg["Subject"] = subject
      msg["From"] = messenger
      msg["To"] = santa.email
      server.send_message(msg)
  print("Done.")


if __name__ == "__main__":
  main()
