#!/usr/bin/python

import sys
from random import randint
from asterisk import agi
import requests
import datetime
import json
import os

# Parse arguments
gestionair = agi.AGI()

gestionair.verbose("HELLO")
try:
    channel = gestionair.env['agi_channel'][4:].split('-')
except:
    channel = [0, 0]

try:
    question = requests.get('http://192.168.1.1/game/agi/%s/%s/' % (0, channel[0])).json()
    gestionair.verbose("SUCCESS")
except:
    gestionair.verbose("EXCEPTION")

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

    if response:
        gestionair.stream_file('gestionair/thankyou')
    else:
        gestionair.stream_file('gestionair/wrong')

    gestionair.stream_file('gestionair/d%s' % question['response'])
