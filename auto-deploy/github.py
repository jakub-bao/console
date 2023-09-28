import requests
from console import info
from colored import Style


class github_client:
    def __init__(self, repo: str, release_tag: str, access_token: str):
        self.repo = repo
        self.release_tag = release_tag
        self.access_token = access_token
        self.release = None

    def get_release(self) -> dict:
        response = requests.get(
            f'https://api.github.com/repos/{self.repo}/releases/tags/{self.release_tag}',
            headers={
                'Authorization': f'Bearer {self.access_token}'
            }
        )
        assert(response.status_code == 200)
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
        assert(response.status_code == 204)
        info(f'Asset {Style.bold}{asset["name"]}{Style.reset} from {asset["updated_at"]} deleted.')

    def upload_asset(self, filename: str) -> None:
        """Uploads a file to a release."""
        response = requests.post(
            f'https://uploads.github.com/repos/{self.repo}/releases/{self.release["id"]}/assets?name={filename}',
            headers={
                'Authorization': f'Bearer {self.access_token}',
                'Content-Type': 'application/octet-stream',
            },
            data=open(filename, 'rb')
        )
        assert(response.status_code == 201)
        info(f'Asset {Style.bold}{filename}{Style.reset} uploaded.')

