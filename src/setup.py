import sys
import os
import toml
from crontab import CronTab

path = os.path.dirname(os.path.realpath(__file__))

with open(path + '/../config.toml') as config_file:
    config = toml.loads(config_file.read())

    schedule = config.get('schedule')
    if schedule == None:
        print('Please set the "schedule" value in the config file.')
        sys.exit()

    command = f'python3  {path}/main.py'

    cron = CronTab(user=True)

    alarm = cron.find_comment('alarmclockbutler')
    cron.remove(alarm)

    if '-r' not in sys.argv:
        alarm = cron.new(command=command, comment='alarmclockbutler')
        alarm.setall(schedule)

    cron.write()
