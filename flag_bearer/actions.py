from __future__ import print_function
from six.moves import input
import requests
import sys
import os

from flag_bearer import utils


def plant(conf):
    user = utils.get_user(conf)

    team = None
    if utils.user_is_red(user):
        print("Which team do you want to get flags for?")
        try:
            team = int(input("> "))
        except ValueError:
            print("Retreiving flags for all teams")

    resp = utils.get_flags(conf, team)
    flags = {i: x for i, x in enumerate(resp)}

    print("Pick the flag to place")
    for flag_id, flag in flags.items():
        # Admins can see both blue and red flags, tell them which is which
        if admin:
            print("{}. {} ({})".format(flag_id, flag['name'], flag['type']))
        else:
            print("{}. {}".format(flag_id, flag['name']))

    flag = int(input("> "))

    if flag not in flags:
        print("[!!] Invalid selection")
        sys.exit(1)

    flag = flags[flag]

    save = conf.has_option('iscore', 'force_save') if red or admin else True
    if save or (not utils.user_is_red(user)):
        print("Where should I put the flag?")
        location = input("(./) > ")

        if not location:
            location = "./"

        print("Placing {} flag in {}".format(flag['name'], location))
        with open(os.path.join(location, flag['filename']), 'w') as fp:
            fp.write(flag['data'])
            fp.write("\n")
    else:
        print("Flag: {}".format(flag['data']))


def download(conf):
    user = utils.get_user(conf)

    team = None
    if utils.user_is_red(user):
        print("Which team to you want to download flags for (blank for all)?")
        try:
            team = int(input("> "))
        except ValueError:
            print("Retreiving flags for all teams")

    resp = utils.get_flags(conf, team)
    flags = {i: x for i, x in enumerate(resp)}
    utils.save_flags(flags)
    print("Flags saved")


def verify(conf):
    user = utils.get_user(conf)

    if not utils.user_is_red(user):
        print("[!] This command is only available to Red Teamers")
