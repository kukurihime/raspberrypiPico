import machine
import utime
import CPiPicoWifi
import CInit
from machine import PWM
import CServoSg90RPPico
import CControlLoop

ini = CInit.CInit()
print( ini.name )
ppw = CPiPicoWifi.CPiPicoWifi(ini.ssid, ini.nwPass)
ppw.connect()
ppw.printStatus()

led = machine.Pin(22, machine.Pin.OUT)
led.toggle()
utime.sleep(0.5)
led.toggle()
utime.sleep(0.5)
led.toggle()
utime.sleep(0.5)

class CMainLoop (CControlLoop.CControlLoop):
    def __init__(self):
        super().__init__(0.1)
        self.sg90 = CServoSg90RPPico.CServoSg90RPPico(2)
        self.sg90.setTarget(0)
        self.target = 0.0
        self.dir = 1
    def loopFunc(self):
        self.sg90.on()
        if self.target >80:
            self.dir = -1
        elif self.target < -80:
            self.dir = 1
        else:
            pass
        self.target += self.dir * (3.0 + self.getLoopCount() * 0.1 )
        self.sg90.setTarget(self.target)
        
    def postProcess(self):
        if self.getLoopCount() >= 600:
            self.loopEnd()
            
ctrl = CMainLoop()
ctrl.loopStart()

led.toggle()
utime.sleep(3)
led.toggle()
utime.sleep(3)
led.toggle()
utime.sleep(3)



