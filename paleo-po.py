#!/usr/bin/python

import sys
from random import randint
from asterisk import agi
import requests
import datetime
import json
import os

# Parse arguments
player = sys.argv[1]
pickup_time = datetime.datetime.now()

gestionair = agi.AGI()

gestionair.verbose("HELLO")

try:
    channel = gestionair.env['agi_channel'][4:].split('-')
except:
    channel = [0, 0]

gestionair.verbose("PLAYER:%s / CHANNEL:%s" % (player, channel[0]))

try:
    question = requests.get('http://192.168.1.1/game/agi/%s/%s/' % (player, channel[0])).json()
    gestionair.verbose("SUCCESS")
except:
    gestionair.verbose("EXCEPTION")
    gestionair.verbose(sys.exc_info()[0])

if question['over']=='over':
    gestionair.stream_file('gestionair/over')

else:
    try:
        os.path.isfile('/var/lib/asterisk/sounds/gestionair/speech/%s.sln' % question['file'])
        speech_file = question['file']
    except:
        speech_file = "1-fr"

    gestionair.verbose("FILE: %s" % speech_file)

    gestionair.stream_file('gestionair/speech/%s' % speech_file)

    if speech_file != "1-fr":
        #gestionair.stream_file('gestionair/ringback')

        answer = gestionair.get_data('gestionair/correspondant', max_digits=1)

        if int(answer) == question['response']:
            response = True
        else:
            response = False

        gestionair.verbose("RESPONSE:%s" % response)

        payload = {'answer_id': question['answer_id'], 'answer_key': int(answer),
               'correct': response}

        gestionair.verbose("PAYLOAD:%s" % payload)

        submit = requests.post('http://192.168.1.1/game/agi/', data=json.dumps(payload))

        gestionair.verbose(submit)

        if response:
            gestionair.stream_file('gestionair/thankyou')
        else:
            gestionair.stream_file('gestionair/wrong')

        if question['last']=='last':
            gestionair.stream_file('gestionair/last')
