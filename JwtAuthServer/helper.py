from typing import Any, Dict, Union


class ConfigurationSettingsBase(object):
    def __init__(self):
        pass

    def load(self, source: str) -> Dict[str, str]:
        pass

    def load_connection_string(self) -> Dict[str, str]:
        pass


class ConfigurationSettingsLocal(ConfigurationSettingsBase):
    def __init__(self):
        pass

    def load(self, source: str) -> Dict[str, str]:
        pass

    def load_connection_string(self) -> Dict[str, str]:
        pass
