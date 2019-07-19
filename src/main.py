import toml
import os
from talker import Talker

path = os.path.dirname(os.path.realpath(__file__))

with open(path + '/../config.toml') as config_file:
    config = toml.loads(config_file.read())
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = config['google_credentials']

    language = config.get('language', 'en-US')
    gender = config.get('gender', 'NEUTRAL')
    speaking_rate = config.get('speaking_rate', 0.85)
    pitch = config.get('pitch', 0)
    talker = Talker(language, gender, speaking_rate, pitch)

    for i, step in enumerate(config['steps']):
        talker.say(step['text'], f'step{i}', step['type'])
