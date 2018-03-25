from __future__ import print_function

import sys

import paramiko
from six import BytesIO
from six.moves import input

from flag_bearer import utils


def plant(conf):
    """
    Remotely plant a flag.
    """
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
    data = flag['data']

    username = conf.cli_args.username
    host = conf.cli_args.host
    port = conf.cli_args.port
    location = conf.cli_args.location
    password = conf.cli_args.password

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, username=username, password=password, port=port)

    pkt = BytesIO()
    pkt.write(data.encode('utf-8'))
    pkt.write(b'\n')
    pkt.seek(0)

    sftp = ssh.open_sftp()
    sftp.putfo(pkt, location)
    print("Verifying flag plant")

    planted_contents = get_file_contents(ssh, location)

    if planted_contents != data:
        print("Planted flag data does not match, double check the plant")
    else:
        print("Flag Planted")


def get_file_contents(ssh, file):
    """
    Retrieve the contents of file from the remote server.

    This does ***NOT*** use SFTP since teams might disallow SFTP.
    """
    _, stdout, stderr = ssh.exec_command('cat {}'.format(file))
    err = stderr.read()
    if len(err) > 0:
        return False
    return stdout.read().decode('utf-8').strip()
