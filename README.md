# AddTorrent

Script to add torrents to transmission-daemon.
Can handle \*.torrent files or magnet links

## Requires

* python 3
* python-pydbus
* python-bencodepy
* python-transmissionrpc

## Usage

    addtorrent [-h] [-p PROFILE] [-n] <TORRENT>

* `-h`, `--help` help message
* `-p`, `--profile` profile to use from config file
* `-n`, `--notify` use Desktop Notificaton to display messages
* TORRENT file or magnet link

## Configuration file

This script will look for the config file on `$XDG_CONFIG_HOME` or `~/.config`
it the former is not defined.

A section is defined by a name between square brackets and four variables:

    [default]
    SERVER
    PORT
    USER
    PASSW

Set the variables you need to connect to transmission.

More profiles can be added, following the same structure. To make the script
connect using a different profile, use the switch `-p`.
