from pathlib import Path
from commitizen.providers import VersionProvider
import glob, re

class XcodeprojVersionProvider(VersionProvider):
    file = None
    search_re = r'(\s*)MARKETING_VERSION\s*=\s*(\d+(?:\.\d+)*);'

    def __init__(self, config):
        for file in Path().glob("*.xcodeproj/project.pbxproj"):
            self.file = file
            break

    def get_version(self) -> str:
        """
        Reads a version string from the project.pbxproj file in the format
            MARKETING_VERSION = 1;
            MARKETING_VERSION = 1.2;
            MARKETING_VERSION = 1.2.3;

        Always returns 3 digit semver.
        """
        contents = self.file.read_text()
        match = re.search(self.search_re, contents)
        if match:
            version = match.group(2)
            v = version.split(".")
            while len(v) < 3:
                v.append("0")
            return ".".join(v[0:3])

        return ""

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
