#!/usr/bin/env  python3

#Copyright (c) 2016-2019 Carlos Millett
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.


import argparse
import configparser
from os import environ
from re import findall
from pathlib import Path

import transmissionrpc
from pydbus import SessionBus


class Config():
    def __init__(self, server='localhost', port='9091', user=None, passw=None):
        self._server = server
        self._port = port
        self._user = user
        self._passw = passw

    @property
    def server(self):
        return self._server

    @property
    def port(self):
        return self._port

    @property
    def user(self):
        return self._user

    @property
    def passwd(self):
        return self._passwd


def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-p',
        '--profile',
        type=str,
        default='default',
        help='Define profile to read from config file.'
    )
    parser.add_argument(
        '-n',
        '--notify',
        action='store_true',
        help='Use Desktop Notification for output.'
    )
    parser.add_argument(
        'torrent',
        metavar='TORRENT',
        type=str,
        help='torrent/magnet link to add to transmission.'
    )
    return parser


def conf(profile):
    configPath = Path(
        environ.get('XDG_CONFIG_HOME', '~/.config')
    ).expanduser()
    configPath = configPath / 'addtorrent.conf'

    configFile = configparser.ConfigParser()
    configFile.read(configPath)

    opts = Config(
        configFile.get(profile, 'SERVER', fallback='localhost'),
        configFile.get(profile, 'PORT', fallback='9091'),
        configFile.get(profile, 'USER', fallback=None),
        configFile.get(profile, 'PASSW', fallback=None),
    )
    return opts


def main():
    parser = cli()
    args = parser.parse_args()
    opts = conf(args.profile)

    try:
        transmission = transmissionrpc.Client(
            opts.server,
            opts.port,
            opts.user,
            opts.passw
        )
        torrent = transmission.add_torrent(args.torrent)

    except transmissionrpc.error.TransmissionError as err:
        if 'Request' in err.message:
            summary = 'Connection'
            text = err.message

        else:
            summary = 'Error'
            text = findall('"(.*)"', err.message)[0]

    else:
        summary = 'Added'
        text = torrent.name

    finally:
        if args.notify:
            bus = SessionBus()
            bubble = bus.get('.Notifications')
            bubble.Notify(
                'Torrent',
                0,
                'message-email',
                summary,
                text,
                [],
                {},
                -1
            )

        else:
            print('{}: {}'.format(summary, text))


if __name__ == '__main__':
    main()
