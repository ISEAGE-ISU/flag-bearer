import requests
import sys
import os


def plant(conf):
    api_url = "{}/api/{}".format(conf['iscore']['base_url'],
                                 conf['iscore']['api_version'])

    extras = conf.request_extras()
    resp = requests.get(api_url + "/user/show.json", **extras)
    if resp.status_code == 403:
        print("[!!] Unauthorized: Invalid authentication information")
        sys.exit(1)

    resp.raise_for_status()
    resp = resp.json()

    flag_url = api_url + "/flags.json"

    team = None
    red = resp['profile']['is_red']
    admin = resp['is_superuser']
    if red or admin:
        print("Which team do you want to get flags for?")
        try:
            team = int(input("> "))
            flag_url += "?team_number={}".format(team)
        except ValueError:
            print("Retreiving flags for all teams")

    resp = requests.get(flag_url, **extras)
    resp.raise_for_status()
    resp = resp.json()

    if team:
        resp = list(filter(lambda x: x['team_number'] == team, resp))
    flags = {i: x for i, x in enumerate(resp)}

    print("Pick the flag to place")
    for flag_id, flag in flags.items():
        # Admins can see both blue and red flags, tell them which is which
        if admin:
            print("{}. {} ({})".format(flag_id, flag['name'], flag['type']))
        else:
            print("{}. {}".format(flag_id, flag['name']))

    flag = int(input("> "))
    print()

    if flag not in flags:
        print("[!!] Invalid selection")
        sys.exit(1)

    flag = flags[flag]

    save = 'force_save' in conf['iscore'] if red or admin else True
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

