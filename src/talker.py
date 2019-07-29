import os
import subprocess
import time
import hashlib
from datetime import datetime
import requests
from google.cloud import texttospeech

path = os.path.dirname(os.path.realpath(__file__))


class Talker:
    def __init__(self,
                audio_cmd,
                weekdays,
                lang,
                gender,
                speaking_rate,
                pitch):
        self.audio_cmd = audio_cmd
        self.weekdays = weekdays

        self.client = texttospeech.TextToSpeechClient()

        if gender == 'MALE':
            gender_enum = texttospeech.enums.SsmlVoiceGender.MALE
        elif gender == 'FEMALE':
            gender_enum = texttospeech.enums.SsmlVoiceGender.FEMALE
        else:
            gender_enum = texttospeech.enums.SsmlVoiceGender.NEUTRAL

        self.voice = texttospeech.types.VoiceSelectionParams(language_code=lang, ssml_gender=gender_enum)
        self.audio_config = texttospeech.types.AudioConfig(
            audio_encoding=texttospeech.enums.AudioEncoding.MP3,
            speaking_rate=speaking_rate,
            pitch=pitch
        )


    def process(self, step):
        if step['type'] == 'SIMPLE_TEXT':
            return step['text']
        elif step['type'] == 'TIMESTAMP_TEXT':
            return self.processTimestampStep(step)
        elif step['type'] == 'API_TEXT':
            return self.processAPIStep(step)
        return ''


    def processTimestampStep(self, step):
        timestamp = datetime.now()

        date = timestamp.date()
        dateSsml = f'<say-as interpret-as="date" format="yyyymmdd" detail="1">{date}</say-as>'

        month = timestamp.month
        monthSsml = f'<say-as interpret-as="date" format="m" detail="1">{month}</say-as>'

        day = timestamp.day
        daySsml = f'<say-as interpret-as="ordinal">{day}</say-as>'

        time = timestamp.strftime('%I:%M%p')
        timeSsml = f'<say-as interpret-as="time" format="hms12">{time}</say-as>'

        weekday = self.weekdays[timestamp.weekday()]

        return step['text'].format(date=dateSsml, month=monthSsml, day=daySsml, time=timeSsml, weekday=weekday)

    def processAPIStep(self, step):
        parameters = None
        if step.get('parameters') is not None:
            parameters = step['parameters']
        response = requests.get(step['url'], params=parameters)

        values = []
        for i, path in enumerate(step['paths']):
            values.append(response.json())

            for key in path:
                if key[:1] == '$':
                    try:
                        key = int(key[1:])
                    except ValueError:
                        pass
                values[i] = values[i][key]

            try:
                values[i] = float(values[i].replace(',', ''))
            except ValueError:
                pass

        return step['text'].format(*values)


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
