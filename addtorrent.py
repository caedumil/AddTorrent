#!/usr/bin/env  python3

#Copyright (c) 2016-2018 Carlos Millett
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

import os
import re
import sys
import argparse
import configparser

import notify2
import transmissionrpc


parser = argparse.ArgumentParser()
parser.add_argument(
    "-p", "--profile", type=str, default="default",
    help="Define profile to read from config file."
)
parser.add_argument(
    "-n", "--notify", action="store_true",
    help="Use Desktop Notification for output."
)
parser.add_argument(
    "torrent", metavar="TORRENT", type=str,
    help="torrent/magnet link to add to transmission."
)
args = parser.parse_args()


config = os.environ.get("XDG_CONFIG_HOME")
if not config:
    config = os.path.expanduser("~/.config")

config = os.path.join(config, "addtorrent.conf")

opts = configparser.ConfigParser()
opts.read(config)

server = opts.get(args.profile, "SERVER", fallback="localhost")
port = opts.get(args.profile, "PORT", fallback="9091")
user = opts.get(args.profile, "USER", fallback=None)
passw = opts.get(args.profile, "PASSW", fallback=None)


try:
    transmission = transmissionrpc.Client(server, port, user, passw)

    torrent = transmission.add_torrent(args.torrent)
    summary = "Added"
    text = torrent.name

except transmissionrpc.error.TransmissionError as err:
    if "Request" in err.message:
        summary = "Connection"
        text = err.message

    else:
        summary = "Error"
        text = re.findall('"(.*)"', err.message)[0]

finally:
    if args.notify:
        notify2.init("Torrent")
        bubble = notify2.Notification(summary, text, "message-email")
        bubble.show()

    else:
        print("{}: {}".format(summary, text))
