from google.cloud import texttospeech
import os
import subprocess


class Talker:
    def __init__(self,
                language='en-US',
                gender='NEUTRAL',
                speaking_rate=0.85,
                pitch=0):
        self.client = texttospeech.TextToSpeechClient()

        if (gender == 'MALE'):
            gender_enum = texttospeech.enums.SsmlVoiceGender.MALE
        elif (gender == 'FEMALE'):
            gender_enum = texttospeech.enums.SsmlVoiceGender.FEMALE
        else:
            gender_enum = texttospeech.enums.SsmlVoiceGender.NEUTRAL

        self.voice = texttospeech.types.VoiceSelectionParams(language_code=language, ssml_gender=gender_enum)
        self.audio_config = texttospeech.types.AudioConfig(
            audio_encoding=texttospeech.enums.AudioEncoding.MP3,
            speaking_rate=speaking_rate,
            pitch=pitch
        )

    def say(self, text, id, type):
        output_file = 'audio/' + id + '.mp3'

        if (type == 'VARIABLE' or not os.path.isfile(output_file)):
            print('creating audio')
            if (text.startswith('<speak>')):
                ssml = text
            else:
                ssml = f'<speak>{text}</speak>'

            synthesis_input = texttospeech.types.SynthesisInput(ssml=ssml)
            response = self.client.synthesize_speech(synthesis_input, self.voice, self.audio_config)

            with open(output_file, 'wb') as out:
                out.write(response.audio_content)

        subprocess.run(["afplay", output_file])
