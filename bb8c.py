from spherov2 import scanner
from spherov2.sphero_edu import SpheroEduAPI
from spherov2.types import Color
from controllers import XboxOneController
import pygame
import math
import calc

# const values:
modSpeed=50
turboSpeed=150 # deepseek says this might be the max speed, but idk
maxSpeed=255

def move(droid, fangle, fspeed):
    if (fangle!=None):
        droid.set_heading(fangle)
    if (fspeed!=None):
        droid.set_speed(fspeed)
        # if fspeed<0:
        #     droid.set_heading(droid.get_heading())

def on_collision(droid):
    droid.stop_roll()
    print("I hit something")

def find_bb8():
    spherobb8=scanner.find_BB8()
    print("connected to bb8")
    print("after bb8 glows blue press Right Trigger to start driving and Left Trigger stop driving")
    return spherobb8

def main():
    # print("F")
    try:
        spherobb8=find_bb8()
    except Exception as e:
        print(e)
        return
    xoc=XboxOneController(0)
    with SpheroEduAPI(spherobb8) as bb8:
        bb8.set_main_led(Color(r=0, g=0, b=255))

        print("you can drive bb8 now")
        drive=False
        while True:
            pygame.event.pump() # VERY IMPORTANT, THIS ALLOWS THE BLUETOOTH TO TAKE THE CONTROLLER INPUT
            
            axis=xoc.get_axis()
            button_states=xoc.get_button_states()
            # print(button_states)
            if button_states['M']:
                bb8.stop_roll()
                break
            if axis['left_trigger']:
                bb8.stop_roll()
                print("driving stopped")
                drive=False
            if axis['right_trigger']:
                print("driving started")
                drive=True
                
            if not drive:
                continue

            fangle=calc.get_angle(axis["right_x"],axis["right_y"])
            # fspeed=calc.get_speed(axis["left_x"],axis["left_y"])
            fspeed=calc.get_speed(axis["right_trigger"])
            fangle,fspeed=math.floor(fangle) if fangle!=None else None,math.floor(fspeed) if fspeed!=None else None # flooring the values for the sphero function 
            
            # print(f"{axis["left_x"]},{axis["left_y"]}")
            
            move(bb8, fangle, fspeed) 
            
    del xoc

if __name__=="__main__":
    main()