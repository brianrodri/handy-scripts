#! /usr/bin/python3
import random
import smtplib
import sys

from collections import defaultdict, namedtuple
from email.mime.text import MIMEText
from getpass import getpass
from itertools import combinations, groupby, product


def BijectionsOf(domain, codomain, relations):
  """Return the subsets of relations which create 1-to-1 mappings."""
  mapping = defaultdict(set)
  for x, y in relations:
    mapping[x].add(y)
  subsets = map(list, product(*mapping.values()))
  spanning_subsets = filter(lambda ys: len(set(ys)) == len(domain), subsets)
  return [tuple(zip(mapping.keys(), ys)) for ys in spanning_subsets]


Participant = namedtuple("Participant", "name, email")


def main():
  # Fetch input.
  members = set()
  print("Enter one participant per line in the format: \"name, e-mail\"")
  for line in sys.stdin.readlines():
    data = line.split(",", 1)
    name, email = data[0].strip(), data[1].strip()
    members.add(Participant(name, email))

  # Choose a random group of members.
  pairings = set(product(members, members)) - set(zip(members, members))
  try:
    group = random.choice(BijectionsOf(members, members, pairings))
  except ValueError:
    print("No matches.", file=sys.stderr)
    sys.exit()

  # Send out the e-mails.
  messenger, password = input("E-Mail: "), getpass()
  with smtplib.SMTP("smtp.gmail.com:587") as server:
    server.ehlo()
    server.starttls()
    server.login(messenger, password)
    subject = "Secret Santa 2016!"
    body = "Hey {} you got {}, and the spending limit this year is $40!"
    for santa, santee in group:
      msg = MIMEText(body.format(santa.name, santee.name))
      msg["Subject"] = subject
      msg["From"] = messenger
      msg["To"] = santa.email
      server.send_message(msg)
    print("Done.")


if __name__ == "__main__":
  main()
