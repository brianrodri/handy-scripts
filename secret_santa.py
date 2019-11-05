#!/usr/bin/env python3
import dataclasses
import email
import getpass
import itertools
import random
import smtplib
import sys


def MakeRandomPairs(items):
    """Returns a list of random pairs making exactly one cycle through items."""
    items = list(items)
    random.shuffle(items)
    rotated_items = itertools.cycle(items)
    _ = next(rotated_items, None)
    return list(zip(items, rotated_items))


@dataclasses.dataclass(frozen=True)
class Player():
    name: str
    email_address: str


def main():
    player_pairs = MakeRandomPairs([
        Player(name="Me", email_address="me@gmail.com"),
        Player(name="Her", email_address="her@gmail.com"),
        Player(name="Him", email_address="him@gmail.com"),
        Player(name="Them", email_address="them@gmail.com"),
        Player(name="Us", email_address="us@gmail.com"),
    ])

    if '--send' in sys.argv[1:]:
        with smtplib.SMTP('smtp.gmail.com:587') as server:
            server.starttls()  # GMail requires TLS encryption.
            sender_gmail_address = input('GMail address: ')
            server.login(sender_gmail_address, getpass.getpass())
            for santa, santee in player_pairs:
                message = email.message.EmailMessage()
                message.set_content(f'Yo {santa.name}, you got {santee.name}!')
                message['Subject'] = 'Secret Santa!'
                message['From'] = sender_gmail_address
                message['To'] = santa.email_address
                server.send_message(message)
        print('Sent!')
    else:
        for santa, santee in player_pairs:
            print(f'{santa.name} -> {santee.name}')


if __name__ == '__main__':
    main()
