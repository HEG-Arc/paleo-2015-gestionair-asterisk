# paleo-2015-gestionair-asterisk
Asterisk configuration files

paleo-test.py

```
#!/usr/bin/python

import sys
from asterisk import agi

# Parse arguments
player = sys.argv[1]

gestionair = agi.AGI()

# Debug only
gestionair.say_digits(player)

# TODO: Get file from simulator
gestionair.stream_file('alexis2')
answer = gestionair.get_data('gestionair-correspondant', max_digits=1)

# TODO: Check with real answer
if int(answer) == 1:
    gestionair.stream_file('gestionair-thankyou')
    response = True
else:
    gestionair.stream_file('gestionair-wrong')
    response = False

try:
    channel =  gestionair.env['agi_channel'][4:].split('-')
except:
    channel = [0, 0]

gestionair.verbose(extension)

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
