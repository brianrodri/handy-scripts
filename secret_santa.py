#!/usr/bin/env python3
"""Provides a "truly random" set of pairings for secret santa players.

Run this script with `--send` to send emails about designations to each player.
"""
from email.mime.text import MIMEText
from getpass import getpass
from typing import Any, Iterable, List, Tuple

import collections
import itertools
import random
import smtplib
import sys


def MakeRandomPairings(items: Iterable[Any]) -> List[Tuple[Any, Any]]:
    """Returns a list of random pairs which form a bijection on items to itself.

    The bijection is guaranteed to contain exactly one cycle.

    Example:
        >>> MakeRandomPairings([1, 2, 3, 4])
        ... [(2, 1), (1, 3), (3, 4), (4, 2)]  # Possible outcome
        >>> [(3, 2), (2, 3), (1, 4), (4, 1)]  # Impossible outcome
    """
    items = [i for i in items]  # Always create a new independent list of items.
    random.shuffle(items)
    items_iter = iter(items)
    offset_items_iter = itertools.cycle(items)
    _ = next(offset_items_iter)  # Drop first item to offset it from items_iter.
    return list(zip(items_iter, offset_items_iter))


Player = collections.namedtuple('Player', 'name, email')
players = [
    Player(name='Alan', email='alanchiu93@gmail.com'),
    Player(name='Antonette', email='hikkixlovesyou@gmail.com'),
    Player(name='Brian', email='thatbrod@gmail.com'),
    Player(name='Dan', email='Boogydaniel@aol.com'),
    Player(name='Mike', email='Mikechangg@yahoo.com'),
    Player(name='Sean', email='sean.han@brooklaw.edu'),
]
if '--send' in sys.argv[1:]:
    with smtplib.SMTP('smtp.gmail.com:587') as server:
        server.ehlo(), server.starttls()  # Low-level connection stuff.
        sending_address = input('Gmail address: ')
        server.login(sending_address, getpass())
        for santa, santee in MakeRandomPairings(players):
            email = MIMEText(f'yo {santa.name}, you got {santee.name}')
            email['Subject'] = 'Secret Santa 2018!'
            email['From'] = sending_address
            email['To'] = santa.email
            server.send_message(email)
        print('Sent')
else:
    for santa, santee in MakeRandomPairings(players):
        print(f'{santa.name} -> {santee.name}')
