from configparser import ConfigParser
from os import exists
from os.path import expanduser, dirname, join

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
        if exists(flagrc):
            conf.read(flagrc)

        return conf

