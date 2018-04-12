from six.moves import input
from six.moves.configparser import ConfigParser
from os.path import expanduser, dirname, join, exists
import getpass

ROOT = dirname(__file__)


class Config(ConfigParser):
    cli_args = None

    @classmethod
    def load(cls, noflagrc=False):
        # Load configuration files in order
        # - default.ini
        # - /etc/flagrc
        # - ~/.flagrc
        conf = cls()
        conf.read(join(ROOT, 'default.ini'))
        conf.read('/etc/flagrc')

        # Skip loading the flagrc, only used in tests
        if noflagrc:
            return conf

        flagrc = join(expanduser('~'), '.flagrc')
        if exists(flagrc):
            print("Loading {}".format(flagrc))
            conf.read(flagrc)

        return conf

    def merge(self, args):
        """
        Merge the configuration files with parsed arguments.
        """
        # Keep a copy of the args for an action
        self.cli_args = args
        if not self.has_section('iscore'):
            self.add_section('iscore')

        if args.iscore_url:
            self.set('iscore', 'base_url', args.iscore_url)

        if args.api_version:
            self.set('iscore', 'api_version', args.api_version)

        if hasattr(args, 'save') and args.save:
            self.set('iscore', 'force_save', 'yes')

        self.credentials = None
        if args.api_token:
            self.api_token = args.api_token
        elif self.has_option('iscore', 'api_token'):
            self.api_token = self.get('iscore', 'api_token')
        else:
            print("Enter your IScorE API Token (leave blank to use your credentials)")
            self.api_token = input("> ")

            if not self.api_token:
                print("Please login using your IScorE credentials")
                username = input("Username: ")
                password = getpass.getpass()
                self.credentials = (username, password)

    def request_extras(self):
        """
        Get extra requests configuration, specifically about authentication.

        Example:
        >>> extras = config.request_extras()
        >>> requests.get(url, **extras)
        """
        conf = {}
        if self.api_token:
            conf['headers'] = {
                'Authorization': 'Token {}'.format(self.api_token),
            }

        if self.credentials:
            conf['auth'] = self.credentials

        return conf
