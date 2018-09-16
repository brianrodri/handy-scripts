#!/usr/bin/env python3
"""Provides a "truly random" set of pairings for secret santa players.

Run with '--send' to send emails about designations to each player.
"""
from collections import namedtuple
from email.mime.text import MIMEText
from getpass import getpass

import itertools
import random
import smtplib
import sys


def MakeRandomPairings(items):
    """Return random list of pairs such that items appear once on each side.

    Items are never paired with themselves, unless only one item is present.

    Example:
        >>> MakeRandomPairings([1, 2, 3])
        ... [(2, 1), (1, 3), (3, 2)]  # Possible outcome
        >>> [(3, 1), (1, 3), (2, 2)]  # Impossible outcome
    Args:
        items: iterable of anything.
    Returns:
        list of pairs such that each item appears once on both sides.
    """
    items = [i for i in items]  # Always create a new list of items.
    random.shuffle(items)
    items_iter = iter(items)
    offset_items_iter = itertools.cycle(items)
    _ = next(offset_items_iter)  # Drop first item to offset it from items_iter.
    return list(zip(items_iter, offset_items_iter))


Player = namedtuple('Player', 'name, email')
players = [
    Player(name='Brian', email='thatbrod@gmail.com'),
    Player(name='Rianb', email='dthatbro@gmail.com'),
    Player(name='Ianbr', email='odthatbr@gmail.com'),
]
if '--send' in sys.argv[1:]:
    with smtplib.SMTP('smtp.gmail.com:587') as server:
        server.ehlo(), server.starttls()  # Low-level connection stuff.
        email_sender = input('Gmail address: ')
        server.login(email_sender, getpass())
        for santa, santee in MakeRandomPairings(players):
            email = MIMEText(f'yo {santa.name}, you got {santee.name}.')
            email['Subject'] = 'Secret Santa 2018!'
            email['From'] = email_sender
            email['To'] = santa.email
            server.send_message(email)
        print('Sent')
else:
    for santa, santee in MakeRandomPairings(players):
        print(f'{santa.name} -> {santee.name}')
