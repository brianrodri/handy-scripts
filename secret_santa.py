#!/usr/bin/env python3
import collections
import dataclasses
import email.message
import getpass
import random
import smtplib
import sys


@dataclasses.dataclass
class Player():
    name: str
    email: str


def MakeRandomPairs(items):
    """Returns list of random item-pairs with exactly one cycle."""
    if not (items := list(items)):
        return []
    random.shuffle(items)
    rotated_items = collections.deque(items)
    rotated_items.rotate(1)
    return list(zip(items, rotated_items))


player_pairs = MakeRandomPairs([
    Player(name="Me", email="me@gmail.com"),
    Player(name="Her", email="her@gmail.com"),
    Player(name="Him", email="him@gmail.com"),
    Player(name="Them", email="them@gmail.com"),
    Player(name="Us", email="us@gmail.com"),
])

if '--send' in sys.argv[1:]:
    with smtplib.SMTP('smtp.gmail.com:587') as server:
        server.starttls()  # GMail requires TLS encryption.
        sender_gmail = input('GMail address: ')
        server.login(sender_gmail, getpass.getpass())
        for santa, santee in player_pairs:
            msg = message.EmailMessage()
            msg.set_content(f'Yo {santa.name}, you got {santee.name}!')
            msg['Subject'] = 'Secret Santa!'
            msg['From'] = sender_gmail
            msg['To'] = santa.email
            server.send_message(msg)
    print('Sent!')
else:
    for santa, santee in player_pairs:
        print(f'{santa.name} -> {santee.name}')
