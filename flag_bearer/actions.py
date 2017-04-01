import requests
import sys


def plant(args):
    api_url = "{}/api/{}".format(args.iscore_url, args.api_version)

    if not args.api_token:
        print("Enter Your IScorE API Key")
        api_key = input("> ")
        print()
    else:
        api_key = args.api_token

    resp = requests.get(api_url + "/flags.json", headers={'Authorization': 'Token ' + api_key})
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
    with open(flag['filename'], 'w') as fp:
        fp.write(flag['data'])

