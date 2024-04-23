import pytest
from src.commitizen_xcodeproj.xcodeproj_version_provider import XcodeprojVersionProvider
from unittest.mock import patch

import inspect
import pathlib

pbxproj = inspect.cleandoc("""// !$*UTF8*$!
        {
                archiveVersion = 1;
                                MARKETING_VERSION = 1.0;
                            };
                            name = Debug;
                                MARKETING_VERSION = 1.0;
                            };
                            name = Release;
    """)

@pytest.fixture()
def mocker(mocker):
    mocker.patch("pathlib.Path.read_text", return_value = pbxproj)
    mocker.patch("pathlib.Path.glob", return_value = [pathlib.Path("A.xcodeproj/project.pbxproj")])
    yield mocker

class TestXcodeprojVersionProvider:
    def test_get_version(self, mocker):
        assert XcodeprojVersionProvider({}).get_version() == "1.0.0"

    def test_set_version(self, mocker):
        patcher = patch("pathlib.Path.write_text")
        mpatch = patcher.start()

        XcodeprojVersionProvider({}).set_version("4.5.6")

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
