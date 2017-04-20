from configparser import ConfigParser
from os.path import expanduser, dirname, join, exists
import getpass

ROOT = dirname(__file__)


class Config(ConfigParser):
    @classmethod
    def load(cls):
        # Load configuration files in order
        # - default.ini
        # - ~/.flagrc
        conf = cls()
        conf.read(join(ROOT, 'default.ini'))
        
        flagrc = join(expanduser('~'), '.flagrc')
        print("Loading {}".format(flagrc))
        if exists(flagrc):
            print("Loading")
            conf.read(flagrc)

        return conf

    def merge(self, args):
        """
        Merge the configuration files with parsed arguments.
        """

        if args.iscore_url:
            self['iscore']['base_url'] = args.iscore_url

        if args.api_version:
            self['iscore']['api_version'] = args.api_version

        self.credentials = None
        if args.api_token:
            self.api_token = args.api_token
        else:
            print("Enter your IScorE API Token (leave blank to use your credentials)")
            self.api_token = input("> ")

            if not self.api_token:
                print()
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
