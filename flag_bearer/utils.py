import difflib
import requests
import sys
import zipfile


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


def save_flags(flags, team=None):
    if team:
        filename = "team_{}_flags.zip".format(team)
    else:
        filename = "all_team_flags.zip"

    z = zipfile.ZipFile(filename, 'a', compression=zipfile.ZIP_DEFLATED)

    for flag in flags.values():
        flag['data'] += '\n'
        z.writestr(flag['filename'], flag['data'])

    for zipped_file in z.filelist:
        zipped_file.create_system = 0
    z.close()


def get_diff(planted, actual):
    diff = difflib.ndiff([planted], [actual])
    return ''.join(diff)
