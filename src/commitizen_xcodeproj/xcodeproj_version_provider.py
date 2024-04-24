from commitizen.providers import VersionProvider
from commitizen.exceptions import InvalidConfigurationError
from deepmerge import always_merger
from pathlib import Path
import glob, re

from pprint import pprint

class XcodeprojVersionProvider(VersionProvider):
    file = None
    default_config = {
        'fill_missing': 'right'
    }
    config = {}
    search_re = r'(\s*)MARKETING_VERSION\s*=\s*(\d+(?:\.\d+)*);'

    def __init__(self, config):
        if 'commitizen_xcodeproj' in config._settings:
            self.config = always_merger.merge(self.default_config.copy(), config._settings['commitizen_xcodeproj'])

        self.__verify_config()

        for file in Path().glob("*.xcodeproj/project.pbxproj"):
            self.file = file
            break

    def get_version(self) -> str:
        """
        Reads a version string from the project.pbxproj file in the format
            MARKETING_VERSION = 1;
            MARKETING_VERSION = 1.2;
            MARKETING_VERSION = 1.2.3;

        Always returns 3 digit semver which is filled up with 0s either from left or right,
        depending on the `fill_missing` setting.
        """
        contents = self.file.read_text()
        match = re.search(self.search_re, contents)
        if match:
            version = match.group(2)
            v = version.split(".")
            while len(v) < 3:
                if self.config['fill_missing'] == 'right':
                    v.append("0")
                else:
                    v.insert(0, "0")
            return ".".join(v[0:3])

        return "0.0.0"

    def set_version(self, version: str):
        """
        Writes a new project.pbxproj replacing the version line.
        """
        old_content = self.file.read_text()
        new_content = re.sub(
            self.search_re,
            r'\1MARKETING_VERSION = %s;' % version,
            old_content
        )

        self.file.write_text(new_content)

    def __verify_config(self):
        allowed = [ 'left', 'right']
        if self.config['fill_missing'] not in allowed:
            raise InvalidConfigurationError(f"Filler for missing version specifier not one of {allowed}")
