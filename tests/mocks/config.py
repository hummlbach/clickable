from clickable.config import Config
from unittest.mock import Mock


class ConfigMock(Config):
    def __init__(self, *args, **kwargs):
        super().__init__(Mock(), clickable_version='0.0.0', *args, **kwargs)
        self.cwd = '/tmp'
        self.config['build_dir'] = '/tmp/build'
        self.temp = '/tmp/build/tmp'

    def load_json_config(self, *args):
        return {}

    def load_env_config(self):
        return {}

    def load_arg_config(self, *args):
        return {}

    def find_manifest(self, *args):
        return '/fake/manifest.json'

    def get_manifest(self):
        return {
            'version': '1.2.3',
            'name': 'foo.bar',
            'hooks': {
                'foo': {
                    'desktop': '/fake/foo.desktop',
                },
            },
        }

    def get_template(self):
        return self.PURE
