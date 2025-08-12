from spherov2 import scanner
from spherov2.sphero_edu import SpheroEduAPI
from spherov2.types import Color

class bb8v1:
    def __init__(self):
        self.toy = scanner.find_BB8()
        if not self.toy:
            print("Could not find BB8")
        
        # Hack to maintain persistent connection
        self.bb8 = SpheroEduAPI(self.toy)
        self.bb8.__enter__()  # Manually enter context without automatic cleanup
        # F*CK YEAH, WHO NEEDS WITH CONTEX WHEN YOU CAN JUST DO THIS SHIT
        print("Connected to BB8")

    def __del__(self):
        if hasattr(self, 'bb8'):
            self.bb8.__exit__(None, None, None)  # Manually exit context
            print("Disconnected from BB8")
    
    def look(self, angle):
        if not angle:
            return
        self.bb8.set_heading(angle)
    def move(self, speed):
        if not speed:
            self.bb8.set_speed(0)
        self.bb8.set_speed(speed)
    def stop(self):
        self.bb8.stop_roll()
    
    def set_main_led(self, Color):
        self.bb8.set_main_led(Color)

if __name__=="__main__":   # testing
    droid=bb8v1()
    droid.set_main_led(Color(r=0,g=0,b=255))
    droid.move(80)
    from time import sleep
    sleep(3)
    droid.stop()
    del droid