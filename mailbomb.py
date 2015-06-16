#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""A simple script to send a lot of emails."""

import csv
import os
import smtplib
import string
import sys


TEMPLATE = 'From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n%s'
SUBJECT = 'mailbomb.py'
BODY = '''Dear %s,

[...]

In faith,
%s'''
AUTHOR = 'Bar Foo'


class DebugCredentials(object):

    """Dummy debug credentials."""

    def __init__(self):
        """Nothing to do."""
        pass

    @property
    def email(self):
        """Return an email from the credentials."""
        return 'bar.foo@example.com'


class DebugServer(object):

    """Dummy debug server."""

    def __init__(self, credentials):
        """Nothing to do."""
        pass

    def login(self):
        """Nothing to do."""
        pass

    def send(self, address, message):
        """Print the message to stdout."""
        print message

    def close(self):
        """Nothing to do."""
        pass


class MissingGoogleCredentials(RuntimeError):

    """Represent missing Google Credentials."""

    pass


class GoogleCredentials(object):

    """Wrap Google credentials in an object."""

    def __init__(self):
        """Read credentials from the environment.

        If this fails, die with an informative error.
        """
        try:
            self.username = os.environ['GMAIL_USERNAME']
            self.password = os.environ['GMAIL_PASSWORD']
        except KeyError:
            raise MissingGoogleCredentials('Add your Gmail username and ' +
                                           'password to the environment ' +
                                           'as GMAIL_USERNAME and ' +
                                           'GMAIL_PASSWORD.')

    @property
    def email(self):
        """Return email from the wrapped username."""
        return self.username + '@gmail.com'


class GoogleServer(object):

    """Wrap Google Server in an object."""

    def __init__(self, credentials):
        """Store credentials and create SMTP server."""
        self.credentials = credentials
        self.server = smtplib.SMTP_SSL('smtp.gmail.com', 465)

    def login(self):
        """Open server connection."""
        self.server.login(self.credentials.username, self.credentials.password)

    def send(self, address, message):
        """Send the message to the address, using the stored credentials."""
        self.server.sendmail(self.credentials.email, address, message)

    def close(self):
        """Close server connection."""
        self.server.close()


def compose(credentials, data):
    """Compose email from template."""
    subject = SUBJECT
    author = AUTHOR
    body = BODY % (string.capwords(data['name']), author)

    return TEMPLATE % (credentials.email, data['email'], subject, body)


def main():
    """Example usage of the provided classes and methods."""
    if len(sys.argv) != 2:
        raise RuntimeError('Usage: python mailbomb.py file.csv')

    credentials = DebugCredentials()
    server = DebugServer(credentials)

    with open(sys.argv[1]) as f:
        header = f.readline().strip().split(',')
        reader = csv.DictReader(f, header)

        for row in reader:
            email = row['email']
            if email:
                server.send(email, compose(credentials, row))

    server.close()


if __name__ == '__main__':
    main()
