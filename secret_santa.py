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
class Participant():
    name: str
    email_address: str


def main():
    matches = MakeRandomPairs([
        Participant(name='Me', email_address='me@gmail.com'),
        Participant(name='Her', email_address='her@gmail.com'),
        Participant(name='Him', email_address='him@gmail.com'),
        Participant(name='Them', email_address='them@gmail.com'),
        Participant(name='Us', email_address='us@gmail.com'),
    ])

    if '--send' in sys.argv[1:]:
        with smtplib.SMTP('smtp.gmail.com:587') as server:
            server.starttls()  # Gmail requires TLS encryption.
            sender_gmail_address = input('Gmail address: ')
            server.login(sender_gmail_address, getpass.getpass())
            for santa, santee in matches:
                message = email.message.EmailMessage()
                message.set_content(f'Yo {santa.name}, you got {santee.name}!')
                message['subject'] = 'Secret Santa!'
                message['from'] = sender_gmail_address
                message['to'] = santa.email_address
                server.send_message(message)
        print('Done!')
    else:
        for santa, santee in matches:
            print(f'{santa.name} -> {santee.name}')


if __name__ == '__main__':
    main()
