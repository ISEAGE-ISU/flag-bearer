from __future__ import print_function
from argparse import ArgumentParser
from flag_bearer import __version__, actions, config


parser = ArgumentParser()
parser.add_argument('--iscore-url', help="IScorE base url", default=None)
parser.add_argument('--api-version', default='v1')
parser.add_argument('--api-token')
subparsers = parser.add_subparsers()


plant = subparsers.add_parser('plant')
plant.set_defaults(func=actions.plant)
plant.add_argument('-f', '--flag', help="The name of the flag to plant")
plant.add_argument('-l', '--location', help="The location to plant the flag")
plant.add_argument('-n', '--team', help="The team number")
plant.add_argument('-s', '--save', action='store_true', default=False, 
                   help="Force the flag to be downloaded")


plant = subparsers.add_parser('download', help="Download all the flags for a team")
plant.set_defaults(func=actions.download)

try:
    import paramiko
    from flag_bearer import remote as remote_actions
    remote = subparsers.add_parser('remote', help='Remotely plant flags')
    remote_sub = remote.add_subparsers()

    remote_plant = remote_sub.add_parser('plant')
    remote_plant.set_defaults(func=remote_actions.plant)
    remote_plant.add_argument('-H', '--host', help='The host to connect to')
    remote_plant.add_argument('-p', '--port', help='The port of the remote host', default=22)
    remote_plant.add_argument('-u', '--username', help='The user to connect with')
    remote_plant.add_argument('-P', '--password', help='Password to connect with')
    remote_plant.add_argument('-l', '--location', help="The location to plant the flag", required=True)
except ImportError:
    pass


def main():
    print("Flag Bearer v{}".format(__version__))
    args = parser.parse_args()

    if not hasattr(args, 'func'):
        parser.print_help()
        return

    conf = config.Config.load()
    conf.merge(args)
    args.func(conf)

