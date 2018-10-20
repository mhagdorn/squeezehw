import socket
import lms
import sys
import gpiozero
import time

playerName = socket.gethostname()
server = lms.find_server()
onSwitch = gpiozero.Button(17)
volumePoti = gpiozero.MCP3008(channel=0,device=1)

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
        player.query('pause','0')
    if player.is_stopped:
        pass
    print(player.query(
                    'status', '-', '1', 'tags:adKl'))
def switchOff():
    player.turn_off()

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

print('waiting')
volume()
while True:
    volume()
    time.sleep(0.2)

