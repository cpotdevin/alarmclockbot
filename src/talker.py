import os
import subprocess
import time
import hashlib
from datetime import datetime
from google.cloud import texttospeech

path = os.path.dirname(os.path.realpath(__file__))


class Talker:
    def __init__(self,
                audio_cmd,
                language='en-US',
                gender='NEUTRAL',
                speaking_rate=0.85,
                pitch=0):
        self.audio_cmd = audio_cmd

        self.client = texttospeech.TextToSpeechClient()

        if gender == 'MALE':
            gender_enum = texttospeech.enums.SsmlVoiceGender.MALE
        elif gender == 'FEMALE':
            gender_enum = texttospeech.enums.SsmlVoiceGender.FEMALE
        else:
            gender_enum = texttospeech.enums.SsmlVoiceGender.NEUTRAL

        self.voice = texttospeech.types.VoiceSelectionParams(language_code=language, ssml_gender=gender_enum)
        self.audio_config = texttospeech.types.AudioConfig(
            audio_encoding=texttospeech.enums.AudioEncoding.MP3,
            speaking_rate=speaking_rate,
            pitch=pitch
        )

    def process(self, step):
        if step['type'] == 'SIMPLE_TEXT':
            return step['text']
        elif step['type'] == 'TIMESTAMP_TEXT':
            timestamp = datetime.now()

            date = timestamp.date()
            dateSsml = f'<say-as interpret-as="date" format="yyyymmdd" detail="1">{date}</say-as>'

            time = timestamp.strftime('%I:%M%p')
            timeSsml = f'<say-as interpret-as="time" format="hms12">{time}</say-as>'
            return step['text'].format(dateSsml, timeSsml)
        return ''

    def say(self, text, delay=0):
        time.sleep(delay)

        id = hashlib.sha1(text.encode()).hexdigest()
        output_file = path + '/../audio/' + id + '.mp3'

        if not os.path.isfile(output_file):
            print(f'creating audio file {output_file}')
            if text.startswith('<speak>'):
                ssml = text
            else:
                ssml = f'<speak>{text}<break time="300ms" /></speak>'

            synthesis_input = texttospeech.types.SynthesisInput(ssml=ssml)
            response = self.client.synthesize_speech(synthesis_input, self.voice, self.audio_config)

            with open(output_file, 'wb') as out:
                out.write(response.audio_content)

        subprocess.run(self.audio_cmd.format(output_file), shell=True)
