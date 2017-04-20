from flag_bearer.config import Config
from argparse import Namespace

def test_load():
    c = Config.load(noflagrc=True)
    assert c.get('iscore', 'api_version') == 'v1'
    assert c.get('iscore', 'base_url') == 'https://iscore.iseage.org'


def test_merge():
    c = Config.load(noflagrc=True)

    args = Namespace(api_token='abcd', iscore_url=None, api_version=None, save=False)

    c.merge(args)
    assert c.api_token == 'abcd'
    assert c.get('iscore', 'base_url') == 'https://iscore.iseage.org'
    assert c.get('iscore', 'api_version') == 'v1'
    assert not c.has_option('iscore', 'force_save')


def test_extras():
    c = Config.load(noflagrc=True)
    args = Namespace(api_token='abcd', iscore_url=None, api_version=None, save=False)
    c.merge(args)

    extras = c.request_extras()

    assert 'Authorization' in extras['headers']
    assert extras['headers']['Authorization'] == 'Token abcd'

