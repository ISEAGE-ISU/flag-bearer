from __future__ import print_function

import os
import sys

from six.moves import input

from flag_bearer import utils


def plant(conf):
    resp = utils.get_user(conf)

    team = None
    red = resp['profile']['is_red']
    admin = resp['is_superuser']
    if red or admin:
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
    if save or (not red and not admin):
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
    resp = utils.get_user(conf)

    team = None
    red = resp['profile']['is_red']
    admin = resp['is_superuser']
    if red or admin:
        print("Which team to you want to download flags for (blank for all)?")
        try:
            team = int(input("> "))
        except ValueError:
            print("Retreiving flags for all teams")

    resp = utils.get_flags(conf, team)
    flags = {i: x for i, x in enumerate(resp)}
    utils.save_flags(flags)
    print("Flags saved")

