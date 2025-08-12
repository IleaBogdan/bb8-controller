from spherov2.types import Color
from controllers import XboxOneController
from droids import bb8v1
import pygame
import calc
import math

def main():
    droid=bb8v1()
    droid.set_main_led(Color(r=0,g=0,b=255))
    ctrl=XboxOneController()
    drive=False
    while True:
        pygame.event.pump()
        
        axis=ctrl.get_axis()
        button_states=ctrl.get_button_states()

        if button_states['M']:
            droid.stop()
            break
        if axis['left_trigger']:
            droid.stop()
            print("driving stopped")
            drive=False
        if not drive and axis['right_trigger']:
            print("driving started")
            drive=True

        if not drive: continue
        fangle=calc.get_angle(axis["right_x"],axis["right_y"])
        # fspeed=calc.get_speed(axis["left_x"],axis["left_y"])
        fspeed=calc.get_speed(axis["right_trigger"])
        fangle,fspeed=math.floor(fangle) if fangle!=None else None,math.floor(fspeed) if fspeed!=None else None # flooring the values for the sphero function 
        
        droid.look(fangle)
        droid.move(fspeed) 

if __name__=="__main__":
    main()