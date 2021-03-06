import json
import os


class Settings(dict):
    """
    Settings of bot
    """

    def __init__(self, settings_path):
        self._path = settings_path
        if os.path.isfile(self._path):
            with open(self._path, 'rt') as fl:
                data = fl.read()
            settings = json.loads(data)
            super().__init__(settings)
            self.upgrade()
        else:
            super().__init__(Settings.get_default_settings())
            self.save()

    @staticmethod
    def get_default_settings():
        """
        Default bot settings
        """
        return {
            'ipv6_enabled': True,
            'udp_enabled': True,
            'proxy_type': 0,
            'proxy_host': '127.0.0.1',
            'proxy_port': 9050,
            'start_port': 0,
            'end_port': 0,
            'tcp_port': 0,
            'download_nodes': False,
            'auto_rights': 'user',
            'users': {},
            "ban": {
                "nicks": [],
                "public_keys": []
            }
        }

    def upgrade(self):
        default = Settings.get_default_settings()
        for key in default:
            if key not in self:
                print(key)
                self[key] = default[key]
        self.save()

    def save(self):
        text = json.dumps(self)
        with open(self._path, 'wt') as fl:
            fl.write(text)
