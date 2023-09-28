import requests
from info import info
from colored import Style

from config_types import GitConfig, ZipConfig


class GithubClient:
    def __init__(self, config: GitConfig):
        self.repository = config.repository
        self.release_tag = config.release_tag
        self.access_token = config.access_token
        self.release = None

    def get_release(self) -> None:
        response = requests.get(
            f'https://api.github.com/repos/{self.repository}/releases/tags/{self.release_tag}',
            headers={
                'Authorization': f'Bearer {self.access_token}'
            }
        )
        assert response.ok
        info(f'Release {Style.bold}{self.release_tag}{Style.reset} found.')
        self.release = response.json()

    def delete_asset(self) -> None:
        """Deletes the first asset of a release."""
        assets = self.release['assets']
        if len(assets) == 0:
            info('No assets found.')
            return
        asset = assets[0]
        response = requests.delete(
            asset['url'],
            headers={
                'Authorization': f'Bearer {self.access_token}'
            }
        )
        assert response.ok
        info(f'Asset {Style.bold}{asset["name"]}{Style.reset} from {asset["updated_at"]} deleted.')

    def upload_asset(self, config: ZipConfig) -> None:
        """Uploads a file to a release."""
        response = requests.post(
            f'https://uploads.github.com/repos/{self.repository}/releases/{self.release["id"]}/assets?name={config.filename}',
            headers={
                'Authorization': f'Bearer {self.access_token}',
                'Content-Type': 'application/octet-stream',
            },
            data=open(config.path + config.filename, 'rb')
        )
        assert response.ok
        info(f'Asset {Style.bold}{config.filename}{Style.reset} uploaded.')

