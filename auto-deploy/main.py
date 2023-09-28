from dhis2_deploy import Dhis2Client
from info import info, error
from github_upload import GithubClient
from colored import Style
import yaml

from config_types import GitConfig, DhisConfig, ZipConfig

config = 'console.yaml'
git_access_token = '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'


def get_info(filename):
    """Loads release info from console.yaml"""
    try:
        with open(filename, 'r') as file:
            config = yaml.safe_load(file)
            github = config['GithubRelease']
            dhis2 = config['Dhis2Server']
            zip = config['ZipFile']

            git = GitConfig(
                access_token=git_access_token,
                repository=github['Repository'],
                release_tag=github['ReleaseTag'],
            )
            dhis = DhisConfig(
                base_url=dhis2['BaseUrl'],
                auth=dhis2['Auth'],
            )
            zip = ZipConfig(
                filename=zip['Filename'],
                path=zip['Path'],
            )
            return git, dhis, zip
    except FileNotFoundError:
        error("console.yaml not found in current directory")


# init
git_config, dhis_config, zip_config = get_info(config)
info(f'Repository {Style.bold}{git_config.repository}{Style.reset}')

# upload to github
github = GithubClient(git_config)
github.get_release()
github.delete_asset()
github.upload_asset(zip_config)

# upload to dhis2
dhis2 = Dhis2Client(dhis_config)
dhis2.upload_app(zip_config)
