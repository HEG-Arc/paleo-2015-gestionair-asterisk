#!/usr/bin/python

import logging
import sys
from random import randint
from asterisk import agi
import requests
import datetime
import json
import os


logging.basicConfig(filename='/var/log/gestionair/agi.log',level=logging.INFO)

logging.info("%s-New call: %s" % (datetime.datetime.now(), sys.argv))
# Parse arguments
player = sys.argv[1]
pickup_time = datetime.datetime.now()

gestionair = agi.AGI()


try:
    channel = gestionair.env['agi_channel'][4:].split('-')
    current = channel[0]
except:
    channel = [0, 0]
    current = channel[0]
    logging.error("Unable to detect channel from: %s" % gestionair.env['agi_channel'])

if len(player) == 3:
    logging.info("[%s] PLAYER:%s / CHANNEL:%s" % (current, player, channel[0]))
else:
    logging.error("[%s] PLAYER:%s / CHANNEL:%s" % (current, player, channel[0]))
    gestionair.stream_file('gestionair/wrong-code')
    gestionair.hangup()
    sys.exit()

try:
    question = requests.get('http://192.168.1.1/game/agi/%s/%s/' % (player, channel[0])).json()
    logging.info("[%s] Received question: %s" % (current, question))
except:
    logging.error("[%s] Unable to get a question: %s" % (current, sys.exc_info()[0]))

if question['over']=='over':
    gestionair.stream_file('gestionair/over')

else:
    try:
        os.path.isfile('/var/lib/asterisk/sounds/gestionair/speech/%s.sln' % question['file'])
        speech_file = question['file']
        logging.info("[%s] Playing file: %s" % (current, speech_file))
    except:
        speech_file = "1-fr"
        logging.error("[%s] Unable to play file: %s" % (current, speech_file))

    gestionair.stream_file('gestionair/speech/%s' % speech_file)

    if speech_file != "1-fr":
        #gestionair.stream_file('gestionair/ringback')

        answer = gestionair.get_data('gestionair/correspondant', max_digits=1)
        logging.info("[%s] Received answer: %s" % (current, answer))
        if int(answer) == question['response']:
            response = True
        else:
            response = False

        payload = {'answer_id': question['answer_id'], 'answer_key': int(answer),
               'correct': response}

        logging.info("[%s] PAYLOAD: %s" % (current, payload))

        submit = requests.post('http://192.168.1.1/game/agi/', data=json.dumps(payload))
        if submit.status_code == 200:
            logging.info("[%s] Response submitted: %s" % (current, submit.status_code))
        else:
            logging.error("[%s] Unable to submit response: %s" % (current, submit.text))

        if response:
            gestionair.stream_file('gestionair/thankyou')
        else:
            gestionair.stream_file('gestionair/wrong')

        if question['last']=='last':
            gestionair.stream_file('gestionair/last')

        logging.info("[%s] End" % current)
