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

    red = resp['profile']['is_red']
    if red:
        print("Which team do you want to get flags for?")
        team = int(input("> "))
        flag_url += "?team_number={}".format(team)

    resp = requests.get(flag_url, **extras)
    resp.raise_for_status()
    resp = resp.json()

    flags = {x['id']: x for x in resp}

    print("Pick the flag to place")
    for flag_id, flag in flags.items():
        print("{}. {}".format(flag_id, flag['name']))

    flag = int(input("> "))
    print()

    if flag not in flags:
        print("[!!] Invalid selection")
        sys.exit(1)

    flag = flags[flag]

    print("Where should I put the flag?")
    location = input("(./) > ")

    if not location:
        location = "./"

    print("Placing {} flag in {}".format(flag['name'], location))
    with open(os.path.join(location, flag['filename']), 'w') as fp:
        fp.write(flag['data'])
        fp.write("\n")

