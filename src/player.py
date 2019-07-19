import os
import subprocess
import time

path = os.path.dirname(os.path.realpath(__file__))


class Player:
    def __init__(self, audio_cmd):
        self.audio_cmd = audio_cmd

    def play(self, file_name, thread='CONCURRENT', delay=0):
        time.sleep(delay)
        file = path + '/../audio/' + file_name
        if thread == 'CONCURRENT':
            subprocess.run(self.audio_cmd.format(file), shell=True)
        else:
            subprocess.Popen(self.audio_cmd.format(file), shell=True)
