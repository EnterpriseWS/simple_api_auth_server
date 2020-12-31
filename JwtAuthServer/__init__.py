import json

settings_file = open('settings.json')
settings = json.load(settings_file)
settings_file.close()