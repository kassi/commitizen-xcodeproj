import pytest
from src.commitizen_xcodeproj.xcodeproj_version_provider import XcodeprojVersionProvider
from commitizen.config.yaml_config import YAMLConfig
from commitizen.exceptions import InvalidConfigurationError
from unittest.mock import patch

import inspect
import pathlib

from pprint import pprint

pbxproj = inspect.cleandoc("""// !$*UTF8*$!
        {
                archiveVersion = 1;
                                MARKETING_VERSION = 1.2;
                            };
                            name = Debug;
                                MARKETING_VERSION = 1.2;
                            };
                            name = Release;
    """)

@pytest.fixture()
def mocker(mocker):
    mocker.patch("pathlib.Path.read_text", return_value = pbxproj)
    mocker.patch("pathlib.Path.glob", return_value = [pathlib.Path("A.xcodeproj/project.pbxproj")])
    yield mocker

def make_config(overwrite):
    yaml = YAMLConfig(data="---\ncommitizen:\n", path="dummy")
    yaml._settings['commitizen_xcodeproj'] = {}
    for key in overwrite:
        yaml._settings['commitizen_xcodeproj'][key] = overwrite[key]
    return yaml

class TestXcodeprojVersionProvider:
    def test_init_with_default(self):
        assert XcodeprojVersionProvider(make_config({})).config == { 'fill_missing': 'right' }

    def test_init_with_fill_missing_overwrite(self):
        assert XcodeprojVersionProvider(make_config({'fill_missing': 'left'})).config == { 'fill_missing': 'left' }

    def test_init_with_fill_missing_invalid(self):
        with pytest.raises(InvalidConfigurationError):
            XcodeprojVersionProvider(make_config({'fill_missing': 'invalid'}))

    def test_get_version_fill_right(self, mocker):
        assert XcodeprojVersionProvider(make_config({'fill_missing': 'right'})).get_version() == "1.2.0"

    def test_get_version_fill_left(self, mocker):
        assert XcodeprojVersionProvider(make_config({'fill_missing': 'left'})).get_version() == "0.1.2"

    def test_set_version(self, mocker):
        patcher = patch("pathlib.Path.write_text")
        mpatch = patcher.start()

        XcodeprojVersionProvider(make_config({})).set_version("4.5.6")

        mpatch.assert_called_once()
        mpatch.assert_called_with(inspect.cleandoc("""// !$*UTF8*$!
        {
                archiveVersion = 1;
                                MARKETING_VERSION = 4.5.6;
                            };
                            name = Debug;
                                MARKETING_VERSION = 4.5.6;
                            };
                            name = Release;
        """))
        patcher.stop()
