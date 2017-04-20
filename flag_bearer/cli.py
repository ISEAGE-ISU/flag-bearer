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


def main():
    print("Flag Bearer v{}".format(__version__))
    args = parser.parse_args()

    if not hasattr(args, 'func'):
        parser.print_help()
        return

    conf = config.Config.load()
    conf.merge(args)
    args.func(conf)

