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
volumePoti = gpiozero.MCP3008(channel=0,device=1)
multiSwitch = gpiozero.MCP3008(channel=1,device=1)

default_playlist = "SWR1 Baden-Wuertenberg"

            
def getPlaylistURI(pl):
    try: 
        uri = server.query('playlists',0,1,dict(search=pl,tags="u"))['playlists_loop'][0]['url']
    except:
        uri = None
    return uri

# find the default playlist
default_uri = getPlaylistURI(default_playlist)

channels = {
        2: getPlaylistURI("SWR1"),
        5: getPlaylistURI("Planet Rock"),
        9: getPlaylistURI("SWR2"),
        }

for p in server.players:
    if p.name == playerName:
        player = p
        break
else:
    sys.exit(1)

def switchOn():
    #player.is_playing)
    player.turn_on()
    if player.is_paused:
        print('was paused')
        player.query('pause','0')
    if player.is_stopped:
        print('was stopped')
        # the module is broken
        if False:
            player.play_uri(default_uri)
        else:
            player.query('playlist', 'play', default_uri)
def switchOff():
    player.turn_off()

class Channel:
    def __init__(self,channels):
        self._curChannel = -1
        self._channels = channels
        if True:
            for c in self._channels:
                print(c,self._channels[c])

    @staticmethod
    def _getSwitch():
        return round(multiSwitch.value*10)

    def __call__(self,change=True):
        s = self._getSwitch()
        if s!=self._curChannel:
            self._curChannel = s
            try:
                c = self._channels[s]
            except:
                c = default_uri
            if change:
                player.play_uri(c)

class Volume:
    def __init__(self):
        self._curVolume = -1

    @staticmethod
    def _getVolume():
        return int(volumePoti.value*100)

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
channel = Channel(channels) 

print('waiting')
volume()
channel(change=False)
while True:
    volume()
    channel()
    time.sleep(0.2)

