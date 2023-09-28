from console import info
from github import github_client
from colored import Style

tag = 'test'
repo = 'pepfar-datim/erb-processor-json'
token = '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'

filename = 'ERB-Processor.zip'

info(f'Repo {Style.bold}{repo}{Style.reset}')

gh = github_client(repo=repo, release_tag=tag, access_token=token)
gh.get_release()
gh.delete_asset()
gh.upload_asset(filename)