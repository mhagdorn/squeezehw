#!/usr/bin/env python

import socket
import lms
import sys
import gpiozero
import time
from pprint import pprint

playerName = socket.gethostname()
server = lms.find_server()
onSwitch = gpiozero.Button(17)
volumePoti = gpiozero.MCP3008(channel=0,device=0)
led = gpiozero.LED(22)

default_playlist = "SWR1 Baden-Wuertenberg"

            
def getPlaylistURI(pl):
    try: 
        uri = server.query('playlists',0,1,dict(search=pl,tags="u"))['playlists_loop'][0]['url']
    except:
        uri = None
    return uri

# find the default playlist
default_uri = getPlaylistURI(default_playlist)

for p in server.players:
    if p.name == playerName:
        player = p
        break
else:
    sys.exit(1)

def switchOn():
    #player.is_playing)
    player.turn_on()
    led.on()
    player.play_uri(default_uri)
def switchOff():
    player.turn_off()
    led.off()

class Volume:
    def __init__(self):
        self._curVolume = -1

    @staticmethod
    def _getVolume():
        return 20+int(volumePoti.value*30)

    def __call__(self):
        v = self._getVolume()
        if v!= self._curVolume:
            self._curVolume = v
            player.set_volume(self._curVolume)


if onSwitch.is_pressed:
    switchOn()
else:
    switchOff()

onSwitch.when_pressed = switchOn
onSwitch.when_released = switchOff
volume = Volume()

print('waiting')
volume()
while True:
    volume()
    time.sleep(0.1)

