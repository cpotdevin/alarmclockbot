import os
import toml
import validator
from talker import Talker
from player import Player


def runStep(step):
    delay = step.get('delay', 0)
    if step['type'] == 'AUDIO_FILE':
        player.play(step['file'], step['thread'], delay)
    else:
        text = talker.process(step)
        talker.say(text, delay)


path = os.path.dirname(os.path.realpath(__file__))

with open(path + '/../config.toml') as config_file:
    config = toml.loads(config_file.read())
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = config['google_credentials']

    audio_cmd = config['audio_cmd']

    language = config.get('language', 'en-US')
    gender = config.get('gender', 'NEUTRAL')
    speaking_rate = config.get('speaking_rate', 0.85)
    pitch = config.get('pitch', 0)
    talker = Talker(audio_cmd, language, gender, speaking_rate, pitch)

    player = Player(audio_cmd)

    for step in config['steps']:
        validator.validateStep(step)

    for step in config['steps']:
        runStep(step)
