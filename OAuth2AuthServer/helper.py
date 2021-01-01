from typing import Any, Dict, Union
import json


class ConfigurationSettingsBase(object):
    def __init__(self):
        pass

    def load_app_settings(self) -> Dict[str, str]:
        pass

    def load_connection_strings(self) -> Dict[str, str]:
        pass

    def load_all_strings(self) -> Dict[str, Union[str, Dict[str, str]]]:
        pass


class ConfigurationSettingsLocal(ConfigurationSettingsBase):
    def __init__(self, source: str, source_path: str = ''):
        self._source_path = source_path
        self._source = source
        with open(self._source_path + self._source) as fd:
            self._dict = json.load(fd)

    def load_app_settings(self) -> Dict[str, str]:
        pass

    def load_connection_strings(self) -> Dict[str, str]:
        pass

    def load_all_settings(self) -> Dict[str, Union[str, Dict[str, str]]]:
        return self._dict
