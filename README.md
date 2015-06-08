# paleo-2015-gestionair-asterisk
Asterisk configuration files

paleo-test.py

```
#!/usr/bin/python

import sys
from random import randint
from asterisk import agi

# Parse arguments
player = sys.argv[1]

Q = [{'file': 0, 'answer': 0}, {'file': 5, 'answer': 5}, {'file': 27, 'answer': 5}, {'file': 46, 'answer': 4}, {'file': 83, 'answer': 3}]

gestionair = agi.AGI()

try:
    channel =  gestionair.env['agi_channel'][4:].split('-')
except:
    channel = [0, 0]

# Debug only
#gestionair.say_digits(player)

# TODO: Get file from simulator
question = Q[randint(0,4)]
gestionair.stream_file(question['file'])
answer = gestionair.get_data('gestionair-correspondant', max_digits=1)

# TODO: Check with real answer
if int(answer) == question['answer']:
    response = True
    gestionair.stream_file('gestionair-thankyou')
else:
    response = False
    gestionair.stream_file('gestionair-wrong')

# TODO: Save everything in the DB
# channel
# player
# question number
# answer
# response
```

extensions_custom.conf

```
[paleo-agi]
exten => 1234,1,Answer()
exten => 1234,n,Wait(1)
exten => 1234,n,Read(code,gestionair-entercode,1)
exten => 1234,n,Playback(gestionair-appel)
exten => 1234,n,AGI(paleo-test.py,${code})
exten => 1234,n,Wait(1)
exten => 1234,n,Hangup()
```
