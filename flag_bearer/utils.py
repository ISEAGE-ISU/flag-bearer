import requests
import sys


def get_api_url(conf):
    return "{}/api/{}".format(conf.get('iscore', 'base_url'),
                              conf.get('iscore', 'api_version'))


def get_user(conf):
    api_url = get_api_url(conf)
    extras = conf.request_extras()
    resp = requests.get(api_url + "/user/show.json", **extras)
    if resp.status_code == 403:
        print("[!!] Unauthorized: Invalid authentication information")
        sys.exit(1)

    resp.raise_for_status()
    resp = resp.json()

    return resp


def get_flags(conf, team=None):
    api_url = get_api_url(conf)
    extras = conf.request_extras()

    url = api_url + '/flags.json'

    if team:
        url += "?team_number={}".format(team)

    resp = requests.get(url, **extras)
    resp.raise_for_status()
    resp = resp.json()

    if team:
        resp = list(filter(lambda x: x['team_number'] == team, resp))

    return resp
