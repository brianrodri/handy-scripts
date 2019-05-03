#!/usr/bin/env python3
from dataclasses import dataclass
from email.mime.text import MIMEText
from getpass import getpass
from itertools import cycle
from random import shuffle
from smtplib import SMTP
from typing import Any, Iterable, List, Tuple
import sys


@dataclass
class Player():
    name: str
    email: str


def MakeRandomPairs(players):
    """Returns list of random pairs with exactly one cycle."""
    players = list(players)
    if not players:
        return []
    shuffle(players)
    rotated_players = cycle(players)
    next(rotated_players)  # Rotate by 1.
    return list(zip(players, rotated_players))


pairs = MakeRandomPairs([
    Player(name="Me", email="me@gmail.com"),
    Player(name="Her", email="her@gmail.com"),
    Player(name="Him", email="him@gmail.com"),
    Player(name="Them", email="them@gmail.com"),
    Player(name="Us", email="us@gmail.com"),
])

if '--send' in sys.argv[1:]:
    with SMTP('http://smtp.gmail.com:587') as server:
        server.ehlo(), server.starttls()
        mock_sender = input('Gmail address: ')
        server.login(mock_sender, getpass())
        for santa, santee in pairs:
            email = MIMEText(
                f'Yo {santa.name}, you got {santee.name}!')
            email['Subject'] = 'Secret Santa!'
            email['From'] = mock_sender
            email['To'] = santa.email
            server.send_message(email)
        print('Sent!')
else:
    for santa, santee in pairs:
        print(f'{santa.name} -> {santee.name}')
