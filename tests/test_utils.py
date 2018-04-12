import vcr
import pytest

from argparse import Namespace

from flag_bearer import utils
from flag_bearer.config import Config


@pytest.fixture
def config():
    conf = Config.load(noflagrc=True)
    args = Namespace(api_token='32257d57fcae845fc89db97a0835c78b60fb8adb', iscore_url='http://localhost:8000', api_version=None, save=False)
    conf.merge(args)
    return conf


@vcr.use_cassette('fixtures/vcr_cassettes/user.yaml')
def test_user_profile(config):
    user = utils.get_user(config)

    assert user['is_superuser']
    assert user['username'] == 'admin'


@vcr.use_cassette('fixtures/vcr_cassettes/flags.yaml')
def test_get_flags(config):
    flags = utils.get_flags(config, team=3)

    print(flags)
    assert len(flags) > 0
    assert flags[0]['team_number'] == 3
    assert len(flags[0]['data']) == 50


def test_get_diff():
    side_a = "abc"
    side_b = "abd"
    diff = utils.get_diff(side_a, side_b)
    assert diff == "- abc+ abd"
