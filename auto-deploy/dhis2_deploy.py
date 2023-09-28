import requests

from info import info
from config_types import DhisConfig, ZipConfig


class Dhis2Client:
    def __init__(self, config: DhisConfig):
        self.base_url = config.base_url
        self.auth = config.auth
        response = self.get_request('/api/me.json')
        assert response.ok
        info(f'Connection to {self.base_url} successful')

    def get_request(self, endpoint: str, data: dict = None):
        return requests.get(self.base_url + endpoint, headers={
            'Authorization': f'Basic {self.auth}'
        })

    def post_request(self, endpoint: str, data: dict = None):
        return requests.post(self.base_url + endpoint, headers={
            'Authorization': f'Basic {self.auth}',
            # 'Content-Type': 'multipart/form-data'
        }, files=data)

    def upload_app(self, config: ZipConfig):
        response = self.post_request('/api/apps', data={
            'file': open(config.path + config.filename, 'rb')
        })
        assert response.ok
        info(f'App {config.filename} uploaded.')