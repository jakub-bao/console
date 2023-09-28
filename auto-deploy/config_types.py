from collections import namedtuple

GitConfig = namedtuple('GitConfig', [
    'access_token',
    'repository',
    'release_tag',
])
DhisConfig = namedtuple('DhisConfig', [
    'base_url',
    'auth',
])
ZipConfig = namedtuple('ZipConfig', [
    'filename',
    'path',
])