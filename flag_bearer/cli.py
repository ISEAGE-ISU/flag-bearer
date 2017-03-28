from argparse import ArgumentParser
from flag_bearer import __version__, actions


parser = ArgumentParser()
subparsers = parser.add_subparsers()


plant = subparsers.add_parser('plant')
plant.set_defaults(func=actions.plant)
plant.add_argument('-f', '--flag', help="The name of the flag to plant")


def main():
    print("Flag Bearer v{}".format(__version__))
    args = parser.parse_args()

    if not hasattr(args, 'func'):
        parser.print_help()
        return

    args.func(args)

