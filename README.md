# Commitizen Xcode Project Version Provider

A commitizen version provider for Xcode project files, which store the version in the `MARKETING_VERSION` field.

## Installation

    pip install commitizen-xcodeproj

## Usage

### Configuration

There are several ways to configure commitizen.
This example setup uses a local installation of commitizen via python and works  with `yaml` configuration files, but any other format as stated in the commitizen documentation works as well.

In your Xcode project root folder, create a `.cz.yaml`:

    ---
    commitizen:
      name: cz_conventional_commits
      tag_format: $version
      update_changelog_on_bump: true
      version_provider: "commitizen-xcodeproj"
      version_scheme: semver

Note: it's not necessary to include a `version` key inside the config file. Best practice is to keep the version in a single source of truth, which is the `project.pbxproj` file.

By default, short version numbers are filled with ".0" on the right,
thus 1.0 becoming 1.0.0. This can be configured:

    ---
    commitizen:
      commitizen_xcodeproj:
        fill_missing: left

will transform 1.0 to 0.1.0.

### Bumping versions

Now

    cz bump

will read the current version from `project.pbxproj`, increase it accordingly and write it back to the same file to both, the _Debug_ and the _Release_ version.

## Contribution

Contributions, issues and feature requests are welcome.
For major changes, please open an issue first to discuss what you would like to change.

- Fork the project
- Clone the fork
- Add your changes and update tests as appropriate.
- Create a pull request

## License

This project is [MIT](LICENSE) licensed.
