from spherov2 import scanner
from spherov2.sphero_edu import SpheroEduAPI
from spherov2.types import Color
from controllers import XboxOneController
import pygame
import math

# const values:
modSpeed=50
turboSpeed=150 # deepseek says this might be the max speed, but idk
maxSpeed=255

def calc_angle(x, y):
    '''
        +1
    -1      +1
        -1
    '''
    if x==0 and y==0: return None
    y=-y # making y to be in the xOy 
    sin_AOB=abs(x)/math.sqrt(x*x+y*y)
    rad_AOB=math.asin(sin_AOB)
    deg_AOB=(rad_AOB*180.0)/math.pi
    if x>0 and y<0:
        # quadrant 4 (idk some symmetry stuff)
        deg_AOB=180-deg_AOB
    elif x<0 and y<0:
        # quadrant 3 (adding 180 to flip it)
        deg_AOB+=180
    elif x<0 and y>0:
        # quadrant 2 (same stuff as quadrant 4 but with +180)
        deg_AOB=360-deg_AOB
    return deg_AOB

def calc_speed(x, y):
    is_neg=-1 if y>0.0 else 1
    speed=math.sqrt(x*x+y*y)*100.0*is_neg # this formula is shit, but I have no better ideas for it 
    return speed

def move(droid, fangle, fspeed):
    if (fspeed!=None):
        droid.set_speed(fspeed)
        if fspeed<0:
            droid.set_heading(droid.get_heading())
    if (fangle!=None):
        droid.set_heading(fangle)

def on_collision(droid):
    droid.stop_roll()
    print("I hit something")

def find_bb8():
    spherobb8=scanner.find_BB8()
    print("connected to bb8")
    print("after bb8 glows blue press 'A' to start driving or stop driving")
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
            
            button_states=xoc.get_button_states()
            # print(button_states)
            if button_states['M']:
                break
            if button_states['A']:
                drive=not drive
                print(("driving stopped", "driving started")[drive])
            if not drive:
                continue

            axis=xoc.get_axis()
            fangle,fspeed=calc_angle(axis["right_x"],axis["right_y"]),calc_speed(axis["left_x"],axis["left_y"])
            fangle,fspeed=math.floor(fangle) if fangle!=None else None,math.floor(fspeed) if fspeed!=None else None # flooring the values for the sphero function 
            
            # print(f"{axis["left_x"]},{axis["left_y"]}")
            
            move(bb8, fangle, fspeed) 
            
    del xoc

if __name__=="__main__":
    main()